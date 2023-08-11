import pygame
import sys
from pygame_gui import UIManager
from pygame_gui.elements import UITextEntryLine, UIButton, UIDropDownMenu
import pygame_gui
from lib.constants import WIDTH, HEIGHT, WHITE, BLACK, CAR_BLACK, CAR_BLUE, CAR_RED, CAR_YELLOW

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
            relative_rect=pygame.Rect(WIDTH // 2 - 100, 450, 200, 50),  # x, y, width, height
            text="Inizia partita",
            object_id="START",
            manager=self.manager,
        )

        # Bottone "Chiudi gioco"
        self.quit_button = UIButton(
            relative_rect=pygame.Rect(WIDTH // 2 - 100, 510, 200, 50),
            text="Chiudi gioco",
            object_id="QUIT",
            manager=self.manager,
        )

        # Bottone "-" per diminuire il numero di giocatori
        self.minus_button = UIButton(
            relative_rect=pygame.Rect(WIDTH // 2 - 50, 240, 40, 40), text="-", object_id="MINUS", manager=self.manager
        )

        # Bottone "+" per aumentare il numero di giocatori
        self.plus_button = UIButton(
            relative_rect=pygame.Rect(WIDTH // 2 + 20, 240, 40, 40), text="+", object_id="PLUS", manager=self.manager
        )

        # create one entry line and add it to the list
        entry_line1 = UITextEntryLine(
            relative_rect=pygame.Rect(WIDTH // 2 - 185, 300 + 50, 300, 40),
            manager=self.manager,
            object_id="PLAYER1",
            initial_text="Player1",
        )

        entry_line2 = UITextEntryLine(
            relative_rect=pygame.Rect(WIDTH // 2 - 185, 300 + 50 * 2, 300, 40),
            manager=self.manager,
            object_id="PLAYER2",
            initial_text="Player2",
        )

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
        self.ai_lines = [None, ai_line2]  # We need a None to have the list of the right lenght

        self.players = [
            {"name": "Player1", "color": CAR_RED, "bot": False},
            {"name": "Player2", "color": CAR_BLACK, "bot": True},
        ]

        self.font = pygame.font.Font(None, 32)

    def show_start_menu(self):
        while self.running:
            time_delta = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if (
                        event.ui_element == self.quit_button or event.type == pygame.QUIT
                    ):  # quit_button.collidepoint(mouse_pos) == 'QUIT' or event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    elif event.ui_element == self.start_button:
                        print("start")
                        # start game
                        self.running = False
                        self.update_player()

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
                        self.start_button.set_position((WIDTH // 2 - 100, 450 + (self.num_players - 1) * 50))
                        self.quit_button.set_position((WIDTH // 2 - 100, 510 + (self.num_players - 1) * 50))

                    # Bottone "+" per aumentare il numero di giocatori
                    elif event.ui_element == self.plus_button and self.num_players < 6:
                        self.num_players += 1
                        entry_line = UITextEntryLine(
                            relative_rect=pygame.Rect(WIDTH // 2 - 185, 300 + 50 * self.num_players - 1, 300, 40),
                            manager=self.manager,
                            object_id="PLAYER" + str(self.num_players),
                            initial_text="Player" + str(self.num_players),
                        )
                        car_line = UIDropDownMenu(
                            relative_rect=pygame.Rect(WIDTH // 2 + 115, 300 + 50 * self.num_players - 1, 80, 40),
                            options_list=["RED", "BLACK", "BLUE", "YELLOW"],
                            starting_option="RED",
                            manager=self.manager,
                            object_id="CAR" + str(self.num_players),
                        )
                        ai_line = UIDropDownMenu(
                            relative_rect=pygame.Rect(WIDTH // 2 + 195, 300 + 50 * self.num_players - 1, 80, 40),
                            options_list=["BOT", "UMANO"],
                            starting_option="BOT",
                            manager=self.manager,
                            object_id="BOT" + str(self.num_players),
                        )
                        self.entry_lines.append(entry_line)
                        self.car_lines.append(car_line)
                        self.ai_lines.append(ai_line)
                        self.start_button.set_position((WIDTH // 2 - 100, 450 + (self.num_players - 1) * 50))
                        self.quit_button.set_position((WIDTH // 2 - 100, 510 + (self.num_players - 1) * 50))
                        self.players.append({"name": "Player" + str(self.num_players), "color": CAR_RED, "bot": True})

                self.manager.process_events(event)

            self.manager.update(time_delta)

            self.screen.fill(WHITE)

            # Visualizza il numero di giocatori
            num_players_display = self.font.render(str(self.num_players), True, BLACK)
            self.screen.blit(num_players_display, (WIDTH // 2 - num_players_display.get_width() // 2, 240))

            self.manager.draw_ui(self.screen)

            # Testo del menu
            title_text = self.font.render("Menu di Gioco", True, BLACK)
            self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

            num_players_text = self.font.render("Numero di giocatori:", True, BLACK)
            self.screen.blit(num_players_text, (WIDTH // 2 - num_players_text.get_width() // 2, 200))

            player_names_text = self.font.render("Nomi dei giocatori:", True, BLACK)
            self.screen.blit(player_names_text, (WIDTH // 2 - player_names_text.get_width() // 2, 300))

            pygame.display.flip()

    def color_to_costant(self, color) -> str:
        colors = [
            {"color": "RED", "costant": CAR_RED},
            {"color": "BLACK", "costant": CAR_BLACK},
            {"color": "BLUE", "costant": CAR_BLUE},
            {"color": "YELLOW", "costant": CAR_YELLOW},
        ]
        for c in colors:
            if c["color"] == color:
                return c["costant"]
        return CAR_RED

    def bot_to_bool(self, bot) -> bool:
        if bot == "BOT":
            return True
        return False

    def update_player(self) -> None:
        for i, entry in enumerate(self.entry_lines):
            self.players[i]["name"] = entry.text
        for i, car in enumerate(self.car_lines):
            self.players[i]["color"] = self.color_to_costant(car.selected_option)
        for i, ai in enumerate(self.ai_lines):
            if ai == None:
                self.players[i]["bot"] = False
            else:
                self.players[i]["bot"] = self.bot_to_bool(ai.selected_option)
