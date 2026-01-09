# Sistema di Stress Testing per PyazzaMarket

Sistema completo di stress testing automatico con logging dettagliato, riproducibilità garantita e crash reporting per debugging.

## 📋 Indice

- [Caratteristiche](#caratteristiche)
- [Installazione](#installazione)
- [Quick Start](#quick-start)
- [Componenti](#componenti)
- [Utilizzo Dettagliato](#utilizzo-dettagliato)
- [Analisi degli Errori](#analisi-degli-errori)
- [Tips & Best Practices](#tips--best-practices)

## ✨ Caratteristiche

- ✅ **Esecuzione automatica** di partite complete con bot
- ✅ **Logging dettagliato** di ogni azione (dadi, movimenti, eventi, transazioni)
- ✅ **Riproducibilità garantita** tramite seed deterministici
- ✅ **Crash reporting** completo con stato del gioco al momento dell'errore
- ✅ **Replay system** per rigiocare esattamente le stesse partite
- ✅ **Modalità headless** per test veloci senza GUI
- ✅ **Statistiche e analisi** automatiche
- ✅ **Cross-platform** (Linux, Windows, Mac)

## 🚀 Installazione

Nessuna installazione aggiuntiva necessaria! Il sistema usa solo le dipendenze già presenti nel progetto.

## ⚡ Quick Start

### Test Rapido (10 partite)
```bash
# Linux/Mac
./test_runner.sh quick

# Windows o alternativa cross-platform
python test_runner.py quick
```

### Test con Seed Specifico
```bash
# Per riprodurre un problema specifico
./test_runner.sh seed 12345
```

### Replay di una Partita con Errori
```bash
# Trova i log con errori
./test_runner.sh find-errors

# Rigiocare una partita
./test_runner.sh replay stress_test_logs/stress_test_0001_seed_12345.json
```

## 📦 Componenti

### 1. **game_logger.py** - Sistema di Logging
Traccia ogni azione del gioco:
- Lanci di dadi
- Movimenti dei giocatori
- Transazioni di cedole
- Cambi di soldi
- Eventi triggherati
- Aste
- Bancarotte
- Errori con stack trace completo

### 2. **seeded_random.py** - Generazione Deterministica
Garantisce riproducibilità:
- `SeededRandom`: Generatore di numeri casuali con seed
- `DiceController`: Controller per lanci di dadi riproducibili
- `EventController`: Controller per shuffle eventi deterministico

### 3. **stress_test.py** - Stress Tester
Esegue partite automatiche:
- Crea partite con 4 bot
- Esegue turni automatici
- Cattura e logga errori
- Genera report dettagliati
- Supporta modalità headless

### 4. **replay_game.py** - Sistema di Replay
Rigiocare partite da log:
- Replay completo con stesso seed
- Modalità step-by-step per debugging
- Analisi dettagliata dei log
- Confronto errori originali vs replay

### 5. **test_runner.sh / test_runner.py** - Launcher
Script di lancio con utilities:
- Comandi predefiniti (quick, medium, intensive)
- Gestione log
- Ricerca errori
- Statistiche

## 📖 Utilizzo Dettagliato

### Stress Testing

#### Test Rapidi
```bash
# 10 test (circa 5-10 minuti)
./test_runner.sh quick

# 50 test (circa 30-60 minuti)
./test_runner.sh medium

# 100 test (circa 1-2 ore)
./test_runner.sh intensive

# 1000 test (per esecuzione notturna)
./test_runner.sh overnight
```

#### Test con Opzioni
```bash
# Test headless (molto più veloce, no GUI)
./test_runner.sh intensive --headless

# Limita i turni per partita
python stress_test.py -n 50 --max-turns 200 --headless

# Test con seed specifico
./test_runner.sh seed 42
```

### Replay e Debugging

#### Trovare Errori
```bash
# Lista tutti i log con errori
./test_runner.sh find-errors

# Output esempio:
# ✗ stress_test_0042_seed_98765.json
#   Tipo errore: IndexError
#   Path: /path/to/log.json
```

#### Rigiocare una Partita
```bash
# Replay normale (veloce)
./test_runner.sh replay stress_test_logs/stress_test_0042.json

# Replay step-by-step (turno per turno)
./test_runner.sh replay stress_test_logs/stress_test_0042.json -s

# Solo analisi senza replay
./test_runner.sh analyze stress_test_logs/stress_test_0042.json
```

#### Replay Step-by-Step
Ottimo per debugging dettagliato:
```bash
python replay_game.py -s logs/game_with_error.json

# Durante il replay:
# - Premi INVIO per avanzare al turno successivo
# - Digita 'q' per uscire
# - Vedi dadi, posizioni, bilanci per ogni turno
```

### Analisi e Statistiche

#### Statistiche Generali
```bash
./test_runner.sh stats

# Output:
# Test totali eseguiti: 150
# Successi: 147
# Con errori: 3
# Tasso di successo: 98.0%
```

#### Analisi Dettagliata di un Log
```bash
python replay_game.py --analyze-only logs/game.json

# Mostra:
# - Azioni per categoria
# - Eventi triggherati
# - Bancarotte
# - Dettagli errori con stato del gioco
```

## 🔍 Analisi degli Errori

### Struttura dei Log

Ogni partita genera un file JSON con:
```json
{
  "session_name": "stress_test_0001_seed_12345",
  "start_time": "2026-01-09T10:30:00",
  "seed": 12345,
  "initial_state": {
    "players": [...],
    "board": {...}
  },
  "actions": [
    {
      "id": 1,
      "timestamp": "2026-01-09T10:30:01",
      "category": "dice_roll",
      "type": "roll",
      "data": {
        "player": "Bot1",
        "dice1": 4,
        "dice2": 3,
        "total": 7,
        "is_double": false,
        "position_before": 0
      }
    },
    ...
  ],
  "errors": [
    {
      "timestamp": "2026-01-09T10:35:42",
      "type": "IndexError",
      "message": "list index out of range",
      "stack_trace": "...",
      "game_state": {
        "current_player_index": 2,
        "players": [...],
        ...
      },
      "action_count": 157
    }
  ],
  "status": "error",
  "end_time": "2026-01-09T10:35:42"
}
```

### Workflow per Debugging

1. **Esegui Stress Test**
   ```bash
   ./test_runner.sh intensive --headless
   ```

2. **Trova Errori**
   ```bash
   ./test_runner.sh find-errors
   ```

3. **Rigiocare la Partita con Errore**
   ```bash
   # Prima analizza
   ./test_runner.sh analyze logs/game_with_error.json

   # Poi replay step-by-step
   python replay_game.py -s logs/game_with_error.json
   ```

4. **Identifica il Problema**
   - Il replay si fermerà esattamente al punto dell'errore
   - Vedrai lo stato completo del gioco
   - Stack trace identico all'originale

5. **Fixa il Bug**
   - Correggi il codice

6. **Verifica il Fix**
   ```bash
   # Rigiocare con lo stesso seed
   ./test_runner.sh seed <SEED_DELL_ERRORE>
   ```

## 💡 Tips & Best Practices

### Per Test Veloci
- Usa sempre `--headless` per test automatici
- Limita `--max-turns` se necessario
- Usa `quick` per verifiche rapide dopo fix

### Per Trovare Bug Rari
- Esegui `overnight` prima di committare
- Usa seed diversi per variabilità
- Tieni i log degli errori per analisi successive

### Per Debugging Efficace
1. **Usa step-by-step** quando l'errore è vicino
2. **Analizza prima** per capire il contesto
3. **Controlla il turno** in cui avviene l'errore
4. **Verifica lo stato** dei giocatori in quel momento

### Gestione dei Log
```bash
# I log possono occupare spazio, pulisci periodicamente
./test_runner.sh clean

# Ma salva sempre i log con errori interessanti!
mkdir bugs_archive
cp stress_test_logs/*error*.json bugs_archive/
```

## 🔧 Configurazione Avanzata

### Modificare il Numero di Bot
Modifica [stress_test.py](stress_test.py:73-77):
```python
players = [
    {"name": "Bot1", "color": "red", "bot": True},
    {"name": "Bot2", "color": "blue", "bot": True},
    # Aggiungi o rimuovi bot qui
]
```

### Personalizzare il Logging
Modifica [game_logger.py](game_logger.py:60-80) per aggiungere nuove categorie di log.

### Esecuzione Parallela
Per test molto intensivi:
```bash
# Esegui più istanze in parallelo
./test_runner.sh intensive --headless &
./test_runner.sh intensive --headless &
./test_runner.sh intensive --headless &
wait
```

## 📊 Interpretare i Risultati

### Summary Files
Ogni run genera un `summary_*.txt`:
```
STRESS TEST SUMMARY
================================================================================

Esecuzione: 2026-01-09 10:30:00
Seed base: 1736421000000
Numero test: 100
Durata totale: 3600.00s
Tempo medio per test: 36.00s

RISULTATI:
  ✓ Successi: 97/100 (97.0%)
  ✗ Errori: 3/100 (3.0%)

ERRORI TROVATI:
Test #42 - Seed: 1736421000041
  Tipo: IndexError
  Messaggio: list index out of range
  Turno: 157
  Log: stress_test_logs/stress_test_0042_seed_1736421000041.json
```

### Tasso di Successo Accettabile
- **> 99%**: Eccellente, solo bug molto rari
- **95-99%**: Buono, alcuni edge case da fixare
- **90-95%**: Discreto, serve lavoro sui bug comuni
- **< 90%**: Problemi seri, debugging prioritario

## 🐛 Troubleshooting

### "ModuleNotFoundError"
```bash
# Assicurati di essere nella directory giusta
cd /path/to/PyazzaMarket

# Attiva virtual environment se necessario
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### "Permission denied" (Linux/Mac)
```bash
chmod +x test_runner.sh
```

### Test Troppo Lenti
- Usa `--headless`
- Riduci `--max-turns`
- Chiudi altre applicazioni

### Out of Memory
- Riduci numero di test simultanei
- Pulisci log vecchi
- Aumenta limite turni più basso

## 📝 Esempi Completi

### Caso d'uso 1: Prima di un Commit
```bash
# Quick test per verificare che non hai rotto nulla
./test_runner.sh quick --headless

# Se tutto ok, commit
git add .
git commit -m "Fix bug X"
```

### Caso d'uso 2: Debugging di un Bug Segnalato
```bash
# 1. Riproduci il bug
./test_runner.sh intensive --headless

# 2. Trova l'errore
./test_runner.sh find-errors

# 3. Analizza
./test_runner.sh analyze logs/error_log.json

# 4. Replay step-by-step
python replay_game.py -s logs/error_log.json

# 5. Fixa
# ... edit code ...

# 6. Verifica con stesso seed
./test_runner.sh seed <SEED_ORIGINALE>
```

### Caso d'uso 3: Test Notturno
```bash
# Lancia prima di andare a dormire
nohup ./test_runner.sh overnight --headless > test_output.log 2>&1 &

# Al mattino, controlla risultati
./test_runner.sh stats
./test_runner.sh find-errors
```

## 🎯 Obiettivi del Sistema

Questo sistema di testing ti permette di:

1. ✅ **Trovare bug nascosti** eseguendo migliaia di partite
2. ✅ **Riprodurre esattamente** ogni bug trovato
3. ✅ **Debuggare efficacemente** vedendo lo stato completo
4. ✅ **Verificare fix** rieseguendo con stesso seed
5. ✅ **Monitorare stabilità** con statistiche aggregate
6. ✅ **Sviluppare con confidenza** sapendo che i test girano

## 📞 Supporto

Per problemi o domande:
1. Controlla questa documentazione
2. Verifica i log in `stress_test_logs/`
3. Usa `--help` sui vari script
4. Controlla il codice sorgente (ben commentato)

---

**Happy Testing! 🎮🐛**
