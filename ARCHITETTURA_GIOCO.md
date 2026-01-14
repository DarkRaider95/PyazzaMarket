# Architettura PyazzaMarket - Documentazione Completa

## Indice
1. [Panoramica Generale](#panoramica-generale)
2. [Creazione Board e Caricamento Asset](#creazione-board-e-caricamento-asset)
3. [Gestione Eventi Pygame](#gestione-eventi-pygame)
4. [Sistema di Pannelli e Finestre](#sistema-di-pannelli-e-finestre)
5. [UIComponents Principali](#uicomponents-principali)
6. [Game Logic](#game-logic)
7. [Flusso di Gioco](#flusso-di-gioco)
8. [Esempi Completi](#esempi-completi)
9. [Diagrammi](#diagrammi)

---

## Panoramica Generale

PyazzaMarket è un gioco tipo Monopoly implementato con Pygame e pygame_gui. L'architettura si basa su:

- **Gestione eventi centralizzata** tramite il metodo `manage_events()` in `Game`
- **Sistema a coda di pannelli** per mostrare finestre in sequenza
- **Separazione tra UI e logica** di gioco
- **State management** tramite `ActionsStatus` per abilitare/disabilitare bottoni

### Struttura File Principali

```
lib/
├── game.py                    # Classe principale del gioco
├── gameLogic.py              # Logiche di gioco (turni, cedole, penalità)
├── player.py                 # Classe giocatore
├── board.py                  # Tabellone di gioco
├── stock.py                  # Cedole
├── auction.py                # Sistema d'asta
├── event.py                  # Eventi casuali
└── uiComponents/
    ├── gameUI.py             # UI principale (dadi, azioni, leaderboard)
    ├── eventUI.py            # Pannello eventi
    ├── bargainUI.py          # Pannello contrattazioni
    ├── showStockUI.py        # Pannello cedole
    ├── diceOverlayUI.py      # Overlay per lancio dadi
    └── takeSomeoneWithYouUI.py  # Pannello "porta qualcuno con te"
```

---

## Creazione Board e Caricamento Asset

### Architettura del Tabellone

Il tabellone è composto da **40 celle** disposte a quadrato:
- **4 angoli** (celle speciali)
- **36 celle laterali** divise in 4 lati da 9 celle ciascuno

### Struttura CELLS_DEF

Le celle sono definite in `constants.py` tramite il dizionario `CELLS_DEF`:

```python
CELLS_DEF = {
    'ORANGE': {
        'logos': ['gled.png', 'friskies.png', 'frio.png'],
        'value': 200,                                    # Valore base cedola
        'color': ORANGE,                                 # Colore RGB
        'penalty': [60, 160, 160, 200, 260, 500],       # Penalità per n cedole
        'side': 'BOT',                                   # Lato del tabellone
        'angle': 0,                                      # Rotazione grafica
        'names': ['gled', 'friskies', 'frio'],          # Nomi aziende
        'index': 0                                       # Indice colore
    },
    'LIGHT_BLUE': { ... },
    'PINK': { ... },
    'GREEN': { ... },
    'RED': { ... },
    'BLUE': { ... },
    'YELLOW': { ... },
    'PURPLE': { ... }
}
```

#### Struttura Penalty Array

L'array `penalty` ha 6 elementi corrispondenti a:
1. **1 cedola** dello stesso colore
2. **2 cedole** della stessa società
3. **3 cedole** dello stesso colore
4. **4 cedole** dello stesso colore
5. **5 cedole** dello stesso colore
6. **6 cedole** dello stesso colore

### Costruzione del Board

Il metodo `Board.__init__()` costruisce il tabellone in senso **orario** partendo dall'angolo in basso a destra:

```python
class Board:
    def __init__(self, enableGraphics=True):
        self.__cells = []

        # 1. CORNER 1 (Partenza) - Posizione 0
        curr_x = WIDTH - 10 - CORNER_WIDTH
        curr_y = HEIGHT - 10 - CORNER_HEIGHT
        corner1 = Cell(..., START_TYPE, ...)
        self.__cells.append(corner1)

        # 2. LATO INFERIORE (Posizioni 1-9)
        curr_x, curr_y, position = self.create_side(
            curr_x, curr_y,
            ["ORANGE", "LIGHT_BLUE"],  # 2 colori per lato
            self.eventImage,
            self.fermataLibImage,
            FREE_STOP_TYPE,
            position
        )

        # 3. CORNER 2 (Riserva Cedole) - Posizione 10
        corner2 = Cell(..., STOCKS_PRIZE_TYPE, ...)

        # 4. LATO SINISTRO (Posizioni 11-19)
        curr_x, curr_y, position = self.create_side(
            curr_x, curr_y,
            ["PINK", "GREEN"],
            self.eventImage,
            self.quotationImage,
            QUOTATION_TYPE,
            position
        )

        # 5. CORNER 3 (Scegli Cedola) - Posizione 20
        corner3 = Cell(..., CHOOSE_STOCK_TYPE, ...)

        # 6. LATO SUPERIORE (Posizioni 21-29)
        curr_x, curr_y, position = self.create_side(
            curr_x, curr_y,
            ["RED", "BLUE"],
            self.eventImage,
            self.chanceImage,
            CHANCE_TYPE,
            position
        )

        # 7. CORNER 4 (600 Scudi) - Posizione 30
        corner4 = Cell(..., SIX_HUNDRED_TYPE, ...)

        # 8. LATO DESTRO (Posizioni 31-39)
        curr_x, curr_y, position = self.create_side(
            curr_x, curr_y,
            ["YELLOW", "PURPLE"],
            self.eventImage,
            self.quotationImage,
            QUOTATION_TYPE,
            position
        )
```

### Metodo create_side()

Ogni lato è composto da **9 celle** con pattern fisso:

```python
def create_side(self, curr_x, curr_y, colors, eventImage, centralImage, centralType, position):
    # Pattern per ogni lato (9 celle):
    # [0] Cedola colore 1
    # [1] Cedola colore 1
    # [2] EVENTO
    # [3] Cedola colore 1
    # [4] CELLA CENTRALE (FREE_STOP/QUOTATION/CHANCE)
    # [5] Cedola colore 2
    # [6] EVENTO
    # [7] Cedola colore 2
    # [8] Cedola colore 2

    for i in range(0, 9):
        x, y = Board.compute_next_coord(x, y, CELLS_DEF[colors[0]]['side'])
        position += 1

        if i == 2 or i == 6:
            # Celle EVENTO
            cell = Cell(None, EVENTS_TYPE, x, y, None, eventImage, ...)
        elif i == 4:
            # Cella CENTRALE
            cell = Cell(None, centralType, x, y, None, centralImage, ...)
        elif i < 4:
            # Prime 3 cedole (colore 1)
            cellDef = CELLS_DEF[colors[0]]
            cell = Cell(cellDef, STOCKS_TYPE, x, y, logos.pop(0), ...)
        else:
            # Ultime 3 cedole (colore 2)
            cellDef = CELLS_DEF[colors[1]]
            cell = Cell(cellDef, STOCKS_TYPE, x, y, logos.pop(0), ...)

        self.__cells.append(cell)
```

### Caricamento Asset Eventi

Gli eventi sono caricati **dinamicamente** dal nome del file tramite parsing automatico.

#### Sistema di Nomenclatura Eventi

I file in `assets/events/` seguono una **nomenclatura strutturata** che codifica il tipo e i parametri:

```python
@staticmethod
def initialize_events():
    events = []
    files = os.listdir(EVENTS_DIR)  # assets/events/

    for fileName in files:
        image = pygame.image.load(EVENTS_DIR + fileName)
        image = pygame.transform.scale(image, (EVENT_WIDTH, EVENT_HEIGHT))

        # PARSING DEL NOME FILE
        eventType, effectData = Event.parse_name(fileName)

        events.append(Event(image, eventType, effectData))

    return events
```

#### Pattern di Nomenclatura

Il metodo `parse_name()` riconosce questi pattern:

##### 1. Eventi Colore
**Pattern**: `color_{colore}_{importo}.png`

```
Esempi:
- color_blue_70.png       → COLOR_EVENT, {'color': 'BLUE', 'amount': 70}
- color_red_60.png        → COLOR_EVENT, {'color': 'RED', 'amount': 60}
- color_light_30.png      → COLOR_EVENT, {'color': 'LIGHT_BLUE', 'amount': 30}
```

**Logica**:
```python
if 'color' in actionsAndValues:
    color = actionsAndValues[1]
    if color == "light":
        color = "LIGHT_BLUE"
    else:
        color = color.upper()

    effectData = {'color': color, 'amount': int(actionsAndValues[2])}
```

##### 2. Eventi GET (Ricevi Denaro)
**Pattern**: `get_{importo}[_from_{da_chi}].png`

```
Esempi:
- get_200.png             → GET_EVENT, {'amount': 200}
- get_300_2.png           → GET_EVENT, {'amount': 300}  (suffisso ignorato)
- get_100_from_others.png → GET_EVENT, {'amount': 100, 'from': 'others'}
```

**Logica**:
```python
if actionsAndValues[0] == 'get':
    if 'from' in actionsAndValues:
        fromIndex = actionsAndValues.index('from')
        fromValue = actionsAndValues[fromIndex+1]
        effectData = {'amount': int(actionsAndValues[1]), 'from': fromValue}
    else:
        effectData = {'amount': int(actionsAndValues[1])}
```

##### 3. Eventi PAY (Paga Denaro)
**Pattern**: `pay_{importo}[_to_{a_chi}].png`

```
Esempi:
- pay_150.png             → PAY_EVENT, {'amount': 150}
- pay_50_to_others.png    → PAY_EVENT, {'amount': 50, 'to': 'others'}
```

##### 4. Eventi GO (Vai a Cella)
**Pattern**: `go_{posizione}[_opzioni].png`

**Opzioni disponibili**:
- `get_{importo}` - ricevi denaro
- `pass_{importo}` - ricevi denaro per ogni giocatore superato
- `ifstart` - controlla se passi dal Via
- `someone` - porta un altro giocatore con te
- `buy` - compra la cedola (o contratta)
- `possiblebuy` - abilita bottone compra se disponibile

```
Esempi:
- go_0_get_300.png              → {'destination': 0, 'get': 300, 'pass': None, 'startCheck': False, 'someone': False, 'buy': False, 'possibleBuy': False}
- go_0_pass_100.png             → {'destination': 0, 'pass': 100, ...}
- go_11_ifstart.png             → {'destination': 11, 'startCheck': True, ...}
- go_31_with_someone.png        → {'destination': 31, 'someone': True, ...}
- go_8_buy_or_negotiate.png     → {'destination': 8, 'buy': True, ...}
- go_32_possiblebuy.png         → {'destination': 32, 'possibleBuy': True, ...}
- go_34_pass_80_ifstart.png     → {'destination': 34, 'pass': 80, 'startCheck': True, ...}
```

**Logica**:
```python
if actionsAndValues[0] == 'go':
    goValue = int(actionsAndValues[1])
    startCheck = 'ifstart' in actionsAndValues
    someone = 'someone' in actionsAndValues
    buy = 'buy' in actionsAndValues
    possibleBuy = 'possiblebuy' in actionsAndValues

    getValue = None
    if 'get' in actionsAndValues:
        get_index = actionsAndValues.index('get')
        getValue = int(actionsAndValues[get_index+1])

    passValue = None
    if 'pass' in actionsAndValues:
        passIndex = actionsAndValues.index('pass')
        passValue = int(actionsAndValues[passIndex+1])

    effectData = {
        'destination': goValue,
        'get': getValue,
        'pass': passValue,
        'startCheck': startCheck,
        'someone': someone,
        'buy': buy,
        'possibleBuy': possibleBuy
    }
```

##### 5. Eventi OWN (Possiedi Cedola)
**Pattern**: `own_{nome_azienda}[_get_{importo}][_each][_others_pay_{importo}].png`

```
Esempi:
- own_cuore_get_200_others_pay_50.png    → {'stockName': 'cuore', 'getAmount': 200, 'each': False, 'othersPayValue': 50}
- own_pepsi_get_200_each.png             → {'stockName': 'pepsi', 'getAmount': 200, 'each': True, 'othersPayValue': None}
- own_gled_get_200.png                   → {'stockName': 'gled', 'getAmount': 200, 'each': False, 'othersPayValue': None}
```

##### 6. Eventi BUY (Compra Cedola Specifica)
**Pattern**: `buy_{posizione}[_or_negotiate].png`

```
Esempi:
- buy_36_or_negotiate.png → {'stockIndex': 36, 'negotiate': True}
```

##### 7. Eventi Semplici (Nome Fisso)
```
- buy_what_you_want.png          → BUY_ANTHING_EVENT
- stop_1.png                     → STOP_1
- free_penalty.png               → FREE_PENALTY
- free_penalty_martini.png       → FREE_PENALTY_MARTINI
- everyone_50_per_point.png      → EVERYONE_FIFTY_EVENT
- player-1_go_39_get_penalty.png → PREVIOUS_PLAYER_GALUP
- player+1_pay_200.png           → NEXT_PLAYER_PAY
```

##### 8. Eventi GIFT (Regalo)
**Pattern**: `gift_{posizione_cedola}_or_get_{importo}.png`

```
Esempi:
- gift_22_or_get_500.png → {'stockIndex': 22, 'amount': 500}
```

**Logica**: Se la cedola non è disponibile, ricevi l'importo dalla riserva di piazza.

### Vantaggi del Sistema a Nomenclatura

1. **Espandibilità**: Aggiungere eventi è semplice come creare un PNG con nome appropriato
2. **Nessun file di configurazione**: La logica è codificata nel nome
3. **Eventi multipli simili**: Suffissi `_2`, `_3` permettono eventi con stesso effetto ma grafica diversa
4. **Parsing robusto**: Il sistema usa split su `_` e cerca keyword specifiche

### Creazione di Cell e Stock

Quando una cella viene creata, genera automaticamente **2 cedole** identiche:

```python
class Cell:
    def __init__(self, cellDef, cellType, ...):
        if cellDef is not None:
            self.__stocks = []
            for _ in range(0, 2):
                self.__stocks.append(
                    Stock(cellDef, position, name, logo_path, enableGraphics)
                )
```

Ogni `Stock` contiene:
- **Valore base** (`__original_value`)
- **Valore corrente** (`__new_value`) - aggiornato dalla QUOTATION
- **Penalità** (`__penalties`) - array di 6 valori
- **Proprietario** (`__owner`)
- **Grafica** (logo, superficie pygame)

### Sistema di Quotazione

Durante la QUOTATION, i valori delle cedole cambiano:

```python
# In constants.py
QUOTATION = [
    {'index': 0, 'quotation': 0.80},   # ORANGE -20%
    {'index': 1, 'quotation': 1.20},   # LIGHT_BLUE +20%
    {'index': 2, 'quotation': 0.90},   # PINK -10%
    ...
]

# In gameLogic.py
def quotation_logic(players, board, new_quotation, game):
    current_quotation = new_quotation[0]  # Primo della coda
    new_quotation.rotate(-1)  # Ruota coda

    # Applica quotazione a tutte le cedole del colore
    for cell in board.get_cells():
        if cell.get_stocks() and cell.get_index() == current_quotation['index']:
            new_value = int(cell.get_cell_value() * current_quotation['quotation'])
            cell.updateCellValue(new_value)

            # Aggiorna anche le cedole dei giocatori
            for player in players:
                for stock in player.get_stocks():
                    if stock.get_position() == cell.get_position():
                        stock.update_value(new_value)
```

Le **penalità vengono ricalcolate proporzionalmente**:

```python
def update_penalties(self):
    self.__new_penalties = []
    for penalty in self.__penalties:
        # Mantieni la proporzione: (penalty / valore_originale) * valore_nuovo
        new_penalty = int(round((penalty / self.__original_value) * self.__new_value))
        self.__new_penalties.append(new_penalty)
```

---

## Gestione Eventi Pygame

### Event Loop Principale

Il game loop si trova in `Game.start()` e segue questo pattern:

```python
while self.running:
    self.clock.tick(FPS)

    # Bot AI (se il giocatore corrente è un bot)
    if self.__players[self.__current_player_index].get_is_bot():
        self.__bot.play()

    # Gestione eventi pygame
    for event in pygame.event.get():
        self.manage_events(event)              # Eventi di gioco
        self.__gameUI.manager.process_events(event)  # Eventi pygame_gui

    # Mostra pannelli in coda
    if len(self.panels_to_show) > 0 or len(self.__alert_messages) > 0:
        self.draw_window()
        self.update_graphic()
```

### Metodo `manage_events()`

Il metodo `manage_events()` in [game.py:273-438](lib/game.py#L273-L438) è il **cuore della gestione eventi**:

```python
def manage_events(self, event):
    curr_player = self.__players[self.__current_player_index]

    if event.type == pygame.QUIT:
        self.running = False

    elif event.type == pygame_gui.UI_BUTTON_PRESSED:
        # Gestione bottoni UI principale
        if event.ui_element == self.__gameUI.launchDice:
            self.turn()
        elif event.ui_element == self.__gameUI.buyButton:
            buy_stock_from_cell(...)
        elif event.ui_element == self.__gameUI.passButton:
            # Passa turno

        # Gestione bottoni dei pannelli attivi
        elif hasattr(self.current_panel, "eventBut") and event.ui_element == self.current_panel.eventBut:
            self.events_logic(curr_player)
            self.current_panel.close_ui()

        # Delega al pannello corrente
        elif self.current_panel is not None:
            self.current_panel.manage_events(event, self.get_players(), curr_player)

    # Eventi dropdown/text entry delegati al pannello
    elif event.type in [pygame_gui.UI_DROP_DOWN_MENU_CHANGED,
                        pygame_gui.UI_TEXT_ENTRY_CHANGED]:
        if self.current_panel is not None:
            self.current_panel.manage_events(event, ...)
```

### Tipi di Eventi Gestiti

| Tipo Evento | Dove Gestito | Scopo |
|-------------|--------------|-------|
| `pygame.QUIT` | `Game.manage_events()` | Chiusura gioco |
| `UI_BUTTON_PRESSED` | `Game.manage_events()` → delegato a pannelli | Click su bottoni |
| `UI_DROP_DOWN_MENU_CHANGED` | Delegato a pannelli (es. BargainUI) | Selezione dropdown |
| `UI_TEXT_ENTRY_CHANGED` | Delegato a pannelli (es. BargainUI) | Modifica testo |
| `pygame.KEYDOWN` | `Game.manage_events()` | Modalità test (input dadi) |

### Pattern di Delega

Gli eventi seguono un pattern a **cascata**:

```
pygame.event.get()
    ↓
Game.manage_events(event)
    ↓
[Controllo evento su UI principale]
    ↓ (se non gestito)
[Controllo evento su current_panel]
    ↓
current_panel.manage_events(event, players, curr_player)
```

Ogni `UIComponent` implementa il proprio metodo `manage_events()` per gestire i propri bottoni/controlli.

---

## Sistema di Pannelli e Finestre

### Code di Pannelli e Alert

Il gioco utilizza **due code separate** per gestire l'ordine di visualizzazione:

```python
# In Game.__init__()
self.__alert_messages = []      # Coda di messaggi alert
self.current_panel = None       # Pannello attualmente visualizzato
self.panels_to_show = []        # Coda di pannelli da mostrare
```

### Meccanismo di Visualizzazione

Il metodo `draw_window()` in [game.py:193-201](lib/game.py#L193-L201) gestisce la coda:

```python
def draw_window(self):
    # Priorità agli alert
    if len(self.__alert_messages) > 0:
        self.__gameUI.drawAlert(self.__alert_messages.pop(0))
        self.current_panel = self.__gameUI.alertUi

    # Se non c'è pannello corrente, prendi il prossimo dalla coda
    if self.current_panel is None:
        self.current_panel = self.panels_to_show.pop(0)
        self.current_panel.draw()
```

### Flusso di Aggiunta Pannelli

Quando serve mostrare un pannello:

```python
# Esempio: mostrare evento
self.panels_to_show.append(EventUI(self.events[0], self.__gameUI.manager))
self.disable_actions()  # Disabilita azioni durante il pannello

# Esempio: mostrare alert
self.__alert_messages.append("Doppio e incidente!")

# Nel game loop, draw_window() verrà chiamato e mostrerà il pannello
```

### Ciclo di Vita di un Pannello

```
1. CREAZIONE
   panel = EventUI(...)

2. AGGIUNTA ALLA CODA
   self.panels_to_show.append(panel)

3. VISUALIZZAZIONE
   draw_window() → panel.draw()
   self.current_panel = panel

4. INTERAZIONE UTENTE
   manage_events() → panel.manage_events()

5. CHIUSURA
   panel.close_ui()
   self.current_panel = None
   self.renable_actions()
```

### Ordine di Priorità

1. **Alert messages** (priorità massima)
2. **Pannelli in coda** (`panels_to_show`)
3. **UI principale** (quando nessun pannello è attivo)

### Esempio: Cella Quotazione

Quando un giocatore capita sulla cella QUOTATION:

```python
def special_cell_logic(self, cell, player):
    if cell.cellType == QUOTATION_TYPE:
        quotation_logic(...)  # Aggiorna valori cedole

        # Crea panel per ogni giocatore con cedole
        for player in self.get_players():
            if len(player.get_stocks()) > 0:
                # Aggiungi alla coda
                self.panels_to_show.append(
                    ShowStockUI(self, player.get_stocks(), "STOCK_TO_AUCTION", player)
                )

        self.disable_actions()
```

I pannelli verranno mostrati **uno alla volta** nell'ordine in cui sono stati aggiunti.

---

## UIComponents Principali

### 1. EventUI - Pannello Eventi

**File**: [lib/uiComponents/eventUI.py](lib/uiComponents/eventUI.py)

Mostra un evento casuale pescato dalla coda eventi.

```python
class EventUI:
    def __init__(self, event, manager):
        self.showed_event = event  # Evento da mostrare

    def draw(self):
        # Crea panel con:
        # - Titolo "EVENTI"
        # - Immagine evento
        # - Bottone "OK"

    def manage_events(self, event, players, curr_player):
        # Stub - gestione diretta in Game.manage_events()
```

**Interazione**:
- L'utente clicca "OK"
- `Game.manage_events()` intercetta il click
- Chiama `events_logic(curr_player)` per applicare l'effetto
- Chiude il pannello

### 2. BargainUI - Contrattazioni

**File**: [lib/uiComponents/bargainUI.py](lib/uiComponents/bargainUI.py)

Permette al giocatore corrente di scambiare cedole e denaro con altri giocatori.

```python
class BargainUI:
    def __init__(self, manager, screen, current_player, other_players, game):
        self.__player = current_player
        self.__other_players = other_players
        self.stocks_given = []      # Cedole date
        self.stocks_got = []        # Cedole ricevute
        self.exchange_values = []   # Denaro scambiato per giocatore
        self.exchange_direction = [] # "Dai" o "Ricevi" per giocatore
```

**Componenti UI**:
- **Selection List 1**: Cedole del giocatore corrente
- **Selection List 2**: Cedole del giocatore selezionato
- **Dropdown**: Selezione giocatore da contrattare
- **Text Entry**: Quantità denaro da scambiare
- **Dropdown Dai/Ricevi**: Direzione dello scambio
- **Selection List Scambi**: Lista scambi aggiunti
- **Bottoni**: Aggiungi scambio, Rimuovi scambio, Contratta, Chiudi

**Flusso**:
1. Giocatore seleziona cedole da entrambe le liste
2. Clicca "Aggiungi scambio" → aggiunto a `bargains_selection_list`
3. Imposta denaro e direzione (Dai/Ricevi)
4. Ripete per altri giocatori (cambiando dal dropdown)
5. Clicca "Contratta" → `process_bargains()` esegue tutti i trasferimenti

**Gestione Eventi**:
```python
def manage_events(self, event, players, current_player):
    if event.ui_element == self.player_selector:
        # Cambia giocatore visualizzato
        self.update_stocks()

    elif event.ui_element == self.add_bargain_butt:
        # Aggiungi scambio alla lista
        self.add_bargains()

    elif event.ui_element == self.bargain_butt:
        # Esegui tutti gli scambi
        self.process_bargains()
        self.close_ui()
```

**Validazione Denaro**:
- Controlla che il giocatore abbia abbastanza denaro per "Dai"
- Controlla che l'altro giocatore abbia abbastanza denaro per "Ricevi"
- Calcola `virtual_balance` considerando tutti gli scambi pianificati

### 3. Auction - Aste

**File**: [lib/auction.py](lib/auction.py)

Sistema d'asta per cedole messe all'asta durante la QUOTATION o bancarotta.

```python
class Auction:
    def __init__(self, manager, screen, owner, bidders, stock, board, game, game_ui):
        self.__owner = owner           # Chi mette all'asta
        self.__bidders = bidders       # Lista offerenti
        self.__stock = stock           # Cedola in asta
        self.bids = [0] * len(bidders) # Offerte per ogni bidder
        self.current_bidder = 0        # Indice bidder corrente
        self.__winner = None
```

**Meccanica**:
1. Ogni bidder può:
   - **OFFRI**: Fare un'offerta (almeno 10 scudi in più dell'offerta massima)
   - **PASSA**: Passare il turno al prossimo bidder
   - **RITIRATI**: Ritirarsi dall'asta

2. L'offerta viene arrotondata a multipli di 10

3. I bidder che non hanno abbastanza denaro vengono rimossi automaticamente

4. L'asta termina quando:
   - Rimane un solo bidder (vince)
   - Tutti i bidder si ritirano (cedola va alla banca)

**Gestione Multiple Aste**:
```python
# In Game
self.__auctions = []  # Coda di aste

def start_first_auction(self):
    self.currentAuction = self.__auctions.pop(0)

    if len(self.currentAuction.get_bidders()) >= 2:
        # Asta normale
        self.panels_to_show.append(self.currentAuction)
    else:
        # Un solo bidder → pannello acquisto diretto
        self.panels_to_show.append(
            ShowStockUI(..., "BUY_AUCTIONED_STOCK", ...)
        )
```

Quando un'asta finisce, `open_next_if_present()` controlla se ci sono altre aste in coda.

### 4. ShowStockUI - Visualizzazione Cedole

**File**: [lib/uiComponents/showStockUI.py](lib/uiComponents/showStockUI.py)

**Pannello multiuso** per mostrare cedole con azioni diverse basate sul tipo.

```python
class ShowStockUI:
    def __init__(self, game, stocks, panel_type, player=None, title=None):
        self.type = panel_type  # Determina quale UI mostrare
```

**Tipi di Panel**:

| Tipo | Scopo | Bottoni |
|------|-------|---------|
| `SHOW_STOCKS` | Visualizza cedole giocatore | X (chiudi) |
| `BUY_ANYTHING` | Compra qualsiasi cedola (evento) | Compra quale vuoi |
| `STOCK_TO_AUCTION` | Scegli cedola da mettere all'asta | Metti all'asta |
| `SHOW_CHOOSE_STOCK` | Scegli cedola da comprare | Scegli |
| `BUY_AUCTIONED_STOCK` | Compra cedola asta (1 bidder) | Compra / Lascia |
| `BANKRUPT_STOCK` | Gestione bancarotta | Metti all'asta / Lascia alla banca |
| `MOVE_TO_STOCK` | Scegli cedola dove muoverti | Scegli |

**Navigazione Cedole**:
- Bottoni `<` e `>` per scorrere le cedole
- `showedStock` tiene traccia dell'indice corrente
- `stockImage` viene aggiornato dinamicamente

**Esempio - Bancarotta**:
```python
if curr_player.is_in_debt():
    if len(curr_player.get_stocks()) > 0:
        # Mostra panel per vendere/mettere all'asta
        self.showStockUI = ShowStockUI(
            self, curr_player.get_stocks(),
            "BANKRUPT_STOCK",
            curr_player
        )
        self.panels_to_show.append(self.showStockUI)
```

### 5. DiceOverlay - Overlay Lancio Dadi

**File**: [lib/uiComponents/diceOverlayUI.py](lib/uiComponents/diceOverlayUI.py)

Overlay **multiuso** per il lancio di dadi in contesti diversi.

```python
class DiceOverlay:
    def __init__(self, game, message, title, actions_status,
                 twoDices=True, establishing_players_order=True,
                 color_event=False):
        self.__establishing_players_order = establishing_players_order
        self.color_event = color_event
        self.twoDices = twoDices  # Uno o due dadi
```

**Contesti di Utilizzo**:

1. **Ordine Turni** (inizio partita):
   - Ogni giocatore lancia 2 dadi
   - Chi fa il punteggio più alto inizia
   - Gestisce parità con secondo round

2. **Riserva Monetaria** (cella CHANCE):
   - Lancia 2 dadi
   - Logica: vince/perde denaro in base al risultato

3. **Evento Colore**:
   - Lancia **1 solo dado**
   - Importo = cedole_colore × amount × dado

**Logica Ordine Turni**:
```python
def establish_players_order(self):
    self.roll_dice()
    if diceSum > self.__highestScore:
        self.__who_will_start = current_player_index
        self.__highestScore = diceSum
    elif diceSum == self.__highestScore:
        # Parità → secondo round
        self.__second_round_who_start.append(...)
```

**Gestione Evento Colore**:
```python
def launch_but_pressed(self):
    if self.color_event:
        score = roll()
        self.updateDiceOverlay(score)
        # Usa solo il primo dado
        self.__game.handle_color_event(score[0])
```

### 6. GameUI - UI Principale

**File**: [lib/uiComponents/gameUI.py](lib/uiComponents/gameUI.py)

Gestisce tutti gli elementi UI fissi del gioco.

**Componenti**:

1. **Leaderboard** (sinistra):
   - Turno corrente
   - Riserva di piazza
   - Lista giocatori con scudi e valore cedole

2. **Pannello Azioni** (in basso a sinistra):
   - Lancia i dadi
   - Compra
   - Mostra Cedole
   - Passa il turno
   - Salva partita
   - Abbandona

3. **Dadi** (in basso):
   - Visualizzazione risultato lancio

4. **Stockboard** (destra):
   - Cedole possedute da ogni giocatore

**Abilitazione/Disabilitazione Bottoni**:
```python
def renable_actions(self):
    actions_status = self.__actions_status.get_actions_status()
    for index, action in enumerate(self.actions):
        if actions_status[index]:
            action.enable()
        else:
            action.disable()
```

Lo stato viene gestito da `ActionsStatus`:
```python
class ActionsStatus:
    def __init__(self):
        self.__throw_dices = True
        self.__buy_property = False
        self.__show_stock = False
        self.__pass_turn = False
        self.__save_game = True
        self.__quit_game = True
```

---

## Game Logic

### Gestione Cedole

#### Trasferimento Cedole

```python
def transfer_stock(board, new_owner, stock, enable_buy_button=False):
    """Trasferisce una cedola da un proprietario a un altro"""
    old_owner = stock.get_owner()

    if old_owner is not None:
        old_owner.remove_stock(stock)

    if board is not None:
        # Rimuove dalla cella
        board.get_cell(stock.get_position()).remove_stock(stock)

    # Aggiunge al nuovo proprietario
    stock.set_owner(new_owner)
    new_owner.add_stock(stock)
    new_owner.change_balance(-stock.get_stock_value())
```

#### Acquisto da Cella

```python
def buy_stock_from_cell(cells, player, position=None):
    """Compra una cedola dalla cella corrente"""
    curr_pos = position or player.get_position()

    if cells[curr_pos].get_stocks() is None:
        return

    stock_value = cells[curr_pos].get_stocks()[0].get_stock_value()

    if player.get_balance() >= stock_value:
        stock = cells[curr_pos].sell_stock()
        stock.set_owner(player)
        player.change_balance(-stock_value)
        player.add_stock(stock)
    else:
        # Debito
        player.set_in_debt_with("BANK")
        player.add_debt(stock_value)
```

### Sistema Penalità

Le penalità vengono pagate quando si capita su una cedola altrui.

```python
def check_for_penalty(cells, players, player_number):
    current_player = players[player_number]
    cell = cells[current_player.get_position()]

    # 1. Controlla se il giocatore possiede la cedola
    own_by_the_player = any(
        stock.get_position() == cell.get_position()
        for stock in current_player.get_stocks()
    )

    # 2. Controlla esenzioni
    if current_player.get_free_penalty():
        current_player.set_free_penalty(False)
        return "FREE"

    # 3. Trova proprietario e calcola penalità
    if not own_by_the_player:
        for player in players:
            for stock in player.get_stocks():
                if cell.get_position() == stock.get_position():
                    penalty = player.compute_penalty(stock)

                    if current_player.get_balance() < penalty:
                        # Debito
                        current_player.set_in_debt_with(player)
                        current_player.add_debt(penalty)
                    else:
                        current_player.change_balance(-penalty)
                        player.change_balance(penalty)
                    break
```

#### Calcolo Penalità

La penalità dipende dal **numero di cedole dello stesso colore**:

```python
def compute_penalty(self, choosen_stock):
    same_color_cells = self.same_color_count(choosen_stock.color)

    if same_color_cells >= 3:
        # Usa l'indice corrispondente nell'array penalty
        penalty_index = min(same_color_cells - 1, len(choosen_stock.get_penalty()) - 1)
        return choosen_stock.get_penalty()[penalty_index]

    elif same_color_cells == 2:
        # Controlla se possiede 2 cedole della stessa AZIENDA
        # Se sì → penalty[1], altrimenti penalty[0]
        ...

    return choosen_stock.get_penalty()[0]  # Una sola cedola
```

### Bancarotta

#### Rilevamento Debito

```python
class Player:
    def is_in_debt(self):
        return len(self.__debts) > 0

    def set_in_debt_with(self, creditor):
        if self.__in_debt_with is None:
            self.__in_debt_with = []
        self.__in_debt_with.append(creditor)

    def add_debt(self, debt):
        self.__debts.append(debt)
```

#### Gestione Bancarotta

Quando un giocatore va in debito:

```python
def is_debt_solved(self, player):
    if player.is_in_debt():
        if len(player.get_stocks()) > 0:
            # Mostra UI per vendere cedole
            self.showStockUI = ShowStockUI(
                self, player.get_stocks(),
                "BANKRUPT_STOCK", player
            )
            self.panels_to_show.append(self.showStockUI)
        else:
            # Nessuna cedola → elimina giocatore
            solve_larger_debts(player, self)
            self.kill_player(player)
    else:
        # Debito risolto
        solve_bankrupt(player, self)
```

#### Risoluzione Debiti

```python
def solve_larger_debts(debtor, game):
    """Risolve i debiti dal più grande al più piccolo"""
    # Ordina debiti per importo decrescente
    sorted_debts = sorted(
        zip(debtor.get_in_debt_with(), debtor.get_debts()),
        key=lambda x: x[1], reverse=True
    )

    for creditor, debt in sorted_debts:
        if debtor.get_balance() > debt:
            # Paga il debito
            debtor.change_balance(-debt)
            if creditor == "BANK":
                pass  # Denaro perso
            elif creditor == "SQUARE":
                game.set_square_balance(debt)
            else:
                creditor.change_balance(debt)
```

#### Eliminazione Giocatore

```python
def kill_player(self, player):
    removed_player_index = self.__players.index(player)
    self.__players.remove(player)

    # Aggiusta current_player_index
    if removed_player_index < self.__current_player_index:
        self.__current_player_index -= 1
    elif removed_player_index == self.__current_player_index:
        if self.__current_player_index >= len(self.__players):
            self.__current_player_index = 0

    if len(self.get_players()) == 1:
        # Vittoria!
        self.__alert_messages.append(
            self.get_players()[0].get_name() + " ha vinto la partita!"
        )
```

### Eventi

Gli eventi sono gestiti dal metodo `events_logic()` in [game.py:591-716](lib/game.py#L591-L716).

#### Tipi di Eventi

| Tipo | Effetto |
|------|---------|
| `COLOR_EVENT` | Lancia 1 dado, vinci/perdi denaro in base a cedole di quel colore |
| `BUY_ANTHING_EVENT` | Compra qualsiasi cedola (anche occupata) |
| `STOP_1` | Salta un turno |
| `FREE_PENALTY` | Esenzione penalità |
| `FREE_PENALTY_MARTINI` | Esenzione penalità martini (cella 38) |
| `EVERYONE_FIFTY_EVENT` | Tutti i giocatori ricevono 50 scudi |
| `PREVIOUS_PLAYER_GALUP` | Giocatore precedente va alla cella 39 e paga |
| `NEXT_PLAYER_PAY` | Giocatore successivo paga 200 scudi |
| `GIFT_EVENT` | Ricevi cedola gratis o denaro dalla piazza |
| `GET_EVENT` | Ricevi denaro (da banca o da altri) |
| `GO_EVENT` | Vai a una cella specifica (con opzioni) |
| `PAY_EVENT` | Paga denaro (a banca o ad altri) |
| `OWN_EVENT` | Chi possiede certe cedole riceve/paga |
| `BUY_EVENT` | Compra cedola specifica (o contratta se occupata) |

#### Evento Colore (Dettaglio)

```python
def handle_color_event(self, single_dice_score):
    event = self.events[-1]  # Ultimo evento (già ruotato)
    amount = event.effectData['amount']
    current_player = self.__players[self.__current_player_index]

    stock_color_count = current_player.same_color_count(
        event.effectData['color']
    )

    # Usa il tiro PRECEDENTE (per muoversi) per determinare vittoria
    previous_turn_score = self.__last_turn_dice_score

    total_amount = stock_color_count * amount * single_dice_score

    if previous_turn_score >= 8:
        # VINCI
        current_player.change_balance(total_amount)
    else:
        # PERDI
        current_player.change_balance(-total_amount)
```

#### Rotazione Eventi

Gli eventi sono in una **coda circolare**:

```python
self.events = deque(events)
random.shuffle(self.events)

# Dopo aver applicato un evento
self.events.rotate(-1)  # Sposta in fondo
```

---

## Flusso di Gioco

### Inizializzazione

```
1. Creazione Game
   └─ Inizializza giocatori, eventi, board, UI

2. init_graphics()
   └─ Disegna board, dadi, leaderboard, stockboard

3. DiceOverlay per ordine turni
   └─ Ogni giocatore lancia i dadi
   └─ Determina chi inizia

4. start() → Game Loop
```

### Turno di Gioco

```
1. LANCIO DADI
   └─ self.turn()

2. MOVIMENTO
   └─ curr_player.move(dice_sum)

3. CONTROLLI
   └─ check_turn() → incidenti
   └─ check_crash() → altri giocatori sulla stessa cella

4. LOGICA CELLA
   ├─ STOCKS_TYPE → abilita "Compra" + penalità
   ├─ EVENTS_TYPE → mostra EventUI
   ├─ QUOTATION_TYPE → aggiorna valori + aste
   ├─ CHOOSE_STOCK_TYPE → scegli dove muoverti
   ├─ FREE_STOP_TYPE → compra cedola disponibile
   ├─ CHANCE_TYPE → lancia dadi per denaro
   └─ ...altri tipi

5. BANCAROTTA
   └─ Se in debito → ShowStockUI (vendi/asta)

6. PASSA TURNO
   └─ Prossimo giocatore
```

### Ciclo QUOTATION

```
1. Giocatore capita su QUOTATION

2. quotation_logic()
   └─ Aggiorna valori cedole con nuova quotazione

3. Per ogni giocatore con cedole:
   └─ panels_to_show.append(ShowStockUI "STOCK_TO_AUCTION")

4. Ogni giocatore sceglie una cedola da mettere all'asta
   └─ add_auction(player, stock)

5. start_first_auction()
   ├─ Se >= 2 bidder → mostra Auction
   └─ Se 1 bidder → ShowStockUI "BUY_AUCTIONED_STOCK"

6. Asta termina
   └─ open_next_if_present() → prossima asta o fine
```

### Stato Bottoni

```
ActionsStatus controlla abilitazione:

┌─────────────────┬──────────┬─────────┬──────────┬──────────┐
│ Stato           │ Lancia   │ Compra  │ Mostra   │ Passa    │
│                 │ Dadi     │         │ Cedole   │ Turno    │
├─────────────────┼──────────┼─────────┼──────────┼──────────┤
│ Inizio turno    │ ✓        │ ✗       │ ✓*       │ ✗        │
│ Dopo lancio     │ ✗        │ ✓**     │ ✓*       │ ✓        │
│ Tiro doppio     │ ✓        │ ✓**     │ ✓*       │ ✗        │
│ Panel aperto    │ ✗        │ ✗       │ ✗        │ ✗        │
└─────────────────┴──────────┴─────────┴──────────┴──────────┘

* Se ha cedole
** Se può comprare cedola corrente
```

---

## Esempi Completi

### Esempio 1: Turno Completo con Tutti i Dettagli

Scenario: Il giocatore Mario (posizione 8) lancia i dadi e ottiene 5. Capita sulla cella 13 (PINK - evento).

```python
# ========== FASE 1: CLICK SU "LANCIA DADI" ==========
# File: game.py, manage_events()

def manage_events(self, event):
    if event.ui_element == self.__gameUI.launchDice:
        self.turn()  # ← Chiamata

# ========== FASE 2: TURNO ==========
# File: game.py, turn()

def turn(self):
    # 1. Disabilita "Lancia Dadi", abilita "Passa Turno"
    self.__actions_status.set_throw_dices(False)
    self.__actions_status.set_pass_turn(True)

    # 2. Lancia dadi
    score = roll(self.__test, self.__test_dice)  # → (2, 3)
    self.__last_turn_dice_score = sum(score)     # → 5
    self.__gameUI.update_dice(score)             # Aggiorna grafica

    # 3. Controlla doppio
    if is_double(score):  # False (2 ≠ 3)
        tiro_doppio = False

    # 4. Muovi giocatore
    curr_player = self.__players[self.__current_player_index]  # Mario
    curr_player.move(5)  # 8 + 5 = 13
    # ↓ Player.move()
    #   self.__old_position = 8
    #   self.__position = 13

    # 5. Ottieni cella
    cell = self.__board.get_cells()[13]  # Cella PINK

    # 6. Controlla incidenti e crash
    check_turn(curr_player)
    # ↓ gameLogic.check_turn()
    #   Verifica se posizione == vecchia posizione
    #   Se sì: penalità 300 scudi

    crash = check_crash(self.get_players(), self.__current_player_index)
    # ↓ gameLogic.check_crash()
    #   for player in players:
    #       if player.get_position() == 13 and player != Mario:
    #           crash += 1
    #           player.change_balance(100)
    #   curr_player.change_balance(-100 * crash)

    # 7. Logica cella
    if cell.cellType == EVENTS_TYPE:  # ✓ Cella 13 è EVENTI
        self.special_cell_logic(cell, curr_player)

# ========== FASE 3: LOGICA CELLA EVENTO ==========
# File: game.py, special_cell_logic()

def special_cell_logic(self, cell, player):
    if cell.cellType == EVENTS_TYPE:
        self.disable_actions()  # Disabilita tutti i bottoni
        # ↓ ActionsStatus.disable_actions()
        #   self.__throw_dices = False
        #   self.__buy_property = False
        #   self.__show_stock = False
        #   self.__pass_turn = False

        # Crea EventUI e aggiunge alla coda
        self.panels_to_show.append(
            EventUI(self.events[0], self.__gameUI.manager)
        )
        # ↓ EventUI.__init__()
        #   self.showed_event = self.events[0]
        #   # Es: GET_EVENT con {'amount': 200}

# ========== FASE 4: GAME LOOP - DRAW WINDOW ==========
# File: game.py, start() - game loop

while self.running:
    # ...eventi...

    if len(self.panels_to_show) > 0:  # ✓ 1 pannello in coda
        self.draw_window()

# ↓ draw_window()
def draw_window(self):
    if self.current_panel is None:  # ✓ Nessun pannello attivo
        self.current_panel = self.panels_to_show.pop(0)  # EventUI
        self.current_panel.draw()
        # ↓ EventUI.draw()
        #   - Crea UIPanel
        #   - Mostra immagine evento
        #   - Crea bottone "OK"

# ========== FASE 5: CLICK SU "OK" EVENTO ==========
# File: game.py, manage_events()

def manage_events(self, event):
    if (hasattr(self.current_panel, "eventBut") and
        event.ui_element == self.current_panel.eventBut):

        self.events_logic(curr_player)  # ← Applica effetto
        self.current_panel.close_ui()   # ← Chiude pannello
        # ↓ EventUI.close_ui()
        #   self.eventUi.kill()

        self.screen.fill(BLACK)
        self.__gameUI.draw_dices()
        self.__gameUI.updateAllPlayerLables(self.get_players())
        self.current_panel = None
        self.renable_actions()
        # ↓ ActionsStatus.renable_actions()
        #   Ripristina stato precedente

# ========== FASE 6: LOGICA EVENTO ==========
# File: game.py, events_logic()

def events_logic(self, player):
    event = self.events[0]

    if event.evenType == GET_EVENT:  # ✓
        effectData = event.effectData  # {'amount': 200}
        player.change_balance(200)
        # ↓ Player.change_balance()
        #   self.__balance += 200  # 3000 → 3200

    # Ruota eventi
    self.events.rotate(-1)
    # ↓ deque.rotate(-1)
    #   Sposta primo evento in fondo

# ========== FASE 7: AGGIORNAMENTO UI ==========
# File: game.py, dopo renable_actions()

# UI aggiorna leaderboard
self.__gameUI.updateAllPlayerLables(self.get_players())
# ↓ GameUI.updateAllPlayerLables()
#   for i, player in enumerate(sorted_players):
#       self.playerLabels[i].set_text(
#           "Mario (RED) : 3200 | 0"
#       )

# ========== FASE 8: PASSA TURNO ==========
# File: game.py, manage_events()

def manage_events(self, event):
    if event.ui_element == self.__gameUI.passButton:
        # Prossimo giocatore
        self.__current_player_index = (self.__current_player_index + 1) % len(self.get_players())
        # 0 → 1 (se 2+ giocatori)

        curr_player = self.__players[self.__current_player_index]
        self.set_skip_turn()  # Salta turni se necessario
        self.__gameUI.updateTurnLabel(curr_player)

        # Ripristina stato per nuovo turno
        self.__actions_status.set_throw_dices(True)
        self.__actions_status.set_pass_turn(False)
        self.__actions_status.set_buy_property(False)
        self.__actions_status.enable_show_stock(curr_player)
```

**Sequenza Completa delle Chiamate**:
```
1. manage_events() [event: UI_BUTTON_PRESSED, launchDice]
   └─> turn()
       ├─> roll() → (2, 3)
       ├─> curr_player.move(5)
       ├─> check_turn(curr_player)
       ├─> check_crash(...)
       └─> special_cell_logic(cell, curr_player)
           └─> panels_to_show.append(EventUI(...))

2. Game Loop: draw_window()
   └─> current_panel = panels_to_show.pop(0)
   └─> current_panel.draw()

3. manage_events() [event: UI_BUTTON_PRESSED, eventBut]
   ├─> events_logic(curr_player)
   │   ├─> player.change_balance(200)
   │   └─> events.rotate(-1)
   ├─> current_panel.close_ui()
   └─> renable_actions()

4. manage_events() [event: UI_BUTTON_PRESSED, passButton]
   ├─> __current_player_index++
   └─> set_throw_dices(True)
```

---

### Esempio 2: Banca Rotta Completa

Scenario: Luigi ha 150 scudi, capita sulla cedola di Mario e deve pagare 400 scudi di penalità. Ha 2 cedole (valore totale 600).

```python
# ========== FASE 1: PENALITÀ SUPERA BILANCIO ==========
# File: gameLogic.py, check_for_penalty()

def check_for_penalty(cells, players, player_number):
    current_player = players[player_number]  # Luigi, balance=150
    cell = cells[current_player.get_position()]

    for player in players:  # Mario
        for stock in player.get_stocks():
            if cell.get_position() == stock.get_position():
                penalty = player.compute_penalty(stock)  # 400

                if current_player.get_balance() < penalty:  # 150 < 400 ✓
                    # DEBITO!
                    current_player.set_in_debt_with(player)  # Mario
                    # ↓ Player.set_in_debt_with()
                    #   if self.__in_debt_with is None:
                    #       self.__in_debt_with = []
                    #   self.__in_debt_with.append(player)

                    current_player.add_debt(penalty)  # 400
                    # ↓ Player.add_debt()
                    #   self.__debts.append(400)
                    #   # self.__debts = [400]
                else:
                    # Paga normalmente
                    current_player.change_balance(-penalty)
                    player.change_balance(penalty)
                break

# ========== FASE 2: FINE TURNO - CONTROLLO DEBITO ==========
# File: game.py, turn()

def turn(self):
    # ... movimento, penalità, etc. ...

    # Dopo tutta la logica del turno
    if curr_player.is_in_debt():  # ✓ Luigi in debito
        # ↓ Player.is_in_debt()
        #   return len(self.__debts) > 0  # True

        if len(curr_player.get_stocks()) > 0:  # ✓ Ha 2 cedole
            # Mostra UI per vendere cedole
            self.showStockUI = ShowStockUI(
                self,
                curr_player.get_stocks(),  # [Stock1, Stock2]
                "BANKRUPT_STOCK",
                curr_player
            )
            self.panels_to_show.append(self.showStockUI)
        else:
            # Nessuna cedola → elimina giocatore
            self.is_debt_solved(curr_player)

# ========== FASE 3: MOSTRA PANEL BANKRUPT ==========
# Game Loop chiama draw_window() → ShowStockUI.draw()

# File: showStockUI.py, show_bankrupt_stock()
def show_bankrupt_stock(self):
    self.title = "Sei in banca rotta a vendi o metti all'asta?"
    self.draw_stock_ui(False)

    # Bottone "Metti all'asta"
    self.auction_bankrupt = UIButton(..., text="Metti all'asta")

    # Bottone "Lascia alla banca"
    self.leave_to_bank_bankrupt = UIButton(..., text="Lascia alla banca")

# ========== OPZIONE A: CLICK SU "LASCIA ALLA BANCA" ==========
# File: showStockUI.py, manage_events()

def manage_events(self, event, players, curr_player):
    if event.ui_element == self.leave_to_bank_bankrupt:
        # Vende cedola corrente alla banca
        sell_stock_to_bank(self.game.get_board(), self.get_showed_stock())
        # ↓ gameLogic.sell_stock_to_bank()
        #   stock = self.get_showed_stock()  # Stock1 (valore 300)
        #   owner = stock.get_owner()         # Luigi
        #   owner.remove_stock(stock)
        #   owner.change_balance(300 // 2)   # Luigi: 150 + 150 = 300
        #   stock.set_owner(None)
        #   board.get_cell(stock.get_position()).add_stock(stock)

        self.gameUI.updateAllPlayerLables(players)
        self.close_ui()
        self.screen.fill(BLACK)

        # Controlla se il debito è risolto
        self.game.is_debt_solved(self.player)
        # ↓ game.py, is_debt_solved()

# ========== FASE 4: VERIFICA DEBITO RISOLTO ==========
# File: game.py, is_debt_solved()

def is_debt_solved(self, player):
    if player.is_in_debt():  # Balance: 300, Debito: 400
        # ↓ Player.is_in_debt()
        #   return len(self.__debts) > 0  # True (ancora in debito)

        if len(player.get_stocks()) > 0:  # ✓ Ha ancora Stock2
            # Rimostra pannello per vendere altra cedola
            self.showStockUI = ShowStockUI(
                self, player.get_stocks(), "BANKRUPT_STOCK", player
            )
            self.panels_to_show.append(self.showStockUI)
        else:
            # Nessuna cedola rimasta
            self.renable_actions()
            self.showStockUI = None
            self.current_panel = None

            # Paga tutti i debiti possibili
            solve_larger_debts(player, self)

            # Elimina giocatore
            self.kill_player(player)
            self.is_there_some_player_in_bankrupt()

# ========== LUIGI VENDE SECONDA CEDOLA ==========
# File: showStockUI.py (stessa logica)

# Vende Stock2 (valore 300)
sell_stock_to_bank(...)  # Luigi: 300 + 150 = 450

# is_debt_solved()
player.is_in_debt() → True (450 < 400? No! Ma debito esiste ancora)

# RISOLUZIONE DEBITO
# File: game.py, is_debt_solved()

else:  # NOT in_debt (450 >= 400)
    self.renable_actions()
    self.showStockUI = None
    self.current_panel = None
    solve_bankrupt(player, self)
    # ↓ gameLogic.solve_bankrupt()
    #   for creditor, debt in zip(player.get_in_debt_with(), player.get_debts()):
    #       # creditor = Mario, debt = 400
    #       debtor.change_balance(-400)  # Luigi: 450 → 50
    #       creditor.change_balance(400) # Mario riceve 400
    #
    #   debtor.erase_debts()
    #   # ↓ Player.erase_debts()
    #   #   self.__in_debt_with = None
    #   #   self.__debts = []

    self.is_there_some_player_in_bankrupt()
    # Controlla se altri giocatori sono in debito

# ========== OPZIONE B: CLICK SU "METTI ALL'ASTA" ==========
# File: showStockUI.py, manage_events()

def manage_events(self, event, players, curr_player):
    if event.ui_element == self.auction_bankrupt:
        # Crea asta
        self.game.add_auction(self.player, self.get_showed_stock())
        # ↓ game.py, add_auction()
        #   players = self.get_other_players(player)  # Tutti tranne Luigi
        #   auction = Auction(
        #       self.__gameUI.manager,
        #       self.screen,
        #       player,      # Luigi (owner)
        #       players,     # [Mario, ...]
        #       stock,       # Stock1
        #       self.__board,
        #       self,
        #       self.__gameUI
        #   )
        #   self.__auctions.append(auction)

        self.close_ui()
        self.screen.fill(BLACK)
        self.game.showStockUI = None

        # Avvia asta
        self.game.start_first_auction()
        # ↓ game.py, start_first_auction()
        #   self.currentAuction = self.__auctions.pop(0)
        #
        #   if len(self.currentAuction.get_bidders()) >= 2:
        #       self.panels_to_show.append(self.currentAuction)
        #   else:
        #       # Solo 1 bidder → acquisto diretto
        #       stock = self.currentAuction.get_stock()
        #       self.showStockUI = ShowStockUI(
        #           self, [stock], "BUY_AUCTIONED_STOCK",
        #           self.currentAuction.get_bidders()[0]
        #       )
        #       self.panels_to_show.append(self.showStockUI)
        #       self.currentAuction = None

# ========== ASTA TERMINA ==========
# File: auction.py, dopo vincita

def manage_events(self, event, players, curr_player):
    if event.ui_element == self.bidBut:
        self.bid_but()
        if self.is_finished():  # Vince Mario con offerta 350
            finished_auction_logic(self.__board, self)
            # ↓ gameLogic.finished_auction_logic()
            #   winner = auction.get_winner()  # Mario
            #   stock = auction.get_stock()    # Stock1
            #   winner_bid = auction.get_winner_bid()  # 350
            #
            #   # Trasferisce cedola
            #   transfer_stock(board, winner, stock, True)
            #   # ↓ Mario riceve Stock1, paga 350
            #   #   Luigi riceve 350 scudi
            #
            #   owner = auction.get_owner()  # Luigi
            #   owner.change_balance(winner_bid)  # Luigi: 150 + 350 = 500

            self.open_next_if_present()
            # Se ci sono altre aste, continua
            # Altrimenti chiude e chiama game.renable_actions()

# ========== DOPO ASTA: VERIFICA DEBITO ==========
# Luigi ora ha 500 scudi, debito 400

# game.is_debt_solved(Luigi)
Luigi.is_in_debt() → True (debito esiste)

if len(Luigi.get_stocks()) > 0:  # Ha ancora Stock2
    # Mostra di nuovo pannello
else:
    # Vende Stock2 o va in bancarotta definitiva

# Scenario: Luigi vende anche Stock2 → totale 800 scudi
solve_bankrupt(Luigi, game)
# Luigi: 800 - 400 = 400 scudi rimanenti
# Mario: riceve 400 scudi

# Luigi sopravvive! ✓
```

**Sequenza Completa Banca Rotta**:
```
1. check_for_penalty()
   └─> set_in_debt_with(Mario)
   └─> add_debt(400)

2. turn() → if is_in_debt():
   └─> panels_to_show.append(ShowStockUI "BANKRUPT_STOCK")

3. draw_window() → ShowStockUI.draw()

4a. OPZIONE: Lascia alla banca
    ├─> sell_stock_to_bank(Stock1) → +150 scudi
    ├─> is_debt_solved(Luigi)
    │   └─> Ancora in debito → mostra di nuovo panel
    ├─> sell_stock_to_bank(Stock2) → +150 scudi
    └─> is_debt_solved(Luigi)
        └─> Debito risolto → solve_bankrupt() → paga 400 a Mario

4b. OPZIONE: Metti all'asta
    ├─> add_auction(Luigi, Stock1)
    ├─> start_first_auction()
    ├─> Auction UI → Mario vince con 350
    ├─> finished_auction_logic()
    │   ├─> transfer_stock(board, Mario, Stock1)
    │   └─> Luigi.change_balance(350)
    └─> is_debt_solved(Luigi)
        └─> Continua con Stock2...

5. Se NON risolve debito dopo tutte le cedole:
   ├─> solve_larger_debts(Luigi, game)
   │   └─> Paga quello che può (priorità debiti grandi)
   └─> kill_player(Luigi)
       ├─> players.remove(Luigi)
       ├─> Aggiusta current_player_index
       └─> Controlla vincitore (se rimane 1 giocatore)
```

---

## Diagrammi

### Diagramma Architettura Generale

```
┌─────────────────────────────────────────────────────────┐
│                     GAME LOOP                           │
│  ┌───────────────────────────────────────────────────┐  │
│  │  while running:                                   │  │
│  │    ├─ Bot AI (se bot)                            │  │
│  │    ├─ pygame.event.get()                         │  │
│  │    │    └─ manage_events()                       │  │
│  │    ├─ draw_window() (se panels in coda)         │  │
│  │    └─ update_graphic()                           │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
    ┌─────────┐    ┌──────────┐    ┌─────────────┐
    │  Board  │    │ Players  │    │   Events    │
    │         │    │          │    │   (deque)   │
    └─────────┘    └──────────┘    └─────────────┘
         │                │                │
         ▼                ▼                ▼
    ┌─────────┐    ┌──────────┐    ┌─────────────┐
    │  Cells  │    │  Stocks  │    │   EventUI   │
    │         │    │          │    │             │
    └─────────┘    └──────────┘    └─────────────┘
```

### Diagramma Sistema Pannelli

```
┌──────────────────────────────────────────────────────┐
│                   SISTEMA PANNELLI                   │
└──────────────────────────────────────────────────────┘
                          │
         ┌────────────────┴────────────────┐
         ▼                                 ▼
┌─────────────────┐              ┌─────────────────┐
│ alert_messages  │              │ panels_to_show  │
│   (lista)       │              │   (lista)       │
└─────────────────┘              └─────────────────┘
         │                                 │
         │         draw_window()           │
         └────────────┬────────────────────┘
                      ▼
            ┌───────────────────┐
            │  current_panel    │
            │  (riferimento)    │
            └───────────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
   ┌─────────┐  ┌──────────┐  ┌──────────┐
   │ EventUI │  │ BargainUI│  │ Auction  │
   └─────────┘  └──────────┘  └──────────┘
        ▼             ▼             ▼
   ┌─────────┐  ┌──────────┐  ┌──────────┐
   │ShowStock│  │DiceOverl.│  │TakeSome..│
   └─────────┘  └──────────┘  └──────────┘
```

### Diagramma Flusso Eventi

```
pygame.event.get()
        │
        ▼
┌───────────────────┐
│ pygame.QUIT?      │─Yes─→ running = False
└───────────────────┘
        │No
        ▼
┌───────────────────────────┐
│ UI_BUTTON_PRESSED?        │
└───────────────────────────┘
        │Yes
        ▼
┌────────────────────────────────────────┐
│ Bottone GameUI?                        │
│ ├─ launchDice → turn()                 │
│ ├─ buyButton → buy_stock_from_cell()   │
│ ├─ passButton → next player            │
│ └─ ...                                 │
└────────────────────────────────────────┘
        │No
        ▼
┌────────────────────────────────────────┐
│ Bottone current_panel?                 │
│ └─ current_panel.manage_events(...)    │
└────────────────────────────────────────┘
        │No
        ▼
┌────────────────────────────────────────┐
│ UI_DROP_DOWN_MENU_CHANGED?             │
│ └─ current_panel.manage_events(...)    │
└────────────────────────────────────────┘
```

### Diagramma Turno Completo

```
    START TURNO
         │
         ▼
    ┌─────────┐
    │ Lancia  │
    │  Dadi   │
    └─────────┘
         │
         ▼
    ┌─────────┐
    │ Muovi   │
    │ Giocatore│
    └─────────┘
         │
         ▼
  ┌──────────────┐
  │ Controlla    │
  │ Incidenti    │
  └──────────────┘
         │
         ▼
  ┌──────────────────────────────────┐
  │ Tipo Cella?                      │
  ├─ STOCKS → penalità + buy button  │
  ├─ EVENTS → mostra EventUI         │
  ├─ QUOTATION → aste                │
  ├─ CHOOSE_STOCK → scegli dove      │
  ├─ FREE_STOP → compra cedola       │
  ├─ CHANCE → lancia dadi denaro     │
  └─ ...                             │
         │
         ▼
  ┌──────────────┐
  │ In debito?   │
  └──────────────┘
       │Yes│No
       │   └─────────────────┐
       ▼                     │
  ┌──────────────┐           │
  │ ShowStockUI  │           │
  │ BANKRUPT     │           │
  └──────────────┘           │
       │                     │
       │ ┌───────────────────┘
       ▼ ▼
  ┌──────────────┐
  │ Mostra Alert │
  │ (se presenti)│
  └──────────────┘
         │
         ▼
  ┌──────────────┐
  │ Passa Turno? │
  └──────────────┘
       │Yes│No
       │   └─> Rilancia (doppio)
       ▼
   NEXT PLAYER
```

### Diagramma Ciclo Vita Auction

```
QUOTATION_TYPE
      │
      ▼
┌──────────────┐
│ quotation_   │
│ logic()      │
└──────────────┘
      │
      ▼
┌─────────────────────────────┐
│ Per ogni player con stocks  │
│ └─ ShowStockUI              │
│    "STOCK_TO_AUCTION"       │
└─────────────────────────────┘
      │
      ▼
┌─────────────────────────────┐
│ Player sceglie cedola       │
│ └─ add_auction(player,stock)│
└─────────────────────────────┘
      │
      ▼
┌─────────────────────────────┐
│ start_first_auction()       │
└─────────────────────────────┘
      │
      ├─ >= 2 bidders
      │  └─> Mostra Auction UI
      │
      └─ 1 bidder
         └─> ShowStockUI
             "BUY_AUCTIONED_STOCK"
      │
      ▼
┌─────────────────────────────┐
│ Asta in corso               │
│ ├─ OFFRI                    │
│ ├─ PASSA                    │
│ └─ RITIRATI                 │
└─────────────────────────────┘
      │
      ▼
┌─────────────────────────────┐
│ is_finished()?              │
└─────────────────────────────┘
      │
      ├─ Vincitore → trasferisci stock
      └─ Nessuno → vendi a banca
      │
      ▼
┌─────────────────────────────┐
│ open_next_if_present()      │
└─────────────────────────────┘
      │
      ├─ Altre aste → repeat
      └─ Fine → renable_actions()
```

### Diagramma Stati Bottoni Menu

```
                    ┌──────────────────┐
                    │  INIZIO TURNO    │
                    │  throw_dices: ✓  │
                    │  buy: ✗          │
                    │  pass: ✗         │
                    └──────────────────┘
                            │
                    Click "Lancia Dadi"
                            │
                            ▼
                    ┌──────────────────┐
                    │  DOPO LANCIO     │
                    │  throw_dices: ✗  │
                    │  buy: ✓*         │
                    │  pass: ✓         │
                    └──────────────────┘
                            │
              ┌─────────────┴─────────────┐
              │                           │
        Tiro Doppio?                 Panel Aperto?
              │                           │
              ▼                           ▼
      ┌──────────────────┐      ┌──────────────────┐
      │  TIRO DOPPIO     │      │  PANEL ATTIVO    │
      │  throw_dices: ✓  │      │  throw_dices: ✗  │
      │  buy: ✓*         │      │  buy: ✗          │
      │  pass: ✗         │      │  show_stock: ✗   │
      └──────────────────┘      │  pass: ✗         │
              │                 └──────────────────┘
              │                           │
              └───────────┬───────────────┘
                          │
                    Panel Chiuso
                          │
                          ▼
                  renable_actions()

* buy abilitato solo se può comprare cedola corrente
```

---

## Best Practices e Pattern

### 1. Aggiunta di un Nuovo Pannello

```python
# Passo 1: Crea la classe UI in lib/uiComponents/
class MyNewUI:
    def __init__(self, game, ...):
        self.game = game
        self.manager = game.get_gameUI().get_manager()

    def draw(self):
        # Crea UIPanel e componenti

    def manage_events(self, event, players, curr_player):
        # Gestisci eventi specifici

    def close_ui(self):
        # Pulisci e resetta riferimenti
        self.ui_panel.kill()
        self.game.current_panel = None
```

```python
# Passo 2: Aggiungi alla coda in Game
def some_game_logic(self):
    new_panel = MyNewUI(self, ...)
    self.panels_to_show.append(new_panel)
    self.disable_actions()
```

```python
# Passo 3: (Opzionale) Gestisci eventi speciali in Game.manage_events()
elif hasattr(self.current_panel, "specialButton") and \
     event.ui_element == self.current_panel.specialButton:
    # Logica speciale
    self.current_panel.close_ui()
```

### 2. Gestione Denaro e Debiti

```python
# Sempre usare change_balance(), non modificare direttamente
player.change_balance(amount)   # Positivo = riceve, negativo = paga

# Per debiti
if player.get_balance() < cost:
    player.set_in_debt_with(creditor)  # "BANK", "SQUARE", o Player
    player.add_debt(cost)
```

### 3. Modifiche all'UI

```python
# Dopo modifiche ai giocatori, aggiorna sempre le label
self.__gameUI.updateAllPlayerLables(self.get_players())

# Dopo modifiche a cedole, aggiorna stockboard
Player.last_stock_update = time.time()
# update_graphic() farà il resto
```

### 4. Debugging

```python
# Modalità test per controllare i dadi
game = Game(..., test=True)

# In-game:
# Premi 0-9 per impostare i dadi
# Premi ENTER per lanciare
# Premi SPAZIO per resettare
```

---

## Conclusione

Questa architettura separa chiaramente:
- **Presentazione** (UIComponents)
- **Logica** (gameLogic.py, eventi)
- **Stato** (ActionsStatus, code pannelli)

Il sistema a **coda di pannelli** permette di gestire sequenze complesse (es. quotation → aste multiple → bancarotta) in modo ordinato e prevedibile.

La **delega degli eventi** da Game ai pannelli mantiene il codice modulare e testabile.
