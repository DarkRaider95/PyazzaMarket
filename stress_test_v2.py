"""
Stress tester v2 per PyazzaMarket.
Versione ottimizzata senza multithreading e basata su frame invece di sleep.
"""

import os
import sys
import pygame
import pygame_gui
import argparse
import traceback
import time
from datetime import datetime
from typing import Optional, List, Dict, Any

# Aggiungi la directory lib al path
sys.path.insert(0, os.path.dirname(__file__))

from lib.game import Game
from lib.game_logger import GameLogger
from lib.seeded_random import SeededRandom, DiceController, EventController
from lib.constants import WIDTH, HEIGHT, CAR_RED, CAR_BLUE, CAR_BLACK, CAR_YELLOW


class StressTestRunnerV2:
    """Esegue stress test automatici del gioco usando frame-based timing."""

    def __init__(self, num_tests: int = 1, seed: Optional[int] = None,
                 max_turns: int = 500, fps: int = 120):
        """
        Inizializza lo stress tester.

        Args:
            num_tests: Numero di test da eseguire
            seed: Seed iniziale (incrementato per ogni test)
            max_turns: Numero massimo di turni per partita
            fps: Framerate del gioco (più alto = più veloce)
        """
        self.num_tests = num_tests
        self.base_seed = seed if seed is not None else int(time.time() * 1000) % (2**32)
        self.max_turns = max_turns
        self.fps = fps
        self.results = []

        # Crea directory per logs
        self.log_dir = "stress_test_logs"
        os.makedirs(self.log_dir, exist_ok=True)

        # Summary file
        self.summary_file = os.path.join(
            self.log_dir,
            f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

    def run_all_tests(self):
        """Esegue tutti i test configurati."""
        print(f"╔{'═'*78}╗")
        print(f"║ PyazzaMarket Stress Test Runner V2{' '*42}║")
        print(f"║ Esecuzione di {self.num_tests} test{'s' if self.num_tests > 1 else ''}{' '*(60-len(str(self.num_tests)))}║")
        print(f"║ Seed base: {self.base_seed}{' '*(63-len(str(self.base_seed)))}║")
        print(f"║ FPS: {self.fps}{' '*(70-len(str(self.fps)))}║")
        print(f"╚{'═'*78}╝")
        print()

        start_time = time.time()

        for test_num in range(1, self.num_tests + 1):
            test_seed = self.base_seed + test_num - 1
            print(f"\n{'='*80}")
            print(f"Test {test_num}/{self.num_tests} - Seed: {test_seed}")
            print(f"{'='*80}")

            try:
                result = self.run_single_test(test_seed, test_num)
                self.results.append(result)

                # Stampa risultato
                status_symbol = "✓" if result["status"] == "success" else "✗"
                print(f"\n{status_symbol} Test {test_num} completato: {result['status']}")
                print(f"  Turni: {result['turns']}")
                print(f"  Durata: {result['duration']:.2f}s")

                if result["status"] == "error":
                    print(f"  ⚠ Errore: {result['error_type']}")
                    print(f"  Log: {result['log_file']}")

            except Exception as e:
                print(f"\n✗ Test {test_num} FALLITO COMPLETAMENTE")
                print(f"  Errore critico: {str(e)}")
                traceback.print_exc()

                self.results.append({
                    "test_num": test_num,
                    "seed": test_seed,
                    "status": "critical_failure",
                    "error": str(e),
                    "traceback": traceback.format_exc()
                })

        elapsed_time = time.time() - start_time

        # Genera summary
        self.generate_summary(elapsed_time)

    def run_single_test(self, seed: int, test_num: int) -> Dict[str, Any]:
        """
        Esegue un singolo test.

        Args:
            seed: Seed per questo test
            test_num: Numero del test

        Returns:
            Dizionario con risultati del test
        """
        session_name = f"stress_test_{test_num:04d}_seed_{seed}"
        logger = GameLogger(log_dir=self.log_dir, session_name=session_name)
        logger.set_seed(seed)

        # Inizializza pygame
        if not pygame.get_init():
            pygame.init()

        clock = pygame.time.Clock()

        # Crea giocatori bot
        players = [
            {"name": "Bot1", "color": CAR_RED, "bot": True},
            {"name": "Bot2", "color": CAR_BLUE, "bot": True},
            {"name": "Bot3", "color": CAR_BLACK, "bot": True},
            {"name": "Bot4", "color": CAR_YELLOW, "bot": True}
        ]

        logger.set_initial_state(
            players,
            {"cells": 40, "start_balance": 1500}
        )

        start_time = time.time()
        result = {
            "test_num": test_num,
            "seed": seed,
            "log_file": logger.log_file,
            "turns": 0,
            "status": "unknown"
        }

        try:
            # Crea e configura il gioco per stress test
            game = self.create_test_game(
                WIDTH, HEIGHT, clock, players,
                seed, logger
            )

            # Esegui il gioco
            turn_count = self.run_game_automated(game, logger, self.max_turns)

            result["turns"] = turn_count
            result["status"] = "success"
            result["winner"] = game.get_players()[0].get_name() if len(game.get_players()) == 1 else None

            logger.log_game_end(
                result["winner"],
                "completed" if turn_count < self.max_turns else "max_turns_reached",
                self.get_game_state(game)
            )

        except Exception as e:
            result["status"] = "error"
            result["error_type"] = type(e).__name__
            result["error_message"] = str(e)

            # Log l'errore
            logger.log_error(
                type(e).__name__,
                str(e),
                traceback.format_exc(),
                self.get_game_state(game) if 'game' in locals() else {}
            )

            print(f"\n⚠ ERRORE TROVATO!")
            print(f"  Tipo: {type(e).__name__}")
            print(f"  Messaggio: {str(e)}")
            print(f"  Turno: {result['turns']}")

        finally:
            result["duration"] = time.time() - start_time

        return result

    def create_test_game(self, width: int, height: int, clock, players: List[Dict],
                        seed: int, logger: GameLogger) -> Game:
        """
        Crea un'istanza del gioco configurata per lo stress test.

        Args:
            width: Larghezza finestra
            height: Altezza finestra
            clock: Clock di pygame
            players: Lista giocatori
            seed: Seed per random
            logger: Logger del gioco

        Returns:
            Istanza di Game configurata
        """
        game = Game(width, height, clock, players, test=False, gui=True, disable_integrated_bot=True)

        # Inietta il logger nel gioco
        game.logger = logger

        # Inietta controller seeded per dadi ed eventi
        seeded_random = SeededRandom(seed)
        game.dice_controller = DiceController(seeded_random)
        game.event_controller = EventController(seeded_random)

        # Sovrascrivi il metodo events shuffle
        if hasattr(game, 'events'):
            game.events = game.event_controller.shuffle_events(game.events)

        return game

    def run_game_automated(self, game: Game, logger: GameLogger, max_turns: int) -> int:
        """
        Esegue il gioco in modalità automatica simulando click e interazioni.
        Usa frame-based timing invece di sleep.

        Args:
            game: Istanza del gioco
            logger: Logger
            max_turns: Numero massimo di turni

        Returns:
            Numero di turni eseguiti
        """
        turn_count = 0
        frame_count = 0
        game_started = False
        dice_launched = False

        # Frames da aspettare tra le azioni (configurabile via FPS)
        frames_between_actions = max(1, self.fps // 10)  # ~0.1s a 60fps, più veloce a fps più alti

        # Inizializza la grafica
        game.init_graphics()

        # Loop principale del gioco
        while game.running and turn_count < max_turns:
            frame_count += 1

            # Raccogli eventi pygame
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    game.running = False
                    break

            # Processa il frame del gioco
            time_delta = 1.0 / self.fps
            game.process_frame(events, time_delta)

            # Fase iniziale: gestione dice overlay per ordine turni
            if not game_started:
                if not hasattr(game, 'dice_overlay'):
                    game_started = True
                elif not game.dice_overlay.overlay_on():
                    # Tutti hanno tirato, chiudi overlay
                    if hasattr(game.dice_overlay, 'closeDiceOverlayBut'):
                        logger.log_action("bot", "dice_overlay_close", {"reason": "all_players_rolled"})
                        click_event = pygame.event.Event(
                            pygame_gui.UI_BUTTON_PRESSED,
                            {'ui_element': game.dice_overlay.closeDiceOverlayBut}
                        )
                        pygame.event.post(click_event)
                        game_started = True
                else:
                    # Gestisci lanci dei dadi per ordine turni solo ogni N frames
                    if frame_count % frames_between_actions == 0:
                        if not dice_launched:
                            # Lancia i dadi
                            if hasattr(game.dice_overlay, 'launchOverlayDiceBut'):
                                logger.log_action("bot", "dice_overlay_launch", {"phase": "turn_order"})
                                click_event = pygame.event.Event(
                                    pygame_gui.UI_BUTTON_PRESSED,
                                    {'ui_element': game.dice_overlay.launchOverlayDiceBut}
                                )
                                pygame.event.post(click_event)
                                dice_launched = True
                        else:
                            # Chiudi per passare al prossimo
                            if hasattr(game.dice_overlay, 'closeDiceOverlayBut'):
                                logger.log_action("bot", "dice_overlay_close", {"phase": "turn_order", "next_player": True})
                                click_event = pygame.event.Event(
                                    pygame_gui.UI_BUTTON_PRESSED,
                                    {'ui_element': game.dice_overlay.closeDiceOverlayBut}
                                )
                                pygame.event.post(click_event)
                                dice_launched = False
                continue

            # Gioco iniziato: esegui azioni solo ogni N frames per simulare timing
            if frame_count % frames_between_actions != 0:
                # Tick del clock per mantenere il framerate
                game.clock.tick(self.fps)
                continue

            # PRIORITÀ 1: Gestisci pannelli aperti
            if game.current_panel is not None:
                self.handle_panel(game, logger)
                game.clock.tick(self.fps)
                continue

            # PRIORITÀ 2: Gestisci panels_to_show
            if hasattr(game, 'panels_to_show') and len(game.panels_to_show) > 0:
                game.clock.tick(self.fps)
                continue

            # PRIORITÀ 3: Gestisci alert messages
            if hasattr(game, '_Game__alert_messages') and len(game._Game__alert_messages) > 0:
                game.clock.tick(self.fps)
                continue

            # PRIORITÀ 4: Azioni di gioco normali
            if not hasattr(game, '_Game__actions_status'):
                game.clock.tick(self.fps)
                continue

            # Lancia dadi se possibile
            if game._Game__actions_status.get_throw_dices():
                turn_count += 1
                current_player = game.get_current_player()

                # Log ogni turno
                logger.log_action("bot", "throw_dice", {
                    "turn": turn_count,
                    "player": current_player.get_name(),
                    "position": current_player.get_position(),
                    "balance": current_player.get_balance()
                })

                # Log stato completo ogni 10 turni
                if turn_count % 10 == 0:
                    logger.log_game_state(
                        turn_count,
                        current_player.get_name(),
                        self.get_players_state(game.get_players())
                    )

                if hasattr(game._Game__gameUI, 'launchDice'):
                    click_event = pygame.event.Event(
                        pygame_gui.UI_BUTTON_PRESSED,
                        {'ui_element': game._Game__gameUI.launchDice}
                    )
                    pygame.event.post(click_event)
                game.clock.tick(self.fps)
                continue

            # Compra stock se possibile e conveniente
            if game._Game__actions_status.get_buy_property():
                if self.should_buy_stock(game, logger):
                    if hasattr(game._Game__gameUI, 'buyButton'):
                        click_event = pygame.event.Event(
                            pygame_gui.UI_BUTTON_PRESSED,
                            {'ui_element': game._Game__gameUI.buyButton}
                        )
                        pygame.event.post(click_event)
                else:
                    # Non comprare, passa il turno
                    if hasattr(game._Game__gameUI, 'passButton'):
                        click_event = pygame.event.Event(
                            pygame_gui.UI_BUTTON_PRESSED,
                            {'ui_element': game._Game__gameUI.passButton}
                        )
                        pygame.event.post(click_event)
                game.clock.tick(self.fps)
                continue

            # Passa il turno se possibile
            if game._Game__actions_status.get_pass_turn():
                current_player = game.get_current_player()
                logger.log_action("bot", "pass_turn", {
                    "player": current_player.get_name(),
                    "turn": turn_count
                })
                if hasattr(game._Game__gameUI, 'passButton'):
                    click_event = pygame.event.Event(
                        pygame_gui.UI_BUTTON_PRESSED,
                        {'ui_element': game._Game__gameUI.passButton}
                    )
                    pygame.event.post(click_event)
                game.clock.tick(self.fps)
                continue

            # Check vittoria
            if len(game.get_players()) == 1:
                logger.log_action("system", "game_won", {
                    "winner": game.get_players()[0].get_name(),
                    "turns": turn_count
                })
                game.running = False
                break

            # Tick del clock e aggiorna display
            game.clock.tick(self.fps)
            game.update_graphic(tick_clock=False)

        return turn_count

    def handle_panel(self, game: Game, logger: GameLogger):
        """Gestisce i pannelli aperti."""
        # Pannello alert
        if hasattr(game._Game__gameUI, 'alertUi') and game.current_panel == game._Game__gameUI.alertUi:
            if hasattr(game._Game__gameUI, 'closeAlertBut'):
                logger.log_action("bot", "close_alert", {})
                click_event = pygame.event.Event(
                    pygame_gui.UI_BUTTON_PRESSED,
                    {'ui_element': game._Game__gameUI.closeAlertBut}
                )
                pygame.event.post(click_event)
            return

        # Pannello evento
        if hasattr(game.current_panel, 'eventBut'):
            logger.log_action("bot", "confirm_event", {"panel_type": "event"})
            click_event = pygame.event.Event(
                pygame_gui.UI_BUTTON_PRESSED,
                {'ui_element': game.current_panel.eventBut}
            )
            pygame.event.post(click_event)
            return

        # Dice overlay durante il gioco (es. riserva monetaria) - lancia e chiudi in sequenza
        if hasattr(game.current_panel, 'launchOverlayDiceBut'):
            # Usa un flag per tracciare se abbiamo già lanciato
            if not hasattr(game.current_panel, '_dice_launched'):
                game.current_panel._dice_launched = False

            if not game.current_panel._dice_launched:
                # Lancia il dado
                logger.log_action("bot", "launch_dice", {"context": "overlay"})
                click_event = pygame.event.Event(
                    pygame_gui.UI_BUTTON_PRESSED,
                    {'ui_element': game.current_panel.launchOverlayDiceBut}
                )
                pygame.event.post(click_event)
                game.current_panel._dice_launched = True
            else:
                # Chiudi dopo aver lanciato
                if hasattr(game.current_panel, 'closeDiceOverlayBut'):
                    logger.log_action("bot", "close_dice_overlay", {})
                    click_event = pygame.event.Event(
                        pygame_gui.UI_BUTTON_PRESSED,
                        {'ui_element': game.current_panel.closeDiceOverlayBut}
                    )
                    pygame.event.post(click_event)
                    game.current_panel._dice_launched = False
                elif hasattr(game.current_panel, 'close_die_overlay_but'):
                    logger.log_action("bot", "close_dice_overlay", {})
                    click_event = pygame.event.Event(
                        pygame_gui.UI_BUTTON_PRESSED,
                        {'ui_element': game.current_panel.close_die_overlay_but}
                    )
                    pygame.event.post(click_event)
                    game.current_panel._dice_launched = False
            return

        # ShowStockUI - controlla tutti i tipi possibili
        if (hasattr(game.current_panel, 'chooseBut') or
            hasattr(game.current_panel, 'chooseMoveBut') or
            hasattr(game.current_panel, 'stockToAuction') or
            hasattr(game.current_panel, 'leave_to_bank_auct') or
            hasattr(game.current_panel, 'auction_bankrupt') or
            hasattr(game.current_panel, 'leave_to_bank_bankrupt') or
            hasattr(game.current_panel, 'buyAnyBut')):
            self.handle_stock_panel(game, logger)
            return

        # Auction
        if hasattr(game.current_panel, 'retireAuction'):
            self.handle_auction(game, logger)
            return

        # BargainUI
        if hasattr(game.current_panel, 'close_butt'):
            logger.log_action("bot", "close_bargain", {})
            click_event = pygame.event.Event(
                pygame_gui.UI_BUTTON_PRESSED,
                {'ui_element': game.current_panel.close_butt}
            )
            pygame.event.post(click_event)
            return

        # TakeSomeoneWithYouUI
        if hasattr(game.current_panel, 'take_someone_butt'):
            logger.log_action("bot", "take_someone", {"action": "choose"})
            click_event = pygame.event.Event(
                pygame_gui.UI_BUTTON_PRESSED,
                {'ui_element': game.current_panel.take_someone_butt}
            )
            pygame.event.post(click_event)
            return

    def should_buy_stock(self, game: Game, logger: GameLogger) -> bool:
        """Decide se comprare uno stock."""
        current_player = game.get_current_player()
        player_balance = current_player.get_balance()

        cells = game.get_board().get_cells()
        current_cell = cells[current_player.get_position()]

        if current_cell.get_stocks() is not None and len(current_cell.get_stocks()) > 0:
            stock = current_cell.get_stocks()[0]
            stock_price = stock.get_stock_value()
            stock_name = stock.get_name()
            num_stocks = len(current_player.get_stocks())

            buy_probability = 0.6

            if num_stocks < 3:
                buy_probability += 0.2
            elif num_stocks < 5:
                buy_probability += 0.1

            if stock_price == 0:
                buy_probability = 1.0
            elif player_balance > stock_price * 5:
                buy_probability += 0.2
            elif player_balance > stock_price * 3:
                buy_probability += 0.1
            elif player_balance > stock_price * 1.5:
                buy_probability -= 0.1
            elif player_balance > stock_price:
                buy_probability -= 0.3
            else:
                buy_probability = 0.0

            if num_stocks > 8:
                buy_probability -= 0.2
            elif num_stocks > 6:
                buy_probability -= 0.1

            buy_probability = max(0.0, min(1.0, buy_probability))

            random_value = game.dice_controller.seeded_random.rng.random()

            if random_value < buy_probability:
                logger.log_action("bot", "buy_stock", {
                    "stock": stock_name,
                    "price": stock_price,
                    "balance": player_balance,
                    "num_stocks": num_stocks,
                    "probability": buy_probability
                })
                return True
            else:
                logger.log_action("bot", "skip_buy", {
                    "stock": stock_name,
                    "price": stock_price,
                    "balance": player_balance,
                    "num_stocks": num_stocks,
                    "probability": buy_probability,
                    "reason": "probability_or_expense"
                })
        return False

    def handle_stock_panel(self, game: Game, logger: GameLogger):
        """Gestisce pannelli stock."""
        stock_name = game.current_panel.get_showed_stock().get_name() if hasattr(game.current_panel, 'get_showed_stock') else "unknown"

        # chooseMoveBut per MOVE_TO_STOCK
        if hasattr(game.current_panel, 'chooseMoveBut'):
            logger.log_action("bot", "choose_move_to_stock", {"stock": stock_name})
            click_event = pygame.event.Event(
                pygame_gui.UI_BUTTON_PRESSED,
                {'ui_element': game.current_panel.chooseMoveBut}
            )
            pygame.event.post(click_event)
            return

        # STOCK_TO_AUCTION - metti all'asta
        if hasattr(game.current_panel, 'stockToAuction'):
            logger.log_action("bot", "put_to_auction", {"stock": stock_name})
            click_event = pygame.event.Event(
                pygame_gui.UI_BUTTON_PRESSED,
                {'ui_element': game.current_panel.stockToAuction}
            )
            pygame.event.post(click_event)
            return

        # BUY_AUCTIONED_STOCK - lascia
        if hasattr(game.current_panel, 'leave_to_bank_auct'):
            logger.log_action("bot", "leave_auction_to_bank", {"stock": stock_name})
            click_event = pygame.event.Event(
                pygame_gui.UI_BUTTON_PRESSED,
                {'ui_element': game.current_panel.leave_to_bank_auct}
            )
            pygame.event.post(click_event)
            return

        # BANKRUPT_STOCK - metti all'asta o vendi alla banca
        if hasattr(game.current_panel, 'auction_bankrupt'):
            # Decidi se mettere all'asta o vendere alla banca
            current_player = game.get_current_player()
            stock = game.current_panel.get_showed_stock() if hasattr(game.current_panel, 'get_showed_stock') else None
            stock_price = stock.get_stock_value() if stock and hasattr(stock, 'get_stock_value') else 0

            # Preferisci vendere alla banca se il prezzo è alto (più veloce)
            sell_to_bank_probability = 0.7 if stock_price > 100 else 0.3
            random_value = game.dice_controller.seeded_random.rng.random()

            if random_value < sell_to_bank_probability and hasattr(game.current_panel, 'leave_to_bank_bankrupt'):
                logger.log_action("bot", "bankrupt_sell_to_bank", {"stock": stock_name, "price": stock_price})
                click_event = pygame.event.Event(
                    pygame_gui.UI_BUTTON_PRESSED,
                    {'ui_element': game.current_panel.leave_to_bank_bankrupt}
                )
                pygame.event.post(click_event)
            else:
                logger.log_action("bot", "bankrupt_auction", {"stock": stock_name, "price": stock_price})
                click_event = pygame.event.Event(
                    pygame_gui.UI_BUTTON_PRESSED,
                    {'ui_element': game.current_panel.auction_bankrupt}
                )
                pygame.event.post(click_event)
            return

        # BUY_ANYTHING
        if hasattr(game.current_panel, 'buyAnyBut'):
            current_player = game.get_current_player()
            player_balance = current_player.get_balance()
            stock = game.current_panel.get_showed_stock() if hasattr(game.current_panel, 'get_showed_stock') else None
            stock_price = stock.get_stock_value() if stock and hasattr(stock, 'get_stock_value') else 0

            buy_probability = 0.4
            if stock_price == 0 or player_balance > stock_price * 5:
                buy_probability = 0.7
            elif player_balance > stock_price * 3:
                buy_probability = 0.5
            elif player_balance > stock_price * 1.5:
                buy_probability = 0.3
            elif player_balance > stock_price:
                buy_probability = 0.15
            else:
                buy_probability = 0.0

            random_value = game.dice_controller.seeded_random.rng.random()

            if random_value < buy_probability:
                logger.log_action("bot", "buy_anything", {"stock": stock_name, "price": stock_price, "balance": player_balance})
                click_event = pygame.event.Event(
                    pygame_gui.UI_BUTTON_PRESSED,
                    {'ui_element': game.current_panel.buyAnyBut}
                )
                pygame.event.post(click_event)
            else:
                logger.log_action("bot", "skip_buy_anything", {"stock": stock_name, "reason": "too_expensive", "price": stock_price, "balance": player_balance})
                if hasattr(game.current_panel, 'closeStock'):
                    click_event = pygame.event.Event(
                        pygame_gui.UI_BUTTON_PRESSED,
                        {'ui_element': game.current_panel.closeStock}
                    )
                    pygame.event.post(click_event)
            return

        # SHOW_CHOOSE_STOCK (fermata libera), default case
        if hasattr(game.current_panel, 'chooseBut'):
            current_player = game.get_current_player()
            player_balance = current_player.get_balance()
            stock = game.current_panel.get_showed_stock() if hasattr(game.current_panel, 'get_showed_stock') else None
            stock_price = stock.get_stock_value() if stock and hasattr(stock, 'get_stock_value') else 0

            buy_probability = 0.5
            if stock_price == 0 or player_balance > stock_price * 5:
                buy_probability = 0.8
            elif player_balance > stock_price * 3:
                buy_probability = 0.6
            elif player_balance > stock_price * 1.5:
                buy_probability = 0.4
            elif player_balance > stock_price:
                buy_probability = 0.2
            else:
                buy_probability = 0.0

            random_value = game.dice_controller.seeded_random.rng.random()

            if random_value < buy_probability:
                logger.log_action("bot", "choose_stock", {"stock": stock_name, "price": stock_price, "balance": player_balance})
                click_event = pygame.event.Event(
                    pygame_gui.UI_BUTTON_PRESSED,
                    {'ui_element': game.current_panel.chooseBut}
                )
                pygame.event.post(click_event)
            else:
                logger.log_action("bot", "skip_stock", {"stock": stock_name, "reason": "too_expensive", "price": stock_price, "balance": player_balance})
                if hasattr(game.current_panel, 'closeStock'):
                    click_event = pygame.event.Event(
                        pygame_gui.UI_BUTTON_PRESSED,
                        {'ui_element': game.current_panel.closeStock}
                    )
                    pygame.event.post(click_event)

    def handle_auction(self, game: Game, logger: GameLogger):
        """Gestisce le aste."""
        auction_stock = game.current_panel.get_stock().get_name() if hasattr(game.current_panel, 'get_stock') else "unknown"
        current_bid = getattr(game.current_panel, 'current_bid', 0)
        current_player_in_auction = game.current_panel.get_bidders()[game.current_panel.current_bidder] if hasattr(game.current_panel, 'get_bidders') and hasattr(game.current_panel, 'current_bidder') else None

        if not hasattr(game.current_panel, '_bot_auction_pass_count'):
            game.current_panel._bot_auction_pass_count = {}

        action = 'pass'

        if current_player_in_auction:
            player_balance = current_player_in_auction.get_balance()
            player_name = current_player_in_auction.get_name()

            if player_name not in game.current_panel._bot_auction_pass_count:
                game.current_panel._bot_auction_pass_count[player_name] = 0

            max_bid_index = game.current_panel.find_max_bid() if hasattr(game.current_panel, 'find_max_bid') else -1
            current_bidder_index = game.current_panel.current_bidder
            has_highest_bid = (max_bid_index == current_bidder_index and sum(game.current_panel.bids) > 0)

            if has_highest_bid:
                action = 'pass'
                logger.log_action("bot", "pass_auction_highest_bid", {
                    "stock": auction_stock,
                    "bid": current_bid,
                    "reason": "has_highest_bid",
                    "balance": player_balance
                })
            elif game.current_panel._bot_auction_pass_count[player_name] >= 2:
                action = 'retire'
                logger.log_action("bot", "auto_retire_auction", {
                    "stock": auction_stock,
                    "bid": current_bid,
                    "reason": "passed_too_many_times",
                    "pass_count": game.current_panel._bot_auction_pass_count[player_name]
                })
            else:
                retire_probability = 0.0
                if player_balance < current_bid * 1.1:
                    retire_probability = 0.7
                elif player_balance < current_bid * 1.5:
                    retire_probability = 0.4
                elif player_balance < current_bid * 2.5:
                    retire_probability = 0.2
                else:
                    retire_probability = 0.05

                bid_probability = 0.0
                if current_bid == 0:
                    bid_probability = 0.6
                elif player_balance > current_bid * 4:
                    bid_probability = 0.5
                elif player_balance > current_bid * 2:
                    bid_probability = 0.3
                elif player_balance > current_bid * 1.3:
                    bid_probability = 0.15

                random_value = game.dice_controller.seeded_random.rng.random()

                if random_value < retire_probability:
                    action = 'retire'
                elif random_value < retire_probability + bid_probability:
                    action = 'bid'
                else:
                    action = 'pass'
                    game.current_panel._bot_auction_pass_count[player_name] += 1

        if action == 'bid' and hasattr(game.current_panel, 'bidBut'):
            if current_player_in_auction:
                game.current_panel._bot_auction_pass_count[current_player_in_auction.get_name()] = 0
            logger.log_action("bot", "bid_auction", {"stock": auction_stock, "bid": current_bid, "balance": player_balance})
            click_event = pygame.event.Event(
                pygame_gui.UI_BUTTON_PRESSED,
                {'ui_element': game.current_panel.bidBut}
            )
            pygame.event.post(click_event)
        elif action == 'retire' and hasattr(game.current_panel, 'retireAuction'):
            logger.log_action("bot", "retire_from_auction", {"stock": auction_stock, "bid": current_bid, "balance": player_balance})
            click_event = pygame.event.Event(
                pygame_gui.UI_BUTTON_PRESSED,
                {'ui_element': game.current_panel.retireAuction}
            )
            pygame.event.post(click_event)
        else:
            logger.log_action("bot", "pass_auction", {
                "stock": auction_stock,
                "bid": current_bid,
                "pass_count": game.current_panel._bot_auction_pass_count.get(current_player_in_auction.get_name() if current_player_in_auction else "unknown", 0)
            })
            if hasattr(game.current_panel, 'nextBidder'):
                click_event = pygame.event.Event(
                    pygame_gui.UI_BUTTON_PRESSED,
                    {'ui_element': game.current_panel.nextBidder}
                )
                pygame.event.post(click_event)

    def get_game_state(self, game: Game) -> Dict[str, Any]:
        """Estrae lo stato completo del gioco."""
        return {
            "current_player_index": game.get_current_player_index(),
            "players": self.get_players_state(game.get_players()),
            "square_balance": game.get_square_balance()
        }

    def get_players_state(self, players: List) -> List[Dict[str, Any]]:
        """Estrae lo stato di tutti i giocatori."""
        return [
            {
                "name": p.get_name(),
                "position": p.get_position(),
                "balance": p.get_balance(),
                "stocks": [s.get_name() for s in p.get_stocks()],
                "is_bankrupt": p.is_in_debt()
            }
            for p in players
        ]

    def generate_summary(self, elapsed_time: float):
        """
        Genera un file di sommario con i risultati di tutti i test.

        Args:
            elapsed_time: Tempo totale di esecuzione
        """
        successes = sum(1 for r in self.results if r["status"] == "success")
        errors = sum(1 for r in self.results if r["status"] == "error")
        critical = sum(1 for r in self.results if r["status"] == "critical_failure")

        with open(self.summary_file, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("STRESS TEST SUMMARY V2\n")
            f.write("="*80 + "\n\n")

            f.write(f"Esecuzione: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Seed base: {self.base_seed}\n")
            f.write(f"Numero test: {self.num_tests}\n")
            f.write(f"FPS: {self.fps}\n")
            f.write(f"Durata totale: {elapsed_time:.2f}s\n")
            f.write(f"Tempo medio per test: {elapsed_time/self.num_tests:.2f}s\n\n")

            f.write("RISULTATI:\n")
            f.write(f"  ✓ Successi: {successes}/{self.num_tests} ({successes/self.num_tests*100:.1f}%)\n")
            f.write(f"  ✗ Errori: {errors}/{self.num_tests} ({errors/self.num_tests*100:.1f}%)\n")
            f.write(f"  ✗ Fallimenti critici: {critical}/{self.num_tests} ({critical/self.num_tests*100:.1f}%)\n\n")

            # Dettagli errori
            if errors > 0 or critical > 0:
                f.write("\nERRORI TROVATI:\n")
                f.write("-"*80 + "\n")
                for result in self.results:
                    if result["status"] in ["error", "critical_failure"]:
                        f.write(f"\nTest #{result['test_num']} - Seed: {result['seed']}\n")
                        f.write(f"  Tipo: {result.get('error_type', 'Unknown')}\n")
                        f.write(f"  Messaggio: {result.get('error_message', result.get('error', 'N/A'))}\n")
                        f.write(f"  Turno: {result.get('turns', 'N/A')}\n")
                        f.write(f"  Log: {result.get('log_file', 'N/A')}\n")

            # Statistiche turni
            successful_tests = [r for r in self.results if r["status"] == "success"]
            if successful_tests:
                turns_list = [r["turns"] for r in successful_tests]
                f.write("\n\nSTATISTICHE TURNI:\n")
                f.write(f"  Media: {sum(turns_list)/len(turns_list):.1f}\n")
                f.write(f"  Minimo: {min(turns_list)}\n")
                f.write(f"  Massimo: {max(turns_list)}\n")

            f.write("\n" + "="*80 + "\n")

        print(f"\n\n{'='*80}")
        print(f"STRESS TEST COMPLETATO")
        print(f"{'='*80}")
        print(f"Successi: {successes}/{self.num_tests}")
        print(f"Errori: {errors}/{self.num_tests}")
        print(f"Summary salvato in: {self.summary_file}")
        print(f"{'='*80}\n")


def main():
    """Entry point principale."""
    parser = argparse.ArgumentParser(
        description="Stress tester V2 per PyazzaMarket (frame-based, no threading)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Esempi d'uso:
  # Esegui 10 test con seed random
  python stress_test_v2.py -n 10

  # Esegui 5 test con un seed specifico
  python stress_test_v2.py -n 5 --seed 12345

  # Esegui test con FPS alto per velocizzare
  python stress_test_v2.py -n 10 --fps 240

  # Esegui test con limite di 200 turni
  python stress_test_v2.py -n 10 --max-turns 200
        """
    )

    parser.add_argument(
        "-n", "--num-tests",
        type=int,
        default=1,
        help="Numero di test da eseguire (default: 1)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Seed iniziale (default: timestamp corrente)"
    )
    parser.add_argument(
        "--max-turns",
        type=int,
        default=500,
        help="Numero massimo di turni per partita (default: 500)"
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=120,
        help="Framerate del gioco - più alto = più veloce (default: 120)"
    )

    args = parser.parse_args()

    # Crea ed esegui il tester
    tester = StressTestRunnerV2(
        num_tests=args.num_tests,
        seed=args.seed,
        max_turns=args.max_turns,
        fps=args.fps
    )

    tester.run_all_tests()


if __name__ == "__main__":
    main()
