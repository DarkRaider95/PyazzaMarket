To do list funzionalità:
- eventi
    - grafica per scegliere accompagnatore
    - grafica per avviare trattative
- mostra cedole
    - in showStockUi devo controllare se ci sono 0 cedole da mostrare per qualsiasi ragione essa sia e mostrare che non ci sono cedole
- trattative
    - aggiungere i soldi alle trattative
- macchine
    - due nuove macchine
    - messaggio in caso di doppia selezione della stessa macchina
- aggiungere tasto salva, per salvare stato partita
- controllare cella lancio dadi per perdere o vincere sulla piazza
- aggiungere lunghezza massima nome giocatore
- add requirements.txt
- aggiungere un logger
- aggiungere aggiornamento bottoni basato su timestamp

To fix:
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

- controllare i clock.tick
- controllare che bargain venga eseguito dopo eventuale incidente siccome il bilancio virtuale viene aggiornato all'apertura della finestra

To do list codice:
- fare getters and setters
    - mettere private le variabili
- sistemtare la grafica
    - responsive
    - usare valori negativi dove possibile

To do extra:
- funzionalità di rete
- eseguibili
- ai

Per eseguire i test basta chiamare "pytest", per vedere la copertura "pytest --cov" e per fare un repor "coverage html"

Refactor dopo test:
- cancellare initialize_cells in board e metterlo nel init