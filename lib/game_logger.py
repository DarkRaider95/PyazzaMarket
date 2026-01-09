"""
Sistema di logging completo per tracciare tutte le azioni del gioco.
Permette di salvare e ricostruire l'intera sequenza di eventi per debugging.
"""

import json
import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional
import traceback


class GameLogger:
    """Logger che traccia tutte le azioni del gioco per debugging e replay."""

    def __init__(self, log_dir: str = "logs", session_name: Optional[str] = None):
        """
        Inizializza il logger del gioco.

        Args:
            log_dir: Directory dove salvare i log
            session_name: Nome della sessione (generato automaticamente se None)
        """
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)

        # Genera nome sessione con timestamp
        if session_name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            session_name = f"game_{timestamp}"

        self.session_name = session_name
        self.log_file = os.path.join(log_dir, f"{session_name}.json")
        self.error_log_file = os.path.join(log_dir, f"{session_name}_errors.log")

        # Inizializza struttura dati per il log
        self.game_log: Dict[str, Any] = {
            "session_name": session_name,
            "start_time": datetime.now().isoformat(),
            "seed": None,
            "initial_state": {},
            "actions": [],
            "errors": [],
            "end_time": None,
            "status": "running"
        }

        # Setup logging per errori
        self.error_logger = logging.getLogger(f"GameErrorLogger_{session_name}")
        self.error_logger.setLevel(logging.ERROR)

        # File handler per errori
        fh = logging.FileHandler(self.error_log_file)
        fh.setLevel(logging.ERROR)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        self.error_logger.addHandler(fh)

        self.action_counter = 0

    def set_seed(self, seed: int):
        """Salva il seed usato per questa partita."""
        self.game_log["seed"] = seed
        self.log_action("system", "seed_set", {"seed": seed})

    def set_initial_state(self, players: List[Dict], board_state: Dict):
        """Salva lo stato iniziale del gioco."""
        self.game_log["initial_state"] = {
            "players": players,
            "board": board_state,
            "timestamp": datetime.now().isoformat()
        }
        self.log_action("system", "game_initialized", {
            "num_players": len(players),
            "player_names": [p["name"] for p in players]
        })

    def log_action(self, category: str, action_type: str, data: Dict[str, Any]):
        """
        Logga un'azione del gioco.

        Args:
            category: Categoria dell'azione (dice_roll, move, buy, event, etc.)
            action_type: Tipo specifico di azione
            data: Dati associati all'azione
        """
        self.action_counter += 1
        action_entry = {
            "id": self.action_counter,
            "timestamp": datetime.now().isoformat(),
            "category": category,
            "type": action_type,
            "data": data
        }
        self.game_log["actions"].append(action_entry)

        # Salva periodicamente (ogni 10 azioni)
        if self.action_counter % 10 == 0:
            self._save_log()

    def log_dice_roll(self, player_name: str, dice1: int, dice2: int,
                      player_position: int, is_double: bool):
        """Logga un lancio di dadi."""
        self.log_action("dice_roll", "roll", {
            "player": player_name,
            "dice1": dice1,
            "dice2": dice2,
            "total": dice1 + dice2,
            "is_double": is_double,
            "position_before": player_position
        })

    def log_player_move(self, player_name: str, from_pos: int, to_pos: int,
                       passed_start: bool = False):
        """Logga il movimento di un giocatore."""
        self.log_action("move", "player_moved", {
            "player": player_name,
            "from": from_pos,
            "to": to_pos,
            "passed_start": passed_start
        })

    def log_stock_transaction(self, transaction_type: str, player_name: str,
                             stock_name: str, amount: int, balance_after: int):
        """Logga una transazione di cedole."""
        self.log_action("stock", transaction_type, {
            "player": player_name,
            "stock": stock_name,
            "amount": amount,
            "balance_after": balance_after
        })

    def log_money_change(self, player_name: str, amount: int, reason: str,
                        balance_after: int):
        """Logga un cambio di soldi."""
        self.log_action("money", "balance_change", {
            "player": player_name,
            "amount": amount,
            "reason": reason,
            "balance_after": balance_after
        })

    def log_event(self, event_name: str, event_type: str, affected_players: List[str],
                  event_data: Dict):
        """Logga un evento del gioco."""
        self.log_action("event", event_type, {
            "event_name": event_name,
            "affected_players": affected_players,
            "event_data": event_data
        })

    def log_auction(self, stock_name: str, winner: str, final_price: int,
                   bidders: List[str]):
        """Logga un'asta."""
        self.log_action("auction", "completed", {
            "stock": stock_name,
            "winner": winner,
            "final_price": final_price,
            "bidders": bidders
        })

    def log_bankruptcy(self, player_name: str, debt_amount: int, creditor: Optional[str],
                      remaining_players: List[str]):
        """Logga una bancarotta."""
        self.log_action("bankruptcy", "player_eliminated", {
            "player": player_name,
            "debt": debt_amount,
            "creditor": creditor,
            "remaining_players": remaining_players
        })

    def log_game_state(self, turn_number: int, current_player: str,
                      players_state: List[Dict]):
        """Logga lo stato completo del gioco (snapshot periodico)."""
        self.log_action("system", "game_state_snapshot", {
            "turn": turn_number,
            "current_player": current_player,
            "players": players_state
        })

    def log_error(self, error_type: str, error_message: str,
                 stack_trace: str, game_state: Dict):
        """
        Logga un errore con tutto il contesto necessario per il debug.

        Args:
            error_type: Tipo di errore
            error_message: Messaggio di errore
            stack_trace: Stack trace completo
            game_state: Stato del gioco al momento dell'errore
        """
        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": error_type,
            "message": error_message,
            "stack_trace": stack_trace,
            "game_state": game_state,
            "action_count": self.action_counter
        }
        self.game_log["errors"].append(error_entry)
        self.game_log["status"] = "error"

        # Log anche nel file degli errori
        self.error_logger.error(f"\n{'='*80}\nERROR: {error_type}\n{error_message}\n{stack_trace}\n{'='*80}")

        # Salva immediatamente
        self._save_log()

    def log_game_end(self, winner: Optional[str], end_reason: str,
                    final_state: Dict):
        """Logga la fine del gioco."""
        self.game_log["end_time"] = datetime.now().isoformat()
        self.game_log["status"] = "completed"
        self.log_action("system", "game_ended", {
            "winner": winner,
            "reason": end_reason,
            "final_state": final_state
        })
        self._save_log()

    def _save_log(self):
        """Salva il log su file."""
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(self.game_log, f, indent=2, ensure_ascii=False)
        except Exception as e:
            # Fallback su file di emergenza
            emergency_file = os.path.join(
                self.log_dir,
                f"{self.session_name}_emergency.json"
            )
            with open(emergency_file, 'w', encoding='utf-8') as f:
                json.dump(self.game_log, f, indent=2, ensure_ascii=False)

    def get_log_summary(self) -> Dict[str, Any]:
        """Ritorna un sommario del log."""
        return {
            "session_name": self.session_name,
            "total_actions": len(self.game_log["actions"]),
            "total_errors": len(self.game_log["errors"]),
            "status": self.game_log["status"],
            "start_time": self.game_log["start_time"],
            "end_time": self.game_log["end_time"]
        }

    @staticmethod
    def load_log(log_file: str) -> Dict[str, Any]:
        """Carica un log da file."""
        with open(log_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def export_replay_data(self) -> Dict[str, Any]:
        """Esporta i dati necessari per fare replay della partita."""
        return {
            "seed": self.game_log["seed"],
            "initial_state": self.game_log["initial_state"],
            "actions": [
                action for action in self.game_log["actions"]
                if action["category"] in ["dice_roll", "event", "auction"]
            ]
        }
