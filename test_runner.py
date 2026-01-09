#!/usr/bin/env python3
"""
Cross-platform test runner per PyazzaMarket.
Alternativa Python allo script bash, funziona su Windows/Linux/Mac.
"""

import os
import sys
import glob
import json
import argparse
import subprocess
from pathlib import Path


class TestRunner:
    """Runner cross-platform per stress test."""

    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.log_dir = self.script_dir / "stress_test_logs"

    def run_stress_test(self, num_tests: int, extra_args: list = None):
        """Esegue stress test."""
        print(f"🔄 Esecuzione di {num_tests} test...")
        print()

        cmd = [
            sys.executable,
            str(self.script_dir / "stress_test.py"),
            "-n", str(num_tests)
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

    def run_replay(self, log_file: str, extra_args: list = None):
        """Esegue replay di una partita."""
        log_path = Path(log_file)

        if not log_path.exists():
            print(f"✗ File non trovato: {log_file}")
            sys.exit(1)

        print(f"🔄 Replay di: {log_file}")
        print()

        cmd = [
            sys.executable,
            str(self.script_dir / "replay_game.py"),
            str(log_path)
        ]

        if extra_args:
            cmd.extend(extra_args)

        subprocess.run(cmd)

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
            "--analyze-only"
        ]

        subprocess.run(cmd)

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
                with open(log_file, 'r', encoding='utf-8') as f:
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
                with open(log_file, 'r', encoding='utf-8') as f:
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
            reverse=True
        )[:5]

        for summary in summaries:
            print(f"  • {summary.name}")

    def clean_logs(self):
        """Pulisce i file di log."""
        print("🧹 Pulizia log...")

        if not self.log_dir.exists():
            print("Nessun log da pulire")
            return

        response = input("Sei sicuro di voler cancellare tutti i log? [y/N] ")

        if response.lower() == 'y':
            import shutil
            shutil.rmtree(self.log_dir)
            print("✓ Log cancellati")
        else:
            print("Operazione annullata")


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
  python test_runner.py quick                 # 10 test rapidi
  python test_runner.py seed 12345            # Test con seed specifico
  python test_runner.py intensive --headless  # 100 test senza GUI
  python test_runner.py find-errors           # Trova log con errori
  python test_runner.py replay logs/game.json # Replay di una partita
  python test_runner.py stats                 # Mostra statistiche
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Comando da eseguire')

    # Quick test
    subparsers.add_parser('quick', help='Esegui 10 test rapidi')

    # Medium test
    subparsers.add_parser('medium', help='Esegui 50 test')

    # Intensive test
    intensive = subparsers.add_parser('intensive', help='Esegui 100 test')
    intensive.add_argument('--headless', action='store_true', help='Senza GUI')

    # Overnight test
    overnight = subparsers.add_parser('overnight', help='Esegui 1000 test')
    overnight.add_argument('--headless', action='store_true', help='Senza GUI')

    # Seed test
    seed = subparsers.add_parser('seed', help='Test con seed specifico')
    seed.add_argument('seed_value', type=int, help='Valore del seed')
    seed.add_argument('--headless', action='store_true', help='Senza GUI')

    # Replay
    replay = subparsers.add_parser('replay', help='Replay di una partita')
    replay.add_argument('log_file', help='File di log da rigiocare')
    replay.add_argument('-s', '--step-by-step', action='store_true',
                       help='Modalità step-by-step')
    replay.add_argument('--headless', action='store_true', help='Senza GUI')

    # Analyze
    analyze = subparsers.add_parser('analyze', help='Analizza un log')
    analyze.add_argument('log_file', help='File di log da analizzare')

    # Find errors
    subparsers.add_parser('find-errors', help='Trova log con errori')

    # Stats
    subparsers.add_parser('stats', help='Mostra statistiche')

    # Clean
    subparsers.add_parser('clean', help='Pulisci i log')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    runner = TestRunner()

    # Esegui comando
    if args.command == 'quick':
        runner.run_stress_test(10)

    elif args.command == 'medium':
        runner.run_stress_test(50)

    elif args.command == 'intensive':
        extra = ['--headless'] if args.headless else []
        runner.run_stress_test(100, extra)

    elif args.command == 'overnight':
        extra = ['--headless'] if args.headless else []
        runner.run_stress_test(1000, extra)

    elif args.command == 'seed':
        extra = ['--seed', str(args.seed_value)]
        if args.headless:
            extra.append('--headless')
        runner.run_stress_test(1, extra)

    elif args.command == 'replay':
        extra = []
        if args.step_by_step:
            extra.append('-s')
        if args.headless:
            extra.append('--headless')
        runner.run_replay(args.log_file, extra)

    elif args.command == 'analyze':
        runner.analyze_log(args.log_file)

    elif args.command == 'find-errors':
        runner.find_errors()

    elif args.command == 'stats':
        runner.show_stats()

    elif args.command == 'clean':
        runner.clean_logs()


if __name__ == "__main__":
    main()
