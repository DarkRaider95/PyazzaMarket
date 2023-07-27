import pygame
from .constants import *
from pygame_gui import UIManager
from pygame_gui.elements import UIButton, UIPanel, UILabel, UIImage

# CARICARE LE IMMAGINI DEI DADI IN RAM

class Dice:
    # create initial dice
    def __init__(self, screen):
        self.image_dice_1 = pygame.image.load(DICE_1)
        self.image_dice_1 = pygame.transform.scale(self.image_dice_1, (DICE_WIDTH, DICE_HEIGHT))
        self.image_dice_2 = pygame.image.load(DICE_1)
        self.image_dice_2 = pygame.transform.scale(self.image_dice_2, (DICE_WIDTH, DICE_HEIGHT))
        self.screen = screen

    def drawDices(self):
        surface = pygame.Surface((DICE_WIDTH * 2, DICE_HEIGHT))
        surface.blit(self.image_dice_1, (0, 0))
        surface.blit(self.image_dice_2, (0 + DICE_WIDTH, 0))
        self.screen.blit(surface, (DICE_SURFACE_X, DICE_SURFACE_Y))

    def updateDice(self, score): # score is a tuple from roll in gameLogic
        scoreToImage = [{"score": 1, "image": DICE_1},{"score": 2, "image": DICE_2},{"score": 3, "image": DICE_3},{"score": 4, "image": DICE_4},{"score": 5, "image": DICE_5},{"score": 6, "image": DICE_6}]
        for scoreImage in scoreToImage:
            if(scoreImage["score"] == score[0]):
                self.image_dice_1 = pygame.image.load(scoreImage["image"])
                self.image_dice_1 = pygame.transform.scale(self.image_dice_1, (DICE_WIDTH, DICE_HEIGHT))
            if(scoreImage["score"] == score[1]):
                self.image_dice_2 = pygame.image.load(scoreImage["image"])
                self.image_dice_2 = pygame.transform.scale(self.image_dice_2, (DICE_WIDTH, DICE_HEIGHT))
            
        self.drawDices()