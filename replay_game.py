"""
Sistema di replay per riprodurre partite da log.
Permette di debuggare errori rieseguendo esattamente la stessa sequenza di eventi.
"""

import os
import sys
import json
import pygame
import argparse
from typing import Dict, Any, List

sys.path.insert(0, os.path.dirname(__file__))

from lib.game import Game
from lib.game_logger import GameLogger
from lib.seeded_random import SeededRandom, DiceController, EventController
from lib.constants import WIDTH, HEIGHT


class GameReplayer:
    """Rigioca una partita da un file di log."""

    def __init__(self, log_file: str, pause_on_error: bool = True,
                 step_by_step: bool = False, headless: bool = False):
        """
        Inizializza il replayer.

        Args:
            log_file: Path al file di log da rigiocare
            pause_on_error: Se True, ferma l'esecuzione quando raggiunge un errore
            step_by_step: Se True, procede turno per turno aspettando input
            headless: Se True, esegue senza GUI
        """
        self.log_file = log_file
        self.pause_on_error = pause_on_error
        self.step_by_step = step_by_step
        self.headless = headless

        # Carica il log
        print(f"Caricamento log da: {log_file}")
        self.log_data = GameLogger.load_log(log_file)

        # Estrai informazioni
        self.seed = self.log_data.get("seed")
        self.initial_state = self.log_data.get("initial_state", {})
        self.actions = self.log_data.get("actions", [])
        self.errors = self.log_data.get("errors", [])

        print(f"Seed: {self.seed}")
        print(f"Azioni registrate: {len(self.actions)}")
        print(f"Errori registrati: {len(self.errors)}")

        if self.errors:
            print("\n⚠ ATTENZIONE: Questo log contiene errori!")
            for i, error in enumerate(self.errors, 1):
                print(f"  {i}. {error['type']}: {error['message']}")
                print(f"     Al turno: {error.get('action_count', 'N/A')}")

    def replay(self):
        """Esegue il replay della partita."""
        print("\n" + "="*80)
        print("INIZIO REPLAY")
        print("="*80 + "\n")

        if self.step_by_step:
            print("Modalità STEP-BY-STEP attiva")
            print("Premi INVIO per avanzare al prossimo turno, 'q' per uscire\n")

        # Inizializza pygame
        if not pygame.get_init():
            pygame.init()

        clock = pygame.time.Clock()

        # Ricrea i giocatori dallo stato iniziale
        players = self.initial_state.get("players", [])
        if not players:
            print("⚠ Nessun giocatore trovato nello stato iniziale!")
            from lib.constants import CAR_RED, CAR_BLUE
            players = [
                {"name": "Bot1", "color": CAR_RED, "bot": True},
                {"name": "Bot2", "color": CAR_BLUE, "bot": True}
            ]

        print(f"Giocatori: {[p['name'] for p in players]}")

        # Estrai i lanci di dadi dalle azioni
        dice_rolls = self.extract_dice_rolls()
        print(f"Lanci di dadi estratti: {len(dice_rolls)}")

        # Crea il gioco con lo stesso seed
        seeded_random = SeededRandom(self.seed)
        dice_controller = DiceController(seeded_random, dice_rolls)
        event_controller = EventController(seeded_random)

        game = Game(WIDTH, HEIGHT, clock, players, test=False, gui=not self.headless)

        # Inietta i controller
        game.dice_controller = dice_controller
        game.event_controller = event_controller

        # Reshuffle events con lo stesso seed
        if hasattr(game, 'events'):
            game.events = game.event_controller.shuffle_events(game.events)

        # Cerca l'azione dove è avvenuto l'errore
        error_action_count = None
        if self.errors:
            error_action_count = self.errors[0].get('action_count')
            print(f"\n⚠ Errore previsto all'azione #{error_action_count}")

        # Esegui il replay
        turn_count = 0
        max_turns = 1000  # Safety limit

        try:
            while turn_count < max_turns and len(game.get_players()) > 1:
                turn_count += 1

                # Check se siamo vicini all'errore
                if error_action_count and turn_count >= error_action_count - 5:
                    print(f"\n⚠ Avvicinamento all'errore (turno {turn_count})")

                current_player = game.get_current_player()

                if self.step_by_step:
                    user_input = input(f"\nTurno {turn_count} - {current_player.get_name()} >>> ")
                    if user_input.lower() == 'q':
                        print("Replay interrotto dall'utente")
                        break
                else:
                    # Mostra progresso ogni 10 turni
                    if turn_count % 10 == 0:
                        print(f"Turno {turn_count}...")

                # Esegui il turno
                self.execute_replay_turn(game, turn_count)

                # Check se abbiamo raggiunto l'errore
                if self.pause_on_error and error_action_count and turn_count >= error_action_count:
                    print(f"\n{'='*80}")
                    print(f"⚠ PUNTO DI ERRORE RAGGIUNTO (turno {turn_count})")
                    print(f"{'='*80}")
                    print("\nStato del gioco:")
                    self.print_game_state(game)

                    if self.step_by_step:
                        input("\nPremi INVIO per continuare oltre l'errore...")
                    else:
                        print("\nContinuo l'esecuzione per verificare se l'errore si ripresenta...")

                # Processa eventi pygame
                if not self.headless:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            game.running = False
                            return

                # Vittoria
                if len(game.get_players()) == 1:
                    print(f"\n{'='*80}")
                    print(f"PARTITA TERMINATA al turno {turn_count}")
                    print(f"Vincitore: {game.get_players()[0].get_name()}")
                    print(f"{'='*80}")
                    break

        except Exception as e:
            print(f"\n{'='*80}")
            print(f"✗ ERRORE DURANTE IL REPLAY AL TURNO {turn_count}")
            print(f"{'='*80}")
            print(f"Tipo: {type(e).__name__}")
            print(f"Messaggio: {str(e)}")
            print(f"\nStato del gioco al momento dell'errore:")
            self.print_game_state(game)

            import traceback
            print(f"\nStack trace:")
            traceback.print_exc()

            # Confronta con l'errore originale
            if self.errors:
                original_error = self.errors[0]
                print(f"\n{'='*80}")
                print(f"ERRORE ORIGINALE:")
                print(f"{'='*80}")
                print(f"Tipo: {original_error['type']}")
                print(f"Messaggio: {original_error['message']}")
                print(f"Azione: {original_error.get('action_count', 'N/A')}")

                if original_error['type'] == type(e).__name__:
                    print(f"\n✓ L'errore è stato RIPRODOTTO con successo!")
                else:
                    print(f"\n⚠ L'errore è DIVERSO dall'originale")

            return

        print(f"\n{'='*80}")
        print(f"REPLAY COMPLETATO")
        print(f"{'='*80}")
        print(f"Turni eseguiti: {turn_count}")

        if self.errors and not self.pause_on_error:
            print(f"\n⚠ Il log originale conteneva errori ma il replay è andato a buon fine")
            print(f"   Questo potrebbe indicare un bug non deterministico o già fixato")

    def execute_replay_turn(self, game: Game, turn_num: int):
        """
        Esegue un turno in modalità replay.

        Args:
            game: Istanza del gioco
            turn_num: Numero del turno
        """
        current_player = game.get_current_player()

        # Usa il dice controller per ottenere i dadi registrati
        if hasattr(game, 'dice_controller'):
            dice_roll = game.dice_controller.roll()
            game._Game__test = True
            game._Game__test_dice = dice_roll

            if self.step_by_step or turn_num % 10 == 0:
                print(f"  Dadi: {dice_roll[0]} + {dice_roll[1]} = {sum(dice_roll)}")

        # Esegui il turno
        game.turn()

        # Auto-gestisci UI
        self.auto_handle_ui(game)

    def auto_handle_ui(self, game: Game):
        """Gestisce automaticamente UI panels ed eventi."""
        # Chiudi alert
        if hasattr(game, '_Game__alert_messages') and game._Game__alert_messages:
            game._Game__alert_messages.clear()

        # Passa turno se possibile
        if hasattr(game, '_Game__actions_status'):
            actions = game._Game__actions_status
            if hasattr(actions, 'can_pass_turn') and actions.can_pass_turn():
                current_index = game.get_current_player_index()
                game.set_current_player_index(
                    (current_index + 1) % len(game.get_players())
                )

    def extract_dice_rolls(self) -> List[tuple]:
        """Estrae tutti i lanci di dadi dalle azioni registrate."""
        rolls = []
        for action in self.actions:
            if action.get("category") == "dice_roll" and action.get("type") == "roll":
                data = action.get("data", {})
                dice1 = data.get("dice1")
                dice2 = data.get("dice2")
                if dice1 and dice2:
                    rolls.append((dice1, dice2))
        return rolls

    def print_game_state(self, game: Game):
        """Stampa lo stato corrente del gioco."""
        print(f"\nGiocatore corrente: {game.get_current_player().get_name()}")
        print(f"Bilancio piazza: {game.get_square_balance()}")
        print(f"\nStato giocatori:")
        for p in game.get_players():
            print(f"  • {p.get_name()}:")
            print(f"      Posizione: {p.get_position()}")
            print(f"      Bilancio: {p.get_balance()}")
            print(f"      Cedole: {len(p.get_stocks())}")
            if p.is_in_debt():
                print(f"      ⚠ IN DEBITO!")

    def analyze_log(self):
        """Analizza il log e stampa statistiche utili."""
        print("\n" + "="*80)
        print("ANALISI LOG")
        print("="*80 + "\n")

        # Conta azioni per categoria
        action_counts = {}
        for action in self.actions:
            category = action.get("category", "unknown")
            action_counts[category] = action_counts.get(category, 0) + 1

        print("Azioni per categoria:")
        for category, count in sorted(action_counts.items(), key=lambda x: -x[1]):
            print(f"  {category}: {count}")

        # Analizza eventi
        events_triggered = [
            a for a in self.actions
            if a.get("category") == "event"
        ]
        print(f"\nEventi triggherati: {len(events_triggered)}")

        # Analizza bancarotte
        bankruptcies = [
            a for a in self.actions
            if a.get("type") == "player_eliminated"
        ]
        if bankruptcies:
            print(f"\nBancarotte: {len(bankruptcies)}")
            for b in bankruptcies:
                data = b.get("data", {})
                print(f"  • {data.get('player')} - Debito: {data.get('debt')}")

        # Analizza errori in dettaglio
        if self.errors:
            print(f"\n{'='*80}")
            print("DETTAGLI ERRORI")
            print("="*80)
            for i, error in enumerate(self.errors, 1):
                print(f"\nErrore #{i}:")
                print(f"  Tipo: {error['type']}")
                print(f"  Messaggio: {error['message']}")
                print(f"  Azione: {error.get('action_count', 'N/A')}")
                print(f"  Timestamp: {error.get('timestamp', 'N/A')}")

                # Mostra stato al momento dell'errore
                if 'game_state' in error and error['game_state']:
                    state = error['game_state']
                    print(f"\n  Stato al momento dell'errore:")
                    if 'current_player_index' in state:
                        print(f"    Indice giocatore: {state['current_player_index']}")
                    if 'players' in state:
                        print(f"    Giocatori attivi: {len(state['players'])}")


