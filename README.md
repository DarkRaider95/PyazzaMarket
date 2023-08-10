To do list funzionalità:
- ~~ pedaggi e incidenti ~~
    - ~~ fixare celle,bisogna crearne una per nome adesso sono stampate per colore tutte uguali ~~
- ~~ passaggio via ~~
- ~~ aggiungere situazione doppio dado ~~
- ~~ tabella con proprietà per giocatore ~~
    - ~~ aggiunge x1 o x2 in base al numero di stock ~~
    - ~~ nel caso che le stock siano le stesse non aggiornare ~~
- ~~ caselle speciali, angoli, dadi ~~ 
- ~~ mostra turno ~~
- ~~ quotazioni, senza asta ~~
    - ~~ calcolo penalità ~~
    - ~~ calcolo differenza da dare ai giocatori ~~
- eventi
    - eventi colorati
    - grafica per scegliere accompagnatore
    - grafica per avviare trattative
- loghi
- mostra cedole
    - ~~ fermata libera ~~
    - in showStockUi devo controllare se ci sono 0 cedole da mostrare per qualsiasi ragione essa sia e mostrare che non ci sono cedole
    - asta
- bancarotta
    - vendita, dopo asta
- macchine
    - due nuove macchine
    - messaggio in caso di doppia selezione della stessa macchina
- ~~ ordinare le label quando mostrate di modo da far vedere chi è in testa ~~
- aggiungere tasto salva, per salvare stato partita
- ~~ gestire default piazza ~~
- controllare cella lancio dadi per perdere o vincere sulla piazza
- ~~ fare la ui per incidenti, tiri doppi, penalità ecc ~~
    - ~~ bloccare altri tasti fino a quando non si fa kill o fare kill nel caso si usi un altro bottone ~~
- ~~ interfaccia per tiro dadi per celle speciali, inizio partita ecc ~~
    - ~~ tiro dadi a inizio partita ~~
        - ~~ gestire tiro pari ~~
- aggiungere lunghezza massima nome giocatore
- add requirements.txt
- aggiungere un logger
- aggiungere aggiornamento bottoni basato su timestamp

To fix:
- ~~ fix the two line to draw in stock ~~
- ~~ fix doppio prima di casella combi ~~
- asta no offerte per il giocatore che vende

To do list codice:
- fare getters and setters
    - mettere private le variabili
- sistemtare la grafica
    - responsive
    - usare valori negativi dove possibile
- ~~ unit test ~~

To do extra:
- funzionalità di rete
- eseguibili
- ai

Per eseguire i test basta chiamare "pytest", per vedere la copertura "pytest --cov" e per fare un repor "coverage html"

Refactor dopo test:
- cancellare initialize_cells in board e metterlo nel init