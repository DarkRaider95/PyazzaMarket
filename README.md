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
    ~~ eventi colorati ~~
    - grafica per scegliere accompagnatore
    - grafica per avviare trattative
- ~~ loghi ~~
- mostra cedole
    - ~~ fermata libera ~~
    - in showStockUi devo controllare se ci sono 0 cedole da mostrare per qualsiasi ragione essa sia e mostrare che non ci sono cedole
    - asta
- bancarotta
    ~~ vendita, dopo asta ~~
    ~~ gestire gli indici dopo la rimozione dei giocatori ~~
    ~~ gestire bancarotte multiple ~~
- trattative
    - aggiungere i soldi alle trattative
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
- ~~ asta no offerte per il giocatore che vende ~~
- alert e showStockUI da mettere a parte nel loop principale in questo modo fixo le sovrapposizioni una volta per tutte
    - voglio mettere prima l'oggetto in una variabile globale invece di disegnare subito l'alert
    - voglio creare anche la lista degli alert
    - voglio mettere una variabile tipo in show stock ui e in base al tipo chiamo il metodo corretto che disegna in maniera diversa la gui
      attualmente invece non posso aspettare di disegnare perché poi non so il tipo di gui da mostrare
    - in questo modo nel loop principale controllo se ci sono alert o gui da mostrare
    - se ci sono le disegno una alla volta
    - decidiamo poi la priorità delle gui e degli alert
- dopo chiusura della compra vendita di azioni nella casella fermata libera senza comprare nulla i tasti rimangono bloccati
- fare le cedole uguali a quelle vere
- aste
    - se rimane un solo giocatore che ha fatto l'offerta è costretto a comprare la cedola
    - se nessuno ha offerto allora si possono ritirare tutti e la cedola va alla banca
    - salvare i balance all'inizio delle aste per evitare che il primo che riceve i soldi dell'asta sia avvantaggiato sugli altri

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