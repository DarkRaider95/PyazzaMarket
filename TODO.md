# TODO
## Funziolità di gioco da implementare
### Eventi:
- Grafica per scegliere accompagnatore
- Evento delle cedole colorate
### Aste
- salvare i balance all'inizio delle aste per evitare che il primo che riceve i soldi dell'asta sia avvantaggiato sugli altri

### Funzionalità generali
 - aggiungere tasto salva, per salvare stato partita
 - add requirements.txt
 - aggiungere un logger
 - sistemare la grafica responsive
    - (non si sa bene) usare valori negativi dove possibile
 - funzionalità di rete
 - eseguibili
 - ai

## To FIX
- macchine
  - due nuove macchine
  - messaggio in caso di doppia selezione della stessa macchina
- non si legge la descrizione del titolo nella finestra delle aste
- non si legge la label del bottone per mettere all'asta la cedola
- aggiungere lunghezza massima nome giocatore
- controllare se c'è la logica del perdi un giro

## Non sappiamo se fare 
- controllare i clock.tick
- controllare che bargain venga eseguito dopo eventuale incidente siccome il bilancio virtuale viene aggiornato all'apertura della finestra
- controllare cella lancio dadi per perdere o vincere sulla piazza
- cancellare initialize_cells in board e metterlo nel init
- in showStockUi devo controllare se ci sono 0 cedole da mostrare per qualsiasi ragione essa sia e mostrare che non ci sono cedole

## Comandi utili
Per eseguire i test basta chiamare "pytest", per vedere la copertura "pytest --cov" e per fare un repor "coverage html"