import pygame
import sys
from pygame_gui import UIManager
from pygame_gui.elements import UITextEntryLine, UIButton
import pygame_gui

pygame.init()

# Dimensioni della finestra
WIDTH = 800
HEIGHT = 1000

# Colori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Inizializzazione della finestra di gioco
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu di Gioco")

clock = pygame.time.Clock()

def show_start_menu():
    running = True

    # Numero di giocatori
    num_players = 1

    # Nomi dei giocatori
    player_names = [""] * num_players

    manager = UIManager((WIDTH, HEIGHT))

    font = pygame.font.Font(None, 32)

    # Bottone "Inizia partita"
    start_button = UIButton(relative_rect=pygame.Rect(WIDTH // 2 - 100, 450, 200, 50),
                            text="Inizia partita",
                            object_id = 'START',
                            manager=manager)

    # Bottone "Chiudi gioco"
    quit_button = UIButton(relative_rect=pygame.Rect(WIDTH // 2 - 100, 510, 200, 50),
                            text="Chiudi gioco",
                            object_id = 'QUIT',
                            manager=manager)
    
    # Bottone "-" per diminuire il numero di giocatori
    minus_button = UIButton(relative_rect=pygame.Rect(WIDTH // 2 - 50, 240, 40, 40),
                            text="-",
                            object_id = 'MINUS',
                            manager=manager)

    # Bottone "+" per aumentare il numero di giocatori
    plus_button = UIButton(relative_rect=pygame.Rect(WIDTH // 2 + 20, 240, 40, 40),
                            text="+",
                            object_id = 'PLUS',
                            manager=manager)
    
    #create one entry line and add it to the list
    entry_line = UITextEntryLine(relative_rect=pygame.Rect(WIDTH // 2 - 150, 300 + 50, 300, 40),
                                         manager=manager,
                                         object_id="PLAYER1")
    entry_lines = [entry_line]

    while running:
        time_delta = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                # Salva il nome del giocatore quando viene premuto Invio
                element_id = event.ui_element.get_relative_to_container_id()
                player_names[element_id] = event.text

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == quit_button or event.type == pygame.QUIT:#quit_button.collidepoint(mouse_pos) == 'QUIT' or event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.ui_element == start_button:
                    print("start")
                    #start game

                # Bottone "-" per diminuire il numero di giocatori
                elif event.ui_element == minus_button and num_players > 1:                    
                    entry_lines[num_players-1].kill()                        
                    num_players -= 1
                    player_names = player_names[:num_players]                  
                    entry_lines = entry_lines[:num_players]
                    start_button.set_position((WIDTH // 2 - 100, 450 + (num_players - 1) * 50))
                    quit_button.set_position((WIDTH // 2 - 100, 510 + (num_players - 1) * 50))

                # Bottone "+" per aumentare il numero di giocatori
                elif event.ui_element == plus_button and num_players < 6:
                    num_players += 1
                    entry_line = UITextEntryLine(relative_rect=pygame.Rect(WIDTH // 2 - 150, 300 + 50 * num_players - 1, 300, 40),
                                         manager=manager,
                                         object_id="PLAYER"+str(num_players))
                    entry_lines.append(entry_line)
                    start_button.set_position((WIDTH // 2 - 100, 450 + (num_players - 1) * 50))
                    quit_button.set_position((WIDTH // 2 - 100, 510 + (num_players - 1) * 50))
                    player_names.append("")

            manager.process_events(event)

        manager.update(time_delta)

        screen.fill(WHITE)

        # Testo del menu
        title_text = font.render("Menu di Gioco", True, BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

        num_players_text = font.render("Numero di giocatori:", True, BLACK)
        screen.blit(num_players_text, (WIDTH // 2 - num_players_text.get_width() // 2, 200))

        player_names_text = font.render("Nomi dei giocatori:", True, BLACK)
        screen.blit(player_names_text, (WIDTH // 2 - player_names_text.get_width() // 2, 300))

        # Visualizza il numero di giocatori
        num_players_display = font.render(str(num_players), True, BLACK)
        screen.blit(num_players_display, (WIDTH // 2 - num_players_display.get_width() // 2, 240))
        
        manager.draw_ui(screen)

        pygame.display.flip()

show_start_menu()
