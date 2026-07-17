import html
import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from flask import Flask, Response, jsonify, redirect, request

PORT = int(os.getenv("PORT", "5001"))
EVENT_FILE = Path(os.getenv("EVENT_FILE", "/data/events.jsonl"))
MAX_EVENTS = int(os.getenv("MAX_EVENTS", "500"))

app = Flask(__name__)
file_lock = threading.Lock()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_storage() -> None:
    EVENT_FILE.parent.mkdir(parents=True, exist_ok=True)
    EVENT_FILE.touch(exist_ok=True)


def load_events() -> list[dict[str, Any]]:
    ensure_storage()
    events: list[dict[str, Any]] = []
    with file_lock:
        with EVENT_FILE.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    events.append({"received_at": None, "payload": {"invalid_json_line": line}})
    return events[-MAX_EVENTS:]


def save_event(payload: Any, remote_addr: str | None) -> int:
    ensure_storage()
    event = {
        "received_at": utc_now(),
        "remote_addr": remote_addr,
        "payload": payload,
    }
    with file_lock:
        existing = EVENT_FILE.read_text(encoding="utf-8").splitlines()
        existing = [line for line in existing if line.strip()][-(MAX_EVENTS - 1):]
        existing.append(json.dumps(event, ensure_ascii=False))
        EVENT_FILE.write_text("\n".join(existing) + "\n", encoding="utf-8")
        return len(existing)


def summarize(event: dict[str, Any]) -> tuple[str, str, str, int]:
    payload = event.get("payload")
    if not isinstance(payload, dict):
        return "unknown", "-", "payload non-oggetto", 0

    status = str(payload.get("status", "unknown"))
    receiver = str(payload.get("receiver", "-"))
    alerts = payload.get("alerts")
    alert_count = len(alerts) if isinstance(alerts, list) else 0
    alert_name = "-"
    if isinstance(alerts, list) and alerts:
        first = alerts[0]
        if isinstance(first, dict):
            labels = first.get("labels")
            if isinstance(labels, dict):
                alert_name = str(labels.get("alertname", labels.get("rulename", "-")))
    if status == "unknown" and payload.get("title"):
        status = "test"
    return status, receiver, alert_name, alert_count


@app.get("/")
def root():
    return redirect("/events")


@app.get("/health")
def healthcheck():
    ensure_storage()
    return jsonify({"status": "ok", "service": "ud21-webhook-receiver", "event_file": str(EVENT_FILE)})


@app.post("/grafana-alert")
def grafana_alert():
    payload = request.get_json(silent=True)
    if payload is None:
        raw = request.get_data(as_text=True)
        payload = {"raw_body": raw, "content_type": request.content_type}
    count = save_event(payload, request.remote_addr)
    print(json.dumps({"message": "grafana_webhook_received", "stored_events": count, "payload": payload}, ensure_ascii=False), flush=True)
    return jsonify({"accepted": True, "stored_events": count}), 202


@app.get("/api/events")
def api_events():
    return jsonify({"events": list(reversed(load_events()))})


@app.post("/clear")
def clear_events():
    ensure_storage()
    with file_lock:
        EVENT_FILE.write_text("", encoding="utf-8")
    if request.accept_mimetypes.best == "text/html":
        return redirect("/events")
    return jsonify({"cleared": True})


@app.get("/events")
def events_page():
    events = list(reversed(load_events()))
    rows: list[str] = []
    for index, event in enumerate(events, start=1):
        status, receiver, alert_name, alert_count = summarize(event)
        payload_pretty = json.dumps(event.get("payload"), ensure_ascii=False, indent=2)
        rows.append(
            "<tr>"
            f"<td>{index}</td>"
            f"<td>{html.escape(str(event.get('received_at', '-')))}</td>"
            f"<td><strong>{html.escape(status)}</strong></td>"
            f"<td>{html.escape(receiver)}</td>"
            f"<td>{html.escape(alert_name)}</td>"
            f"<td>{alert_count}</td>"
            f"<td><details><summary>Mostra JSON</summary><pre>{html.escape(payload_pretty)}</pre></details></td>"
            "</tr>"
        )

    body = "".join(rows) or "<tr><td colspan='7'>Nessun evento ricevuto.</td></tr>"
    page = f"""
<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="refresh" content="10">
  <title>UD21 - Grafana Webhook Events</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 28px; background: #f7f7f8; color: #222; }}
    h1 {{ margin-bottom: 6px; }}
    .meta {{ margin-bottom: 18px; color: #555; }}
    table {{ border-collapse: collapse; width: 100%; background: white; }}
    th, td {{ border: 1px solid #ddd; padding: 9px; vertical-align: top; text-align: left; }}
    th {{ background: #ececef; }}
    pre {{ max-width: 900px; white-space: pre-wrap; word-break: break-word; }}
    .actions {{ margin: 14px 0; display: flex; gap: 12px; align-items: center; }}
    button {{ padding: 8px 12px; cursor: pointer; }}
    code {{ background: #eee; padding: 2px 4px; }}
  </style>
</head>
<body>
  <h1>UD21 - Grafana Webhook Events</h1>
  <div class="meta">
    Receiver Docker: <code>http://webhook-receiver:5001/grafana-alert</code><br>
    Pagina host: <code>http://localhost:5001/events</code><br>
    Persistenza: <code>/data/events.jsonl</code> nel volume <code>obs-ud21-webhook-data</code>.
  </div>
  <div class="actions">
    <form method="post" action="/clear" onsubmit="return confirm('Cancellare tutti gli eventi webhook?');">
      <button type="submit">Cancella eventi</button>
    </form>
    <span>Aggiornamento automatico ogni 10 secondi.</span>
  </div>
  <table>
    <thead>
      <tr><th>#</th><th>Ricevuto</th><th>Status</th><th>Receiver</th><th>Alert</th><th>N. alert</th><th>Payload</th></tr>
    </thead>
    <tbody>{body}</tbody>
  </table>
</body>
</html>
"""
    return Response(page, mimetype="text/html")


if __name__ == "__main__":
    ensure_storage()
    app.run(host="0.0.0.0", port=PORT, threaded=True)
