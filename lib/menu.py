import pygame
import sys
from pygame_gui import UIManager
from pygame_gui.elements import UITextEntryLine, UIButton, UIDropDownMenu
import pygame_gui
from lib.save_manager import SaveManager
from lib.constants import (
    WIDTH,
    HEIGHT,
    WHITE,
    BLACK,
    CAR_BLACK,
    CAR_BLUE,
    CAR_RED,
    CAR_YELLOW,
    CAR_COLORS_MAP,
    CAR_PATH_TO_COLOR,
    FPS
)

# Inizializzazione della finestra di gioco
pygame.display.set_caption("Menu di Gioco")


class Menu:
    def __init__(self, width, height, clock):  # each player initialised with its data
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True  # Used to shutdown the game
        self.width = width
        self.height = height
        self.num_players = 2
        self.clock = clock
        self.manager = UIManager(
            (WIDTH, HEIGHT)
        )  # Create something similar to pygame.display.set_mode((WIDTH, HEIGHT))

        # Bottone "Inizia partita"
        self.start_button = UIButton(
            relative_rect=pygame.Rect(
                WIDTH // 2 - 100, 450, 200, 50
            ),  # x, y, width, height
            text="Inizia partita",
            object_id="START",
            manager=self.manager,
        )

        # Bottone "Carica partita"
        self.load_button = UIButton(
            relative_rect=pygame.Rect(WIDTH // 2 - 100, 510, 200, 50),
            text="Carica partita",
            object_id="LOAD",
            manager=self.manager,
        )

        # Bottone "Chiudi gioco"
        self.quit_button = UIButton(
            relative_rect=pygame.Rect(WIDTH // 2 - 100, 570, 200, 50),
            text="Chiudi gioco",
            object_id="QUIT",
            manager=self.manager,
        )

        # Bottone "-" per diminuire il numero di giocatori
        self.minus_button = UIButton(
            relative_rect=pygame.Rect(WIDTH // 2 - 50, 240, 40, 40),
            text="-",
            object_id="MINUS",
            manager=self.manager,
        )

        # Bottone "+" per aumentare il numero di giocatori
        self.plus_button = UIButton(
            relative_rect=pygame.Rect(WIDTH // 2 + 20, 240, 40, 40),
            text="+",
            object_id="PLUS",
            manager=self.manager,
        )

        # create one entry line and add it to the list
        entry_line1 = UITextEntryLine(
            relative_rect=pygame.Rect(WIDTH // 2 - 185, 300 + 50, 300, 40),
            manager=self.manager,
            object_id="PLAYER1",
            initial_text="Player1",
        )
        entry_line1.set_text_length_limit(15)

        entry_line2 = UITextEntryLine(
            relative_rect=pygame.Rect(WIDTH // 2 - 185, 300 + 50 * 2, 300, 40),
            manager=self.manager,
            object_id="PLAYER2",
            initial_text="Player2",
        )
        entry_line2.set_text_length_limit(15)

        car_line1 = UIDropDownMenu(
            relative_rect=pygame.Rect(WIDTH // 2 + 115, 300 + 50, 80, 40),
            options_list=["RED", "BLACK", "BLUE", "YELLOW"],
            starting_option="RED",
            manager=self.manager,
            object_id="CAR1",
        )

        car_line2 = UIDropDownMenu(
            relative_rect=pygame.Rect(WIDTH // 2 + 115, 300 + 50 * 2, 80, 40),
            options_list=["RED", "BLACK", "BLUE", "YELLOW"],
            starting_option="BLACK",
            manager=self.manager,
            object_id="CAR2",
        )

        ai_line2 = UIDropDownMenu(
            relative_rect=pygame.Rect(WIDTH // 2 + 195, 300 + 50 * 2, 80, 40),
            options_list=["BOT", "UMANO"],
            starting_option="BOT",
            manager=self.manager,
            object_id="BOT2",
        )

        self.entry_lines = [entry_line1, entry_line2]
        self.car_lines = [car_line1, car_line2]
        self.ai_lines = [
            None,
            ai_line2,
        ]  # We need a None to have the list of the right lenght

        self.players = [
            {"name": "Player1", "color": CAR_RED, "bot": False},
            {"name": "Player2", "color": CAR_BLACK, "bot": True},
        ]

        self.font = pygame.font.Font(None, 32)
        self.error_message = None
        self.error_message_timer = 0
        self.loaded_game_state = None

    def show_start_menu(self):
        while self.running:
            time_delta = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if (
                        event.ui_element == self.quit_button
                        or event.type == pygame.QUIT
                    ):  # quit_button.collidepoint(mouse_pos) == 'QUIT' or event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    elif event.ui_element == self.start_button:
                        print("start")
                        # start game
                        if not self.check_duplicate_cars():
                            self.running = False
                            self.update_player()
                        else:
                            # Show error message for duplicate car selection
                            self.show_error_message("Errore: due giocatori non possono avere la stessa macchina!")

                    elif event.ui_element == self.load_button:
                        # Load game
                        saves = SaveManager.list_saves()
                        if len(saves) > 0:
                            filepath = saves[0][2]
                            try:
                                self.loaded_game_state = SaveManager.load_game(filepath)
                                self.running = False
                                # Extract players from loaded game state
                                self.players = []
                                for player_data in self.loaded_game_state["players"]:
                                    # Use the saved car_path directly, with fallback to RED
                                    car_path = player_data.get("car_path", CAR_RED)

                                    self.players.append({
                                        "name": player_data["name"],
                                        "color": car_path,
                                        "bot": player_data["is_bot"]
                                    })
                            except Exception as e:
                                self.show_error_message(f"Errore nel caricamento: {str(e)}")
                        else:
                            self.show_error_message("Nessun salvataggio trovato!")

                    # Bottone "-" per diminuire il numero di giocatori
                    elif event.ui_element == self.minus_button and self.num_players > 2:
                        self.entry_lines[self.num_players - 1].kill()
                        self.car_lines[self.num_players - 1].kill()
                        self.ai_lines[self.num_players - 1].kill()
                        self.num_players -= 1
                        self.players = self.players[: self.num_players]
                        self.entry_lines = self.entry_lines[: self.num_players]
                        self.car_lines = self.car_lines[: self.num_players]
                        self.ai_lines = self.ai_lines[: self.num_players]
                        self.start_button.set_position(
                            (WIDTH // 2 - 100, 450 + (self.num_players - 1) * 50)
                        )
                        self.quit_button.set_position(
                            (WIDTH // 2 - 100, 510 + (self.num_players - 1) * 50)
                        )

                    # Bottone "+" per aumentare il numero di giocatori
                    elif event.ui_element == self.plus_button and self.num_players < 6:
                        self.num_players += 1
                        entry_line = UITextEntryLine(
                            relative_rect=pygame.Rect(
                                WIDTH // 2 - 185,
                                300 + 50 * self.num_players - 1,
                                300,
                                40,
                            ),
                            manager=self.manager,
                            object_id="PLAYER" + str(self.num_players),
                            initial_text="Player" + str(self.num_players),
                        )
                        entry_line.set_text_length_limit(15)
                        car_line = UIDropDownMenu(
                            relative_rect=pygame.Rect(
                                WIDTH // 2 + 115,
                                300 + 50 * self.num_players - 1,
                                80,
                                40,
                            ),
                            options_list=["RED", "BLACK", "BLUE", "YELLOW"],
                            starting_option="RED",
                            manager=self.manager,
                            object_id="CAR" + str(self.num_players),
                        )
                        ai_line = UIDropDownMenu(
                            relative_rect=pygame.Rect(
                                WIDTH // 2 + 195,
                                300 + 50 * self.num_players - 1,
                                80,
                                40,
                            ),
                            options_list=["BOT", "UMANO"],
                            starting_option="BOT",
                            manager=self.manager,
                            object_id="BOT" + str(self.num_players),
                        )
                        self.entry_lines.append(entry_line)
                        self.car_lines.append(car_line)
                        self.ai_lines.append(ai_line)
                        self.start_button.set_position(
                            (WIDTH // 2 - 100, 450 + (self.num_players - 1) * 50)
                        )
                        self.quit_button.set_position(
                            (WIDTH // 2 - 100, 510 + (self.num_players - 1) * 50)
                        )
                        self.players.append(
                            {
                                "name": "Player" + str(self.num_players),
                                "color": CAR_RED,
                                "bot": True,
                            }
                        )

                self.manager.process_events(event)

            self.manager.update(time_delta)

            # Update error message timer
            if self.error_message is not None:
                self.error_message_timer -= time_delta
                if self.error_message_timer <= 0:
                    self.error_message = None

            self.screen.fill(WHITE)

            # Visualizza il numero di giocatori
            num_players_display = self.font.render(str(self.num_players), True, BLACK)
            self.screen.blit(
                num_players_display,
                (WIDTH // 2 - num_players_display.get_width() // 2, 240),
            )

            self.manager.draw_ui(self.screen)

            # Testo del menu
            title_text = self.font.render("Menu di Gioco", True, BLACK)
            self.screen.blit(
                title_text, (WIDTH // 2 - title_text.get_width() // 2, 100)
            )

            num_players_text = self.font.render("Numero di giocatori:", True, BLACK)
            self.screen.blit(
                num_players_text, (WIDTH // 2 - num_players_text.get_width() // 2, 200)
            )

            player_names_text = self.font.render("Nomi dei giocatori:", True, BLACK)
            self.screen.blit(
                player_names_text,
                (WIDTH // 2 - player_names_text.get_width() // 2, 300),
            )

            # Display error message if present
            if self.error_message is not None:
                error_font = pygame.font.Font(None, 28)
                error_text = error_font.render(self.error_message, True, (255, 0, 0))
                error_rect = error_text.get_rect(center=(WIDTH // 2, 150))
                pygame.draw.rect(self.screen, WHITE, error_rect.inflate(20, 10))
                pygame.draw.rect(self.screen, (255, 0, 0), error_rect.inflate(20, 10), 2)
                self.screen.blit(error_text, error_rect)

            pygame.display.flip()

    def color_to_costant(self, color) -> str:
        return CAR_COLORS_MAP.get(color, CAR_RED)

    def bot_to_bool(self, bot) -> bool:
        if bot == "BOT":
            return True
        return False

    def update_player(self) -> None:
        for i, entry in enumerate(self.entry_lines):
            self.players[i]["name"] = entry.text
        for i, car in enumerate(self.car_lines):
            selected_color = car.selected_option
            # Handle case where selected_option returns a tuple (color, color)
            if isinstance(selected_color, tuple):
                selected_color = selected_color[0]
            color_path = self.color_to_costant(selected_color)
            print(f"DEBUG: Player {i} - selected_color: {selected_color}, color_path: {color_path}")
            self.players[i]["color"] = color_path
        for i, ai in enumerate(self.ai_lines):
            if ai == None:
                self.players[i]["bot"] = False
            else:
                bot_option = ai.selected_option
                # Handle case where selected_option returns a tuple
                if isinstance(bot_option, tuple):
                    bot_option = bot_option[0]
                self.players[i]["bot"] = self.bot_to_bool(bot_option)
        print(f"DEBUG: Final players list: {self.players}")

    def check_duplicate_cars(self) -> bool:
        """Check if two or more players have selected the same car color.
        Returns True if duplicates found, False otherwise."""
        selected_colors = []
        for car_line in self.car_lines:
            color = car_line.selected_option
            # Handle case where selected_option returns a tuple
            if isinstance(color, tuple):
                color = color[0]
            if color in selected_colors:
                return True
            selected_colors.append(color)
        return False

    def show_error_message(self, message: str) -> None:
        """Display an error message for 3 seconds."""
        self.error_message = message
        self.error_message_timer = 3.0
