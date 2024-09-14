import pygame
from lib.constants import WIDTH, HEIGHT
from lib.game import Game
from lib.menu import Menu
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t","--test", action="store_true", help="Run the game in test mode")
args = parser.parse_args()

pygame.init()

clock = pygame.time.Clock()

def main():
    menu = Menu(WIDTH, HEIGHT, clock)
    menu.show_start_menu()
    #Game start
    if args.test:
        game = Game(WIDTH, HEIGHT, clock, menu.players, True)
    else:
        game = Game(WIDTH, HEIGHT, clock, menu.players)
    game.start()
    pygame.quit()

main()
