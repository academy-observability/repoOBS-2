global:
  scrape_interval: 10s
  evaluation_interval: 10s

scrape_configs:
  - job_name: "products-backend"
    metrics_path: /metrics
    static_configs:
      - targets: ["backend-products:8000"]

  - job_name: "products-frontend"
    metrics_path: /metrics
    static_configs:
      - targets: ["frontend-products:8080"]

  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]
