# Assets: https://techwithtim.net/wp-content/uploads/2020/09/assets.zip
import pygame
from lib.constants import WIDTH, HEIGHT
from lib.game import Game
from lib.menu import Menu

pygame.init()

clock = pygame.time.Clock()

def main():
    menu = Menu(WIDTH, HEIGHT, clock)
    menu.show_start_menu()
    #Game start
    game = Game(WIDTH, HEIGHT, clock, menu.player)
    game.start()
    pygame.quit()

main()