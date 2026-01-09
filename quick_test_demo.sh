#!/bin/bash
# Demo script per testare velocemente il sistema di stress testing
# Esegue 1 singolo test per verificare che tutto funzioni

set -e

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║           PyazzaMarket Stress Test - Quick Demo                    ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Questo script esegue un singolo test per verificare che il sistema"
echo "di stress testing funzioni correttamente."
echo ""
read -p "Premi INVIO per continuare..."

echo ""
echo "▶ Step 1: Esecuzione di un singolo stress test..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 stress_test.py -n 1 --headless --max-turns 100

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Test completato con successo!"
else
    echo ""
    echo "✗ Test fallito"
    exit 1
fi

echo ""
echo "▶ Step 2: Controllo dei log generati..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -d "stress_test_logs" ]; then
    LOG_COUNT=$(find stress_test_logs -name "*.json" -not -name "*summary*" | wc -l)
    echo "✓ Directory log creata: stress_test_logs/"
    echo "✓ File di log trovati: $LOG_COUNT"

    LATEST_LOG=$(find stress_test_logs -name "stress_test_*.json" | sort | tail -1)
    echo "✓ Ultimo log: $(basename $LATEST_LOG)"
else
    echo "✗ Directory log non trovata"
    exit 1
fi

echo ""
echo "▶ Step 3: Analisi del log..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 replay_game.py --analyze-only "$LATEST_LOG"

echo ""
echo "▶ Step 4: Test del sistema di replay..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Saltato per questa demo (usa './test_runner.sh replay $LATEST_LOG' per testarlo)"

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                    DEMO COMPLETATA CON SUCCESSO!                    ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Il sistema di stress testing è funzionante. Ora puoi:"
echo ""
echo "  1. Eseguire test più intensivi:"
echo "     ./test_runner.sh quick         # 10 test"
echo "     ./test_runner.sh intensive     # 100 test"
echo ""
echo "  2. Trovare errori:"
echo "     ./test_runner.sh find-errors"
echo ""
echo "  3. Rigiocare una partita:"
echo "     ./test_runner.sh replay $LATEST_LOG"
echo ""
echo "  4. Vedere le statistiche:"
echo "     ./test_runner.sh stats"
echo ""
echo "📖 Per maggiori informazioni: cat STRESS_TEST_README.md"
echo ""
