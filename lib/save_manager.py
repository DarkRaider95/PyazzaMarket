import json
import os
from datetime import datetime
from typing import Optional

class SaveManager:
    """Manages game state saving and loading"""

    SAVE_DIR = "saves"
    SAVE_EXTENSION = ".json"

    @staticmethod
    def ensure_save_directory():
        """Create save directory if it doesn't exist"""
        if not os.path.exists(SaveManager.SAVE_DIR):
            os.makedirs(SaveManager.SAVE_DIR)

    @staticmethod
    def save_game(game, filename: Optional[str] = None) -> str:
        """
        Save the current game state to a JSON file

        Args:
            game: The Game instance to save
            filename: Optional custom filename (without extension)

        Returns:
            The full path of the saved file
        """
        SaveManager.ensure_save_directory()

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"save_{timestamp}"

        filepath = os.path.join(SaveManager.SAVE_DIR, filename + SaveManager.SAVE_EXTENSION)

        # Collect game state
        game_state = {
            "timestamp": datetime.now().isoformat(),
            "current_player_index": game.get_current_player_index(),
            "square_balance": game.get_square_balance(),
            "players": [],
            "stocks": [],
            "events": [],
            "actions_status": {
                "throw_dices": game.get_actions_status().get_throw_dices(),
                "pass_turn": game.get_actions_status().get_pass_turn(),
                "buy_property": game.get_actions_status().get_buy_property(),
                "show_stock": game.get_actions_status().get_show_stock(),
            }
        }

        # Save players data
        for player in game.get_players():
            player_data = {
                "name": player.get_name(),
                "balance": player.get_balance(),
                "position": player.get_position(),
                "old_position": player.get_old_position(),
                "skip_turn": player.get_skip_turn(),
                "free_penalty": player.get_free_penalty(),
                "free_martini": player.get_free_martini(),
                "is_bot": player.get_is_bot(),
                "stocks_positions": [stock.get_position() for stock in player.get_stocks()],
                "debts": player.get_debts(),
                "car_path": getattr(player.get_car(), 'car_path', "assets/car_red.png") or "assets/car_red.png",
            }
            game_state["players"].append(player_data)

        # Save stocks data (all stocks with their current values and owners)
        from lib.stock import Stock
        for stock in Stock.get_stocks():
            stock_data = {
                "position": stock.get_position(),
                "name": stock.get_name(),
                "current_value": stock.get_stock_value(),
                "owner": stock.get_owner().get_name() if stock.get_owner() else None,
            }
            game_state["stocks"].append(stock_data)

        # Save events queue (we save the order of events by their type)
        for event in game.events:
            game_state["events"].append({
                "evenType": event.evenType,
            })

        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(game_state, f, indent=2, ensure_ascii=False)

        return filepath

    @staticmethod
    def load_game(filepath: str) -> dict:
        """
        Load game state from a JSON file

        Args:
            filepath: Path to the save file

        Returns:
            Dictionary containing the game state
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Save file not found: {filepath}")

        with open(filepath, 'r', encoding='utf-8') as f:
            game_state = json.load(f)

        return game_state

    @staticmethod
    def list_saves() -> list:
        """
        List all available save files

        Returns:
            List of tuples (filename, timestamp) sorted by date (newest first)
        """
        SaveManager.ensure_save_directory()

        saves = []
        for filename in os.listdir(SaveManager.SAVE_DIR):
            if filename.endswith(SaveManager.SAVE_EXTENSION):
                filepath = os.path.join(SaveManager.SAVE_DIR, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        timestamp = data.get("timestamp", "Unknown")
                        saves.append((filename, timestamp, filepath))
                except:
                    continue

        # Sort by timestamp (newest first)
        saves.sort(key=lambda x: x[1], reverse=True)
        return saves

    @staticmethod
    def delete_save(filepath: str) -> bool:
        """
        Delete a save file

        Args:
            filepath: Path to the save file

        Returns:
            True if successful, False otherwise
        """
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
            return False
        except:
            return False

    @staticmethod
    def restore_game_state(game, game_state: dict):
        """
        Restore game state from loaded data

        Args:
            game: The Game instance to restore state to
            game_state: Dictionary containing the saved game state
        """
        from lib.stock import Stock

        # Mark this as a loaded game to skip initial dice overlay
        game.is_loaded_game = True

        # Restore square balance
        game._Game__square_balance = game_state["square_balance"]

        # Restore current player index
        game._Game__current_player_index = game_state["current_player_index"]

        # Restore stocks values and owners
        for stock_data in game_state["stocks"]:
            stock = Stock.get_stock_by_position(stock_data["position"])
            if stock:
                stock.update_value(stock_data["current_value"])
                # Owner will be set when restoring players

        # Restore players
        players = game.get_players()
        for i, player_data in enumerate(game_state["players"]):
            if i < len(players):
                player = players[i]
                player._Player__balance = player_data["balance"]
                player._Player__position = player_data["position"]
                player._Player__old_position = player_data["old_position"]
                player._Player__set_skip_turn = player_data["skip_turn"]
                player._Player__freePenalty = player_data["free_penalty"]
                player._Player__free_martini = player_data["free_martini"]
                player._Player__debts = player_data["debts"]

                # Note: Car is already initialized correctly in Game.__init__
                # from menu.players which contains the correct car_path
                # So we don't need to restore it here

                # Restore stocks ownership
                player._Player__stocks = []
                for stock_pos in player_data["stocks_positions"]:
                    stock = Stock.get_stock_by_position(stock_pos)
                    if stock:
                        player.add_stock(stock)
                        stock.set_owner(player)

        # Restore events queue
        # We need to reorder the events deque to match the saved order
        from collections import deque
        events_dict = {event.evenType: event for event in game.events}
        new_events = deque()
        for event_data in game_state["events"]:
            if event_data["evenType"] in events_dict:
                new_events.append(events_dict[event_data["evenType"]])

        if len(new_events) > 0:
            game.events = new_events

        # Restore actions status
        actions_status = game_state["actions_status"]
        game.get_actions_status().set_throw_dices(actions_status["throw_dices"])
        game.get_actions_status().set_pass_turn(actions_status["pass_turn"])
        game.get_actions_status().set_buy_property(actions_status["buy_property"])
        game.get_actions_status().set_show_stock(actions_status["show_stock"])
