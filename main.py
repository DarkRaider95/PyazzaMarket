# Assets: https://techwithtim.net/wp-content/uploads/2020/09/assets.zip
import pygame
from lib.constants import WIDTH, HEIGHT
from lib.game import Game
from lib.menu import Menu

pygame.init()

clock = pygame.time.Clock()
#FPS = 60

#WIN = pygame.display.set_mode((WIDTH, HEIGHT))
#pygame.display.set_caption('lib')

#def get_row_col_from_mouse(pos):
#    x, y = pos
#    row = y // SQUARE_SIZE
#    col = x // SQUARE_SIZE
#    return row, col

def main():
    menu = Menu(WIDTH, HEIGHT, clock)
    menu.show_start_menu()
    print(menu.player_names)
    game = Game(WIDTH, HEIGHT, clock)
    game.start()
    pygame.quit()
    #run = True
    #clock = pygame.time.Clock()
    #game = Game(WIN)
#
    #while run:
    #    clock.tick(FPS)
#
    #    if game.winner() != None:
    #        print(game.winner())
    #        run = False
#
    #    for event in pygame.event.get():
    #        if event.type == pygame.QUIT:
    #            run = False
    #        
    #        if event.type == pygame.MOUSEBUTTONDOWN:
    #            pos = pygame.mouse.get_pos()
    #            row, col = get_row_col_from_mouse(pos)
    #            game.select(row, col)
#
    #    game.update()
    #
    #pygame.quit()

main()