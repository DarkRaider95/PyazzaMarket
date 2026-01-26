#!/usr/bin/env python3
"""
Cross-platform test runner per PyazzaMarket.
Alternativa Python allo script bash, funziona su Windows/Linux/Mac.
"""

## ci sono degli import non usati

import argparse
import glob
import json
import os
import random
import subprocess
import sys
import time
from pathlib import Path


class TestRunner:
    """Runner cross-platform per stress test."""

    ## lo script è stato spostato controllare che l'init sia corretto

    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.log_dir = self.script_dir / "stress_test_logs"

    ## questa funzione è inutile, bisogna far si che run_parallel_tests accetti 1 come valore per il numero di processi da far girare

    def run_stress_test(
        self, num_tests: int, extra_args: list = None, parallel: int = 1
    ):
        """Esegue stress test."""
        if parallel > 1:
            self.run_parallel_tests(num_tests, parallel, extra_args)
        else:
            print(f"🔄 Esecuzione di {num_tests} test...")
            print()

            cmd = [
                sys.executable,
                str(self.script_dir / "stress_test_v2.py"),
                "-n",
                str(num_tests),
            ]

            if extra_args:
                cmd.extend(extra_args)

            result = subprocess.run(cmd)

            if result.returncode == 0:
                print()
                print(f"✓ Test completati!")
                print(f"Controlla i risultati in: {self.log_dir}")
            else:
                print()
                print(f"✗ Errore durante l'esecuzione dei test")
                sys.exit(1)

    ## questa funzione contiene dei print() che non vanno bene se vuoi andare a capo usa \n
    ## impostare none a list non è corretto
    ## a cosa serve remaining_test? togli quella parte, se si fa un test in meno pace
    ## questi seed vanno semplicemente tolti non funzionano
    ## evita di generare codice in eccesso, per esempio non indicare all'utente quale sia la cartella dei log in continuazione è noto togli quel print

    def run_parallel_tests(
        self, total_tests: int, num_processes: int, extra_args: list = None
    ):
        """Esegue test in parallelo su più processi."""
        tests_per_process = total_tests // num_processes
        remaining_tests = total_tests % num_processes

        print(
            f"🔄 Esecuzione di {total_tests} test su {num_processes} processi paralleli"
        )
        print(f"   {tests_per_process} test per processo", end="")
        if remaining_tests > 0:
            print(f" (+{remaining_tests} extra)")
        else:
            print()
        print()

        processes = []

        # Avvia i processi
        for i in range(num_processes):
            # Distribuisci i test rimanenti sui primi processi
            num_tests = tests_per_process + (1 if i < remaining_tests else 0)

            if num_tests == 0:
                continue

            # Seed casuale per ogni processo
            seed = random.randint(1, 999999)

            cmd = [
                sys.executable,
                str(self.script_dir / "stress_test_v2.py"),
                "-n",
                str(num_tests),
                "--seed",
                str(seed),
            ]

            if extra_args:
                cmd.extend(extra_args)

            print(f"  [Processo {i + 1}] Avvio {num_tests} test con seed {seed}...")
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            processes.append((i + 1, process, num_tests))

        print()
        print("Attendi completamento dei processi...")
        print()

        # Attendi che tutti i processi terminino
        failed = False
        for proc_id, process, num_tests in processes:
            returncode = process.wait()

            if returncode == 0:
                print(f"  ✓ [Processo {proc_id}] Completato ({num_tests} test)")
            else:
                print(f"  ✗ [Processo {proc_id}] Errore ({num_tests} test)")
                failed = True

        print()
        if not failed:
            print(f"✓ Tutti i test completati!")
            print(f"Controlla i risultati in: {self.log_dir}")
        else:
            print(f"⚠ Alcuni processi hanno riportato errori")
            print(f"Controlla i risultati in: {self.log_dir}")

    ## elimina questa funzione, non va

    def run_replay(self, log_file: str, extra_args: list = None):
        """Esegue replay di una partita."""
        log_path = Path(log_file)

        if not log_path.exists():
            print(f"✗ File non trovato: {log_file}")
            sys.exit(1)

        print(f"🔄 Replay di: {log_file}")
        print()

        cmd = [sys.executable, str(self.script_dir / "replay_game.py"), str(log_path)]

        if extra_args:
            cmd.extend(extra_args)

        subprocess.run(cmd)

    ## cosa fa questa funzione? è un duplicato della precedente eliminala

    def analyze_log(self, log_file: str):
        """Analizza un file di log."""
        log_path = Path(log_file)

        if not log_path.exists():
            print(f"✗ File non trovato: {log_file}")
            sys.exit(1)

        print(f"📊 Analisi di: {log_file}")
        print()

        cmd = [
            sys.executable,
            str(self.script_dir / "replay_game.py"),
            str(log_path),
            "--analyze-only",
        ]

        subprocess.run(cmd)

    ## questa funzione può essere eliminata

    def find_errors(self):
        """Trova tutti i log con errori."""
        print("🔍 Ricerca log con errori...")
        print()

        if not self.log_dir.exists():
            print("✗ Directory log non trovata")
            return

        error_count = 0
        total_count = 0

        for log_file in sorted(self.log_dir.glob("*.json")):
            if "summary" in log_file.name:
                continue

            total_count += 1

            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                if data.get("errors"):
                    error_count += 1
                    error_type = data["errors"][0].get("type", "Unknown")

                    print(f"✗ {log_file.name}")
                    print(f"  Tipo errore: {error_type}")
                    print(f"  Path: {log_file}")
                    print()

            except Exception as e:
                print(f"⚠ Errore leggendo {log_file.name}: {e}")

        print("Scansione completata")
        print(f"Log totali: {total_count}")
        print(f"Con errori: {error_count}")

        if error_count > 0:
            print()
            print(f"💡 Usa 'python test_runner.py replay <log_file>' per rigiocare")

    ## questa pure, non ha a che fare un lo scopo dello script

    def show_stats(self):
        """Mostra statistiche sui test."""
        print("�� Statistiche test eseguiti")
        print()

        if not self.log_dir.exists():
            print("✗ Nessun test eseguito ancora")
            return

        total_logs = 0
        error_logs = 0

        for log_file in self.log_dir.glob("*.json"):
            if "summary" in log_file.name:
                continue

            total_logs += 1

            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if data.get("errors"):
                        error_logs += 1
            except:
                pass

        success_logs = total_logs - error_logs

        print(f"Test totali eseguiti: {total_logs}")
        print(f"Successi: {success_logs}")
        print(f"Con errori: {error_logs}")

        if total_logs > 0:
            success_rate = success_logs / total_logs * 100
            print(f"Tasso di successo: {success_rate:.1f}%")

        # Ultimi summary
        print()
        print("Ultimi 5 summary:")
        summaries = sorted(
            self.log_dir.glob("summary_*.txt"),
            key=lambda x: x.stat().st_mtime,
            reverse=True,
        )[:5]

        for summary in summaries:
            print(f"  • {summary.name}")

    ## pure questa la possiamo eliminare

    def clean_logs(self):
        """Pulisce i file di log."""
        print("🧹 Pulizia log...")

        if not self.log_dir.exists():
            print("Nessun log da pulire")
            return

        response = input("Sei sicuro di voler cancellare tutti i log? [y/N] ")

        if response.lower() == "y":
            import shutil

            shutil.rmtree(self.log_dir)
            print("✓ Log cancellati")
        else:
            print("Operazione annullata")


