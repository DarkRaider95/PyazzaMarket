# Esempi Pratici di Utilizzo del Sistema di Stress Testing

Questa guida mostra esempi pratici step-by-step per i casi d'uso più comuni.

## 📚 Indice Esempi

1. [Test Rapido Prima del Commit](#1-test-rapido-prima-del-commit)
2. [Trovare e Debuggare un Bug](#2-trovare-e-debuggare-un-bug)
3. [Test Intensivo Pre-Release](#3-test-intensivo-pre-release)
4. [Riprodurre un Bug Segnalato](#4-riprodurre-un-bug-segnalato)
5. [Test Notturno Automatico](#5-test-notturno-automatico)

---

## 1. Test Rapido Prima del Commit

**Scenario**: Hai fatto modifiche al codice e vuoi verificare rapidamente che non hai rotto nulla.

### Step 1: Esegui il test rapido
```bash
# Linux/Mac
./test_runner.sh quick --headless

# Windows
python test_runner.py quick
```

**Output atteso**:
```
╔═══════════════════════════════════════════════════════════════════╗
║           PyazzaMarket Stress Test Runner                         ║
║ Esecuzione di 10 tests                                            ║
║ Seed base: 1736421234567                                          ║
╚═══════════════════════════════════════════════════════════════════╝

================================================================================
Test 1/10 - Seed: 1736421234567
================================================================================
...
✓ Test 1 completato: success
  Turni: 234
  Durata: 12.45s
...
================================================================================
STRESS TEST COMPLETATO
================================================================================
Successi: 10/10
Errori: 0/10
Summary salvato in: stress_test_logs/summary_20260109_103045.txt
```

### Step 2: Verifica risultati
```bash
./test_runner.sh stats
```

### Step 3: Se tutto OK, commit
```bash
git add .
git commit -m "Implementata nuova feature X"
git push
```

---

## 2. Trovare e Debuggare un Bug

**Scenario**: Il gioco si blocca occasionalmente, vuoi trovare e fixare il bug.

### Step 1: Esegui test intensivo per trovare il bug
```bash
# Esegui 100 test headless (veloce)
./test_runner.sh intensive --headless
```

**Output se trova un errore**:
```
================================================================================
Test 42/100 - Seed: 1736421234608
================================================================================

⚠ ERRORE TROVATO!
  Tipo: IndexError
  Messaggio: list index out of range
  Turno: 157

✗ Test 42 completato: error
  Turni: 157
  Durata: 8.23s
  Log: stress_test_logs/stress_test_0042_seed_1736421234608.json
```

### Step 2: Lista tutti gli errori trovati
```bash
./test_runner.sh find-errors
```

**Output**:
```
🔍 Ricerca log con errori...

✗ stress_test_0042_seed_1736421234608.json
  Tipo errore: IndexError
  Path: stress_test_logs/stress_test_0042_seed_1736421234608.json

Scansione completata
Log totali: 100
Con errori: 1

💡 Usa './test_runner.sh replay <log_file>' per rigiocare
```

### Step 3: Analizza il log dell'errore
```bash
./test_runner.sh analyze stress_test_logs/stress_test_0042_seed_1736421234608.json
```

**Output**:
```
📊 ANALISI LOG

Azioni per categoria:
  dice_roll: 314
  move: 314
  money: 127
  event: 23
  stock: 45

Eventi triggherati: 23

DETTAGLI ERRORI
Errore #1:
  Tipo: IndexError
  Messaggio: list index out of range
  Azione: 314
  Timestamp: 2026-01-09T10:35:42

  Stato al momento dell'errore:
    Indice giocatore: 2
    Giocatori attivi: 4
```

### Step 4: Replay step-by-step per capire esattamente cosa succede
```bash
python replay_game.py -s stress_test_logs/stress_test_0042_seed_1736421234608.json
```

**Interazione durante replay**:
```
Caricamento log da: stress_test_logs/stress_test_0042_seed_1736421234608.json
Seed: 1736421234608
Azioni registrate: 314
Errori registrati: 1

⚠ ATTENZIONE: Questo log contiene errori!
  1. IndexError: list index out of range
     Al turno: 157

Modalità STEP-BY-STEP attiva
Premi INVIO per avanzare al prossimo turno, 'q' per uscire

Turno 1 - Bot1 >>>  [PREMI INVIO]
  Dadi: 4 + 3 = 7

Turno 2 - Bot2 >>>  [PREMI INVIO]
  Dadi: 2 + 5 = 7

...

Turno 155 - Bot3 >>>  [PREMI INVIO]
  Dadi: 6 + 6 = 12

⚠ Avvicinamento all'errore (turno 155)

Turno 156 - Bot4 >>>  [PREMI INVIO]
  Dadi: 3 + 2 = 5

Turno 157 - Bot1 >>>  [PREMI INVIO]
  Dadi: 5 + 1 = 6

================================================================================
⚠ PUNTO DI ERRORE RAGGIUNTO (turno 157)
================================================================================

Stato del gioco:
Giocatore corrente: Bot1
Bilancio piazza: 2450

Stato giocatori:
  • Bot1:
      Posizione: 23
      Bilancio: 850
      Cedole: 3
  • Bot2:
      Posizione: 15
      Bilancio: 1200
      Cedole: 2
  ...

================================================================================
✗ ERRORE DURANTE IL REPLAY AL TURNO 157
================================================================================
Tipo: IndexError
Messaggio: list index out of range

Stack trace:
  File "lib/game.py", line 178, in turn
    cell = self.__board.get_cells()[curr_player.get_position()]
IndexError: list index out of range

✓ L'errore è stato RIPRODOTTO con successo!
```

### Step 5: Analizza il codice e fixa il bug
Ora sai esattamente:
- **Quale turno** (157)
- **Quale giocatore** (Bot1)
- **Quale posizione** (23 - fuori range!)
- **Lo stato completo** del gioco

Apri [lib/game.py](lib/game.py:178) e fixa:
```python
# PRIMA (buggy)
cell = self.__board.get_cells()[curr_player.get_position()]

# DOPO (fixato)
position = curr_player.get_position()
cells = self.__board.get_cells()

# Assicurati che la posizione sia valida
if position >= len(cells):
    position = position % len(cells)  # Wrap around
    curr_player.set_position(position)

cell = cells[position]
```

### Step 6: Verifica il fix con lo stesso seed
```bash
# Rigiocare con lo stesso seed per verificare che il bug è fixato
./test_runner.sh seed 1736421234608
```

**Output atteso**:
```
Test 1/1 - Seed: 1736421234608
✓ Test 1 completato: success
  Turni: 345
  Durata: 15.67s
```

✅ **Bug fixato e verificato!**

---

## 3. Test Intensivo Pre-Release

**Scenario**: Prima di rilasciare una nuova versione, vuoi essere sicuro che tutto funzioni.

### Step 1: Esegui test intensivo overnight
```bash
# Lancia 1000 test in background
nohup ./test_runner.sh overnight --headless > test_output.log 2>&1 &

# Salva il PID per poterlo killare se necessario
echo $! > test_pid.txt
```

### Step 2: Monitora il progresso (opzionale)
```bash
# Controlla quanti test sono stati completati
watch -n 10 './test_runner.sh stats'

# Oppure segui il log
tail -f test_output.log
```

### Step 3: Al mattino, controlla i risultati
```bash
# Statistiche generali
./test_runner.sh stats
```

**Output**:
```
📊 Statistiche test eseguiti

Test totali eseguiti: 1000
Successi: 987
Con errori: 13
Tasso di successo: 98.7%

Ultimi 5 summary:
  • summary_20260109_083045.txt
  • summary_20260109_063012.txt
  • summary_20260109_043001.txt
  • summary_20260109_023045.txt
  • summary_20260109_003012.txt
```

### Step 4: Analizza gli errori trovati
```bash
./test_runner.sh find-errors > errors_report.txt
cat errors_report.txt
```

### Step 5: Decidi se rilasciare
- **> 99% successi**: Ottimo! Puoi rilasciare
- **95-99%**: Valuta la gravità degli errori
- **< 95%**: Fixa i bug prima del rilascio

---

## 4. Riprodurre un Bug Segnalato

**Scenario**: Un utente ha segnalato un bug sporadico. Vuoi riprodurlo per fixarlo.

### Step 1: Cerca il bug con test random
```bash
# Esegui molti test con seed diversi
./test_runner.sh intensive --headless

# Se non lo trovi, prova ancora
./test_runner.sh intensive --headless
./test_runner.sh intensive --headless
```

### Step 2: Quando lo trovi, salva il seed
```bash
./test_runner.sh find-errors
```

Annota il seed del bug, esempio: `1736421234567`

### Step 3: Condividi il seed per riproducibilità
Ora puoi condividere questo seed con il team:
```bash
# Chiunque può riprodurre esattamente lo stesso bug
./test_runner.sh seed 1736421234567
```

### Step 4: Debugga con replay
```bash
python replay_game.py -s stress_test_logs/stress_test_*_seed_1736421234567.json
```

---

## 5. Test Notturno Automatico

**Scenario**: Vuoi che i test girino automaticamente ogni notte.

### Opzione A: Cron Job (Linux/Mac)

Crea uno script `nightly_test.sh`:
```bash
#!/bin/bash
cd /path/to/PyazzaMarket
./test_runner.sh overnight --headless > logs/nightly_$(date +%Y%m%d).log 2>&1

# Invia email se ci sono errori (opzionale)
if ./test_runner.sh find-errors | grep -q "Con errori: [1-9]"; then
    mail -s "PyazzaMarket: Errori trovati!" admin@example.com < logs/nightly_$(date +%Y%m%d).log
fi
```

Aggiungi a crontab:
```bash
crontab -e

# Aggiungi questa riga (esegue ogni notte alle 2:00 AM)
0 2 * * * /path/to/nightly_test.sh
```

### Opzione B: Task Scheduler (Windows)

1. Apri Task Scheduler
2. Crea nuovo task
3. Trigger: Daily alle 2:00 AM
4. Action: Start a program
   - Program: `python`
   - Arguments: `test_runner.py overnight --headless`
   - Start in: `C:\path\to\PyazzaMarket`

### Opzione C: GitHub Actions

Crea `.github/workflows/nightly-test.yml`:
```yaml
name: Nightly Stress Test

on:
  schedule:
    - cron: '0 2 * * *'  # 2:00 AM UTC
  workflow_dispatch:  # Permette esecuzione manuale

jobs:
  stress-test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: |
        pip install -r requirements.txt

    - name: Run stress tests
      run: |
        python test_runner.py medium --headless

    - name: Upload logs
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: stress-test-logs
        path: stress_test_logs/

    - name: Check for errors
      run: |
        python test_runner.py find-errors
```

---

## 💡 Tips Bonus

### Creare un Bug Report Automatico
```bash
#!/bin/bash
# bug_report.sh - Genera un report dettagliato

LOG_FILE=$1
REPORT_FILE="bug_report_$(date +%Y%m%d_%H%M%S).txt"

echo "BUG REPORT - $(date)" > $REPORT_FILE
echo "=============================" >> $REPORT_FILE
echo "" >> $REPORT_FILE

# Analisi del log
python replay_game.py --analyze-only $LOG_FILE >> $REPORT_FILE

# Info di sistema
echo "" >> $REPORT_FILE
echo "SYSTEM INFO" >> $REPORT_FILE
echo "=============================" >> $REPORT_FILE
uname -a >> $REPORT_FILE
python --version >> $REPORT_FILE

echo "Report salvato in: $REPORT_FILE"
```

### Test su Feature Specifica
Se vuoi testare solo una feature specifica, modifica [stress_test.py](stress_test.py:73-77):
```python
# Esempio: testa solo partite con molti eventi
players = [
    {"name": "Bot1", "color": "red", "bot": True},
    {"name": "Bot2", "color": "blue", "bot": True},
]  # Meno giocatori = più eventi per giocatore
```

### Confrontare Due Versioni
```bash
# Test sulla versione corrente
./test_runner.sh intensive --headless
mv stress_test_logs stress_test_logs_v1

# Switcha a un'altra branch
git checkout feature-branch

# Test sulla nuova versione
./test_runner.sh intensive --headless
mv stress_test_logs stress_test_logs_v2

# Confronta
diff <(./test_runner.sh stats --dir stress_test_logs_v1) \
     <(./test_runner.sh stats --dir stress_test_logs_v2)
```

---

## 🎯 Checklist Sviluppatore

Prima di ogni commit:
- [ ] `./test_runner.sh quick` passa
- [ ] Nessun nuovo errore introdotto

Prima di ogni merge:
- [ ] `./test_runner.sh medium` passa con > 95% successo
- [ ] Tutti gli errori critici fixati

Prima di ogni release:
- [ ] `./test_runner.sh intensive` passa con > 99% successo
- [ ] Test notturni eseguiti per almeno 3 notti
- [ ] Tutti i bug noti documentati o fixati

---

**Buon testing! 🚀**
