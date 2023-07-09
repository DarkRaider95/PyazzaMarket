import pygame
from pygame_gui import UIManager
from pygame_gui.elements import UIButton, UIPanel, UILabel
from .constants import *

# Inizializzazione della finestra di gioco
pygame.display.set_caption("Menu di Gioco")

class GameUI:
    def __init__(self, screen, clock):  #each player initialised with its data
        self.screen = screen
        self.running = True # Used to shutdown the game
        self.clock = clock
        self.manager = UIManager((WIDTH, HEIGHT)) # Create something similar to pygame.display.set_mode((WIDTH, HEIGHT))

        #self.actions_UI = pygame.Surface((ACTIONS_WIDTH, ACTIONS_HEIGHT))
        #self.actions_rect = pygame.Rect(30, HEIGHT - 30 - ACTIONS_HEIGHT, ACTIONS_WIDTH, ACTIONS_HEIGHT)#pygame.Surface((ACTIONS_WIDTH, ACTIONS_HEIGHT))
        self.actions_UI = None        
    

    def draw_actions_ui(self):
        panel_rect = pygame.Rect((30, HEIGHT - 30 - ACTIONS_HEIGHT), (ACTIONS_WIDTH, ACTIONS_HEIGHT))
        self.actions_UI = UIPanel(panel_rect, manager=self.manager)
        self.actions_UI.background_colour = WHITE
        #actionLabel = self.font.render(str('AZIONI'), True, BLACK)
        panel_rect = pygame.Rect((30, HEIGHT - 30 - ACTIONS_HEIGHT), (ACTIONS_WIDTH, ACTIONS_HEIGHT))
        label_rect = pygame.Rect((ACTIONS_WIDTH // 2 - LABEL_WIDTH // 2, 10), (LABEL_WIDTH, LABEL_HEIGHT))
        self.actionLabel = UILabel(label_rect, "AZIONI", manager=self.manager, container=self.actions_UI)
        #self.actions_UI.blit(actionLabel, (ACTIONS_WIDTH // 2 - actionLabel.get_width() // 2, 10))
        # Bottone "Inizia partita"
        self.launchDice = UIButton(relative_rect=pygame.Rect(ACTIONS_WIDTH // 2 - BUTTON_WIDTH // 2, 50, BUTTON_WIDTH, BUTTON_HEIGHT),
                                text="Lancia i dadi",
                                container=self.actions_UI,
                                object_id = 'LAUNCH_DICE',
                                manager=self.manager)

        # Bottone "Chiudi gioco"
        self.buyButton = UIButton(relative_rect=pygame.Rect(ACTIONS_WIDTH // 2 - BUTTON_WIDTH // 2, 100, BUTTON_WIDTH, BUTTON_HEIGHT),
                                text="Compra",
                                container=self.actions_UI,
                                object_id = 'BUY',
                                manager=self.manager)
        
        self.buyButton.disable()
        
        # Bottone "-" per diminuire il numero di giocatori
        self.showStocks = UIButton(relative_rect=pygame.Rect(ACTIONS_WIDTH // 2 - BUTTON_WIDTH // 2, 150, BUTTON_WIDTH, BUTTON_HEIGHT),
                                text="Mostra Cedole",
                                container=self.actions_UI,
                                object_id = 'SHOW_STOCKS',
                                manager=self.manager)
        

        self.passButton = UIButton(relative_rect=pygame.Rect(ACTIONS_WIDTH // 2 - BUTTON_WIDTH // 2, 200, BUTTON_WIDTH, BUTTON_HEIGHT),
                                text="Passa il turno",
                                container=self.actions_UI,
                                object_id = 'PASS',
                                manager=self.manager)
        
        self.passButton.disable()
        

        #self.actions_UI.add(self.launchDice)
        #self.actions_UI.add(self.buyButton)
        #self.actions_UI.add(self.showStocks)
        #self.actions_UI.add(self.passButton)
        #pygame.draw.rect(self.screen, WHITE, self.actions_rect)
        #self.screen.blit(self.actions_UI, (30, HEIGHT - 30 - ACTIONS_HEIGHT))
        

#    def show_start_menu(self):        
#
#        while self.running:
#            time_delta = self.clock.tick(60) / 1000.0
#
#            for event in pygame.event.get():
#                if event.type == pygame_gui.UI_BUTTON_PRESSED:
#                    if event.ui_element == self.quit_button or event.type == pygame.QUIT:#quit_button.collidepoint(mouse_pos) == 'QUIT' or event.type == pygame.QUIT:
#                        pygame.quit()
#                        sys.exit()
#
#                    elif event.ui_element == self.start_button:
#                        print("start")
#                        #start game
#                        self.running = False                  
#                        self.updatePlayer()
#
#                    # Bottone "-" per diminuire il numero di giocatori
#                    elif event.ui_element == self.minus_button and self.num_players > 2:                    
#                        self.entry_lines[self.num_players-1].kill()
#                        self.car_lines[self.num_players-1].kill()                        
#                        self.num_players -= 1
#                        self.player = self.player[:self.num_players]                  
#                        self.entry_lines = self.entry_lines[:self.num_players]
#                        self.car_lines = self.car_lines[:self.num_players]
#                        self.start_button.set_position((WIDTH // 2 - 100, 450 + (self.num_players - 1) * 50))
#                        self.quit_button.set_position((WIDTH // 2 - 100, 510 + (self.num_players - 1) * 50))
#
#                    # Bottone "+" per aumentare il numero di giocatori
#                    elif event.ui_element == self.plus_button and self.num_players < 6:
#                                self.num_players += 1
#                                entry_line = UITextEntryLine(relative_rect=pygame.Rect(WIDTH // 2 - 185, 300 + 50 * self.num_players - 1, 300, 40),
#                                                            manager=self.manager,
#                                                            object_id="PLAYER"+str(self.num_players),
#                                                            initial_text="Player"+str(self.num_players))
#                                car_line = UIDropDownMenu(relative_rect=pygame.Rect(WIDTH // 2 + 115, 300 + 50 * self.num_players - 1, 80, 40),
#                                                            options_list=['RED', 'BLACK', 'BLUE', 'YELLOW'],
#                                                            starting_option='RED',
#                                                            manager=self.manager,
#                                                            object_id="CAR"+str(self.num_players))
#                                self.entry_lines.append(entry_line)
#                                self.car_lines.append(car_line)
#                                self.start_button.set_position((WIDTH // 2 - 100, 450 + (self.num_players - 1) * 50))
#                                self.quit_button.set_position((WIDTH // 2 - 100, 510 + (self.num_players - 1) * 50))
#                                self.player.append({"name":"Player"+str(self.num_players), "color": CAR_RED})
#
#                self.manager.process_events(event)
#
#            self.manager.update(time_delta)
#
#            self.screen.fill(WHITE)
#
#            # Visualizza il numero di giocatori
#            num_players_display = self.font.render(str(self.num_players), True, BLACK)
#            self.screen.blit(num_players_display, (WIDTH // 2 - num_players_display.get_width() // 2, 240))
#
#            self.manager.draw_ui(self.screen)
#
#            # Testo del menu
#            title_text = self.font.render("Azioni", True, BLACK)
#            self.screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
#
#            num_players_text = self.font.render("Numero di giocatori:", True, BLACK)
#            self.screen.blit(num_players_text, (WIDTH // 2 - num_players_text.get_width() // 2, 200))
#
#            player_names_text = self.font.render("Nomi dei giocatori:", True, BLACK)
#            self.screen.blit(player_names_text, (WIDTH // 2 - player_names_text.get_width() // 2, 300))        
#
#            pygame.display.flip()