## anche qui troppi print, toglili e usare \n
## togli questa cosa di aver test intensive, quick e medium non ha senso è sempre lo stesso test
## anche overnight e seed devono sparire, replay pure
## togli tutti questi esempi e spiega all'utente quali sono i paremtri solo se passa --help
## ci devono essere dei parametri di default che l'utente può sovrascrivere e basta, nessuna modalità speciale


def main():
    """Entry point principale."""
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║           PyazzaMarket Stress Test Runner                          ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print()

    parser = argparse.ArgumentParser(
        description="Test runner per PyazzaMarket",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi d'uso:
  python test_runner.py quick                              # 10 test rapidi
  python test_runner.py quick -j 4 --max-turns 1000        # 10 test su 4 processi, max 1000 turni
  python test_runner.py seed 12345                         # Test con seed specifico
  python test_runner.py intensive --headless               # 100 test senza GUI
  python test_runner.py intensive --fps 240 --max-turns 800 # 100 test a 240 FPS, max 800 turni
  python test_runner.py intensive -j 8 --fps 240           # 100 test su 8 processi in parallelo
  python test_runner.py find-errors                        # Trova log con errori
  python test_runner.py replay logs/game.json              # Replay di una partita
  python test_runner.py stats                              # Mostra statistiche
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Comando da eseguire")

    # Quick test
    quick = subparsers.add_parser("quick", help="Esegui 10 test rapidi")
    quick.add_argument(
        "--fps", type=int, default=60, help="FPS del gioco (default: 60)"
    )
    quick.add_argument(
        "--max-turns",
        type=int,
        default=500,
        help="Numero massimo di turni (default: 500)",
    )
    quick.add_argument(
        "-j",
        "--parallel",
        type=int,
        default=1,
        help="Numero di processi paralleli (default: 1)",
    )

    # Medium test
    medium = subparsers.add_parser("medium", help="Esegui 50 test")
    medium.add_argument(
        "--fps", type=int, default=60, help="FPS del gioco (default: 60)"
    )
    medium.add_argument(
        "--max-turns",
        type=int,
        default=500,
        help="Numero massimo di turni (default: 500)",
    )
    medium.add_argument(
        "-j",
        "--parallel",
        type=int,
        default=1,
        help="Numero di processi paralleli (default: 1)",
    )

    # Intensive test
    intensive = subparsers.add_parser("intensive", help="Esegui 100 test")
    intensive.add_argument("--headless", action="store_true", help="Senza GUI")
    intensive.add_argument(
        "--fps", type=int, default=60, help="FPS del gioco (default: 60)"
    )
    intensive.add_argument(
        "--max-turns",
        type=int,
        default=500,
        help="Numero massimo di turni (default: 500)",
    )
    intensive.add_argument(
        "-j",
        "--parallel",
        type=int,
        default=1,
        help="Numero di processi paralleli (default: 1)",
    )

    # Overnight test
    overnight = subparsers.add_parser("overnight", help="Esegui 1000 test")
    overnight.add_argument("--headless", action="store_true", help="Senza GUI")
    overnight.add_argument(
        "--fps", type=int, default=60, help="FPS del gioco (default: 60)"
    )
    overnight.add_argument(
        "--max-turns",
        type=int,
        default=500,
        help="Numero massimo di turni (default: 500)",
    )
    overnight.add_argument(
        "-j",
        "--parallel",
        type=int,
        default=1,
        help="Numero di processi paralleli (default: 1)",
    )

    # Seed test
    seed = subparsers.add_parser("seed", help="Test con seed specifico")
    seed.add_argument("seed_value", type=int, help="Valore del seed")
    seed.add_argument("--headless", action="store_true", help="Senza GUI")
    seed.add_argument("--fps", type=int, default=60, help="FPS del gioco (default: 60)")
    seed.add_argument(
        "--max-turns",
        type=int,
        default=500,
        help="Numero massimo di turni (default: 500)",
    )

    # Replay
    replay = subparsers.add_parser("replay", help="Replay di una partita")
    replay.add_argument("log_file", help="File di log da rigiocare")
    replay.add_argument(
        "-s", "--step-by-step", action="store_true", help="Modalità step-by-step"
    )
    replay.add_argument("--headless", action="store_true", help="Senza GUI")

    # Analyze
    analyze = subparsers.add_parser("analyze", help="Analizza un log")
    analyze.add_argument("log_file", help="File di log da analizzare")

    # Find errors
    subparsers.add_parser("find-errors", help="Trova log con errori")

    # Stats
    subparsers.add_parser("stats", help="Mostra statistiche")

    # Clean
    subparsers.add_parser("clean", help="Pulisci i log")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    runner = TestRunner()

    # Esegui comando
    if args.command == "quick":
        extra = []
        if hasattr(args, "fps"):
            extra.extend(["--fps", str(args.fps)])
        if hasattr(args, "max_turns"):
            extra.extend(["--max-turns", str(args.max_turns)])
        parallel = args.parallel if hasattr(args, "parallel") else 1
        runner.run_stress_test(10, extra, parallel)

    elif args.command == "medium":
        extra = []
        if hasattr(args, "fps"):
            extra.extend(["--fps", str(args.fps)])
        if hasattr(args, "max_turns"):
            extra.extend(["--max-turns", str(args.max_turns)])
        parallel = args.parallel if hasattr(args, "parallel") else 1
        runner.run_stress_test(50, extra, parallel)

    elif args.command == "intensive":
        extra = []
        if args.headless:
            extra.append("--headless")
        if hasattr(args, "fps"):
            extra.extend(["--fps", str(args.fps)])
        if hasattr(args, "max_turns"):
            extra.extend(["--max-turns", str(args.max_turns)])
        parallel = args.parallel if hasattr(args, "parallel") else 1
        runner.run_stress_test(100, extra, parallel)

    elif args.command == "overnight":
        extra = []
        if args.headless:
            extra.append("--headless")
        if hasattr(args, "fps"):
            extra.extend(["--fps", str(args.fps)])
        if hasattr(args, "max_turns"):
            extra.extend(["--max-turns", str(args.max_turns)])
        parallel = args.parallel if hasattr(args, "parallel") else 1
        runner.run_stress_test(1000, extra, parallel)

    elif args.command == "seed":
        extra = ["--seed", str(args.seed_value)]
        if args.headless:
            extra.append("--headless")
        if hasattr(args, "fps"):
            extra.extend(["--fps", str(args.fps)])
        if hasattr(args, "max_turns"):
            extra.extend(["--max-turns", str(args.max_turns)])
        runner.run_stress_test(1, extra)

    elif args.command == "replay":
        extra = []
        if args.step_by_step:
            extra.append("-s")
        if args.headless:
            extra.append("--headless")
        runner.run_replay(args.log_file, extra)

    elif args.command == "analyze":
        runner.analyze_log(args.log_file)

    elif args.command == "find-errors":
        runner.find_errors()

    elif args.command == "stats":
        runner.show_stats()

    elif args.command == "clean":
        runner.clean_logs()


if __name__ == "__main__":
    main()
