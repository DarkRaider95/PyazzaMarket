#!/bin/bash
# Script di lancio per stress test di PyazzaMarket
# Fornisce varie modalità di testing e utilities

set -e

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/stress_test_logs"

# Banner
echo -e "${BLUE}╔════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║           PyazzaMarket Stress Test Runner                          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════════╝${NC}"
echo

# Funzione di help
show_help() {
    cat << EOF
Uso: $0 [COMANDO] [OPZIONI]

COMANDI:
    quick           Esegui 10 test rapidi
    medium          Esegui 50 test
    intensive       Esegui 100 test
    overnight       Esegui 1000 test (per test notturni)
    seed SEED       Esegui test con un seed specifico
    replay LOG      Rigiocare una partita da un file di log
    analyze LOG     Analizza un file di log senza rigiocare
    find-errors     Trova tutti i log con errori
    clean           Pulisce i file di log
    stats           Mostra statistiche sui test eseguiti
    help            Mostra questo messaggio

ESEMPI:
    $0 quick                    # 10 test rapidi
    $0 seed 12345               # Test con seed 12345
    $0 replay logs/game_001.json  # Replay di una partita
    $0 intensive --headless     # 100 test senza GUI (veloce)
    $0 find-errors              # Trova tutti gli errori nei log

OPZIONI:
    --headless      Esegui senza GUI (molto più veloce)
    --max-turns N   Limita i turni a N (default: 500)
    --help          Mostra questo messaggio
EOF
}

# Funzione per eseguire stress test
run_stress_test() {
    local num_tests=$1
    local extra_args="${@:2}"

    echo -e "${GREEN}Esecuzione di $num_tests test...${NC}"
    echo

    python3 "$SCRIPT_DIR/stress_test.py" -n "$num_tests" $extra_args

    echo
    echo -e "${GREEN}✓ Test completati!${NC}"
    echo -e "Controlla i risultati in: ${YELLOW}$LOG_DIR${NC}"
}

# Funzione per replay
run_replay() {
    local log_file=$1
    local extra_args="${@:2}"

    if [ ! -f "$log_file" ]; then
        echo -e "${RED}✗ File non trovato: $log_file${NC}"
        exit 1
    fi

    echo -e "${BLUE}Replay di: $log_file${NC}"
    echo

    python3 "$SCRIPT_DIR/replay_game.py" "$log_file" $extra_args
}

# Funzione per analizzare log
analyze_log() {
    local log_file=$1

    if [ ! -f "$log_file" ]; then
        echo -e "${RED}✗ File non trovato: $log_file${NC}"
        exit 1
    fi

    echo -e "${BLUE}Analisi di: $log_file${NC}"
    echo

    python3 "$SCRIPT_DIR/replay_game.py" "$log_file" --analyze-only
}

# Funzione per trovare errori
find_errors() {
    echo -e "${YELLOW}Ricerca log con errori...${NC}"
    echo

    if [ ! -d "$LOG_DIR" ]; then
        echo -e "${RED}✗ Directory log non trovata${NC}"
        exit 1
    fi

    local error_count=0
    local total_count=0

    for log_file in "$LOG_DIR"/*.json; do
        if [ -f "$log_file" ]; then
            total_count=$((total_count + 1))

            # Controlla se contiene errori
            if grep -q '"errors": \[' "$log_file" && ! grep -q '"errors": \[\]' "$log_file"; then
                error_count=$((error_count + 1))
                echo -e "${RED}✗${NC} $(basename "$log_file")"

                # Estrai tipo di errore
                error_type=$(python3 -c "
import json
with open('$log_file') as f:
    data = json.load(f)
    if data.get('errors'):
        print(data['errors'][0].get('type', 'Unknown'))
" 2>/dev/null || echo "Unknown")

                echo -e "  Tipo errore: ${YELLOW}$error_type${NC}"
                echo -e "  Path: ${BLUE}$log_file${NC}"
                echo
            fi
        fi
    done

    echo -e "${GREEN}Scansione completata${NC}"
    echo -e "Log totali: $total_count"
    echo -e "Con errori: ${RED}$error_count${NC}"

    if [ $error_count -gt 0 ]; then
        echo
        echo -e "${YELLOW}Usa '$0 replay <log_file>' per rigiocare una partita con errori${NC}"
    fi
}

# Funzione per statistiche
show_stats() {
    echo -e "${BLUE}Statistiche test eseguiti${NC}"
    echo

    if [ ! -d "$LOG_DIR" ]; then
        echo -e "${RED}✗ Nessun test eseguito ancora${NC}"
        exit 0
    fi

    local total_logs=$(find "$LOG_DIR" -name "*.json" -not -name "*summary*" | wc -l)
    local error_logs=$(find "$LOG_DIR" -name "*.json" -not -name "*summary*" -exec grep -l '"errors": \[[^]]\+\]' {} \; 2>/dev/null | wc -l)
    local success_logs=$((total_logs - error_logs))

    echo "Test totali eseguiti: $total_logs"
    echo -e "Successi: ${GREEN}$success_logs${NC}"
    echo -e "Con errori: ${RED}$error_logs${NC}"

    if [ $total_logs -gt 0 ]; then
        local success_rate=$(python3 -c "print(f'{$success_logs / $total_logs * 100:.1f}')")
        echo -e "Tasso di successo: ${GREEN}${success_rate}%${NC}"
    fi

    # Mostra ultimi summary
    echo
    echo -e "${YELLOW}Ultimi 5 summary:${NC}"
    find "$LOG_DIR" -name "summary_*.txt" -type f | sort -r | head -5 | while read file; do
        echo "  • $(basename "$file")"
    done
}

# Funzione per pulire log
clean_logs() {
    echo -e "${YELLOW}Pulizia log...${NC}"

    if [ ! -d "$LOG_DIR" ]; then
        echo -e "${BLUE}Nessun log da pulire${NC}"
        exit 0
    fi

    read -p "Sei sicuro di voler cancellare tutti i log? [y/N] " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf "$LOG_DIR"
        echo -e "${GREEN}✓ Log cancellati${NC}"
    else
        echo -e "${BLUE}Operazione annullata${NC}"
    fi
}

# Main logic
COMMAND="${1:-help}"
shift || true

case "$COMMAND" in
    quick)
        run_stress_test 10 "$@"
        ;;
    medium)
        run_stress_test 50 "$@"
        ;;
    intensive)
        run_stress_test 100 "$@"
        ;;
    overnight)
        run_stress_test 1000 "$@"
        ;;
    seed)
        if [ -z "$1" ]; then
            echo -e "${RED}✗ Specifica un seed${NC}"
            echo "Uso: $0 seed SEED_NUMBER"
            exit 1
        fi
        SEED=$1
        shift
        run_stress_test 1 --seed "$SEED" "$@"
        ;;
    replay)
        if [ -z "$1" ]; then
            echo -e "${RED}✗ Specifica un file di log${NC}"
            echo "Uso: $0 replay LOG_FILE"
            exit 1
        fi
        run_replay "$@"
        ;;
    analyze)
        if [ -z "$1" ]; then
            echo -e "${RED}✗ Specifica un file di log${NC}"
            echo "Uso: $0 analyze LOG_FILE"
            exit 1
        fi
        analyze_log "$1"
        ;;
    find-errors)
        find_errors
        ;;
    stats)
        show_stats
        ;;
    clean)
        clean_logs
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}✗ Comando sconosciuto: $COMMAND${NC}"
        echo
        show_help
        exit 1
        ;;
esac
