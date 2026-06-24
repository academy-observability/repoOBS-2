Da: Andrea Bello
Per il punto 9 del Guidato UD04, consiglio di installare da riga di comando la libreria jq 
(documentazione reperibile qui: https://jqlang.org/). 
Per installarla da riga di comando basta fare: sudo apt install jq. 
Poi nel comando tail "-n ... | " sostituite "python3 -m json.tool" con "jq ."