def main():
    """Entry point principale."""
    parser = argparse.ArgumentParser(
        description="Replay di partite da log per debugging",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi d'uso:
  # Replay normale
  python replay_game.py logs/stress_test_0001_seed_12345.json

  # Replay step-by-step (turno per turno)
  python replay_game.py -s logs/stress_test_0001_seed_12345.json

  # Solo analisi del log senza replay
  python replay_game.py -a logs/stress_test_0001_seed_12345.json

  # Replay headless (senza GUI, più veloce)
  python replay_game.py --headless logs/stress_test_0001_seed_12345.json
        """
    )

    parser.add_argument(
        "log_file",
        help="Path al file di log da rigiocare"
    )
    parser.add_argument(
        "-s", "--step-by-step",
        action="store_true",
        help="Procedi turno per turno aspettando input"
    )
    parser.add_argument(
        "-a", "--analyze-only",
        action="store_true",
        help="Solo analisi del log senza replay"
    )
    parser.add_argument(
        "--no-pause",
        action="store_true",
        help="Non fermare l'esecuzione quando raggiunge l'errore"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Esegui senza GUI"
    )

    args = parser.parse_args()

    if not os.path.exists(args.log_file):
        print(f"✗ File non trovato: {args.log_file}")
        sys.exit(1)

    replayer = GameReplayer(
        args.log_file,
        pause_on_error=not args.no_pause,
        step_by_step=args.step_by_step,
        headless=args.headless
    )

    if args.analyze_only:
        replayer.analyze_log()
    else:
        replayer.replay()


if __name__ == "__main__":
    main()
