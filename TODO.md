# TODO
## Funziolità di gioco da implementare
### Eventi:
- Evento delle cedole colorate
    - controllo cedole colorate non ha funzionato
    - abbiamo fatto che i dadi si chiudono da soli ma dobbiamo studiare come farlo meglio non fare handle color event finché non si 
    chiude il dice overlay
### Aste
- salvare i balance all'inizio delle aste per evitare che il primo che riceve i soldi dell'asta sia avvantaggiato sugli altri

### Funzionalità generali
 - aggiungere un logger
 - sistemare la grafica responsive
    - (non si sa bene) usare valori negativi dove possibile
 - funzionalità di rete
 - eseguibili
 - ai

## To FIX
- macchine
  - due nuove macchine
- non si legge la descrizione del titolo nella finestra delle aste
- non si legge la label del bottone per mettere all'asta la cedola
- controllare se c'è la logica del perdi un giro
- controllare logica riserva di piazza lanciando 1 i soldi in piazza sono diminuiti

## Non sappiamo se fare 
- controllare i clock.tick
- controllare che bargain venga eseguito dopo eventuale incidente siccome il bilancio virtuale viene aggiornato all'apertura della finestra
- controllare cella lancio dadi per perdere o vincere sulla piazza
- cancellare initialize_cells in board e metterlo nel init
- in showStockUi devo controllare se ci sono 0 cedole da mostrare per qualsiasi ragione essa sia e mostrare che non ci sono cedole

## Comandi utili
Per eseguire i test basta chiamare "pytest", per vedere la copertura "pytest --cov" e per fare un repor "coverage html"
