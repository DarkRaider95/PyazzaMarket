import pygame
import sys
from pygame_gui import UIManager
from pygame_gui.elements import UITextEntryLine, UIButton, UIDropDownMenu
import pygame_gui
from .constants import WIDTH, HEIGHT, WHITE, BLACK

# Inizializzazione della finestra di gioco
pygame.display.set_caption("Menu di Gioco")

class Menu:
    def __init__(self, width, height, clock):  #each player initialised with its data
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True # Used to shutdown the game
        self.width = width
        self.height = height
        self.num_players = 2
        self.clock = clock
        self.manager = UIManager((WIDTH, HEIGHT)) # Create something similar to pygame.display.set_mode((WIDTH, HEIGHT))

        # Bottone "Inizia partita"
        self.start_button = UIButton(relative_rect=pygame.Rect(WIDTH // 2 - 100, 450, 200, 50), # x, y, width, height
                                text="Inizia partita",
                                object_id = 'START',
                                manager=self.manager)

        # Bottone "Chiudi gioco"
        self.quit_button = UIButton(relative_rect=pygame.Rect(WIDTH // 2 - 100, 510, 200, 50),
                                text="Chiudi gioco",
                                object_id = 'QUIT',
                                manager=self.manager)
        
        # Bottone "-" per diminuire il numero di giocatori
        self.minus_button = UIButton(relative_rect=pygame.Rect(WIDTH // 2 - 50, 240, 40, 40),
                                text="-",
                                object_id = 'MINUS',
                                manager=self.manager)

        # Bottone "+" per aumentare il numero di giocatori
        self.plus_button = UIButton(relative_rect=pygame.Rect(WIDTH // 2 + 20, 240, 40, 40),
                                text="+",
                                object_id = 'PLUS',
                                manager=self.manager)
        
        #create one entry line and add it to the list
        entry_line1 = UITextEntryLine(relative_rect=pygame.Rect(WIDTH // 2 - 185, 300 + 50, 300, 40),
                                            manager=self.manager,
                                            object_id="PLAYER1",
                                            initial_text="Player1")
        
        entry_line2 = UITextEntryLine(relative_rect=pygame.Rect(WIDTH // 2 - 185, 300 + 50 * 2, 300, 40),
                                            manager=self.manager,
                                            object_id="PLAYER2",
                                            initial_text="Player2")

        car_line1 = UIDropDownMenu(relative_rect=pygame.Rect(WIDTH // 2 + 115, 300 + 50, 80, 40),
                                            options_list=['RED', 'BLACK', 'BLUE', 'YELLOW'],
                                            starting_option='RED',
                                            manager=self.manager,
                                            object_id="CAR1")
        
        car_line2 = UIDropDownMenu(relative_rect=pygame.Rect(WIDTH // 2 + 115, 300 + 50 * 2, 80, 40),
                                            options_list=['RED', 'BLACK', 'BLUE', 'YELLOW'],
                                            starting_option='BLACK',
                                            manager=self.manager,
                                            object_id="CAR2")

        self.entry_lines = [entry_line1, entry_line2]
        self.car_lines = [car_line1, car_line2]

        self.player_names = ["Player1", "Player2"]
        self.player_colors = ["RED", "BLACK"]

        self.font = pygame.font.Font(None, 32)
        
    def show_start_menu(self):        

        while self.running:
            time_delta = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.quit_button or event.type == pygame.QUIT:#quit_button.collidepoint(mouse_pos) == 'QUIT' or event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    elif event.ui_element == self.start_button:
                        print("start")
                        #start game
                        self.running = False
                        self.updatePlayerNames()
                        self.updatePlayerColors()                    

                    # Bottone "-" per diminuire il numero di giocatori
                    elif event.ui_element == self.minus_button and self.num_players > 2:                    
                        self.entry_lines[self.num_players-1].kill()
                        self.car_lines[self.num_players-1].kill()                        
                        self.num_players -= 1
                        self.player_names = self.player_names[:self.num_players]                  
                        self.entry_lines = self.entry_lines[:self.num_players]
                        self.car_lines = self.car_lines[:self.num_players]
                        self.start_button.set_position((WIDTH // 2 - 100, 450 + (self.num_players - 1) * 50))
                        self.quit_button.set_position((WIDTH // 2 - 100, 510 + (self.num_players - 1) * 50))

                    # Bottone "+" per aumentare il numero di giocatori
                    elif event.ui_element == self.plus_button and self.num_players < 6:
                        self.num_players += 1
                        entry_line = UITextEntryLine(relative_rect=pygame.Rect(WIDTH // 2 - 185, 300 + 50 * self.num_players - 1, 300, 40),
                                             manager=self.manager,
                                             object_id="PLAYER"+str(self.num_players),
                                             initial_text="Player"+str(self.num_players))
                        car_line = UIDropDownMenu(relative_rect=pygame.Rect(WIDTH // 2 + 115, 300 + 50 * self.num_players - 1, 80, 40),
                                            options_list=['RED', 'BLACK', 'BLUE', 'YELLOW'],
                                            starting_option='RED',
                                            manager=self.manager,
                                            object_id="CAR"+str(self.num_players))
                        self.entry_lines.append(entry_line)
                        self.car_lines.append(car_line)
                        self.start_button.set_position((WIDTH // 2 - 100, 450 + (self.num_players - 1) * 50))
                        self.quit_button.set_position((WIDTH // 2 - 100, 510 + (self.num_players - 1) * 50))
                        self.player_names.append("")

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

    def updatePlayerNames(self):
        for i, entry in enumerate(self.entry_lines):
            self.player_names[i] = entry.text

    def updatePlayerColors(self):
        for i, car in enumerate(self.car_lines):
            self.player_colors[i] = car.selected_option