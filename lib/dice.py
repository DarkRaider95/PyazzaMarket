import pygame
from .constants import DICE_1, DICE_2, DICE_3, DICE_4, DICE_5, DICE_6, DICE_WIDTH, DICE_HEIGHT, CELL_WIDTH, CELL_HEIGHT, WIDTH, HEIGHT, CORNER_WIDTH, CORNER_HEIGHT

# CARICARE LE IMMAGINI DEI DADI IN RAM

class Dice:
    # create initial dice
    def __init__(self):
        self.image_dice_1 = pygame.image.load(DICE_1)
        self.image_dice_1 = pygame.transform.scale(self.image_dice_1, (DICE_WIDTH, DICE_HEIGHT))
        self.image_dice_2 = pygame.image.load(DICE_1)
        self.image_dice_2 = pygame.transform.scale(self.image_dice_2, (DICE_WIDTH, DICE_HEIGHT))
        self.surface_x = WIDTH - 5 - CORNER_WIDTH - (CELL_WIDTH * 9)
        self.surface_y = 20 + CELL_HEIGHT
        self.score_dice_1 = 1
        self.score_dice_2 = 1
        self.surface = pygame.Surface((DICE_WIDTH * 2, DICE_HEIGHT))

    def drawDices(self, screen):
        self.surface.blit(self.image_dice_1, (0, 0))
        self.surface.blit(self.image_dice_2, (0 + DICE_WIDTH, 0))
        screen.blit(self.surface, (self.surface_x, self.surface_y))

    def updateDice(self, score): # score is a tuple from roll in gameLogic
        scoreToImage = [{"score": 1, "image": DICE_1},{"score": 2, "image": DICE_2},{"score": 3, "image": DICE_3},{"score": 4, "image": DICE_4},{"score": 5, "image": DICE_5},{"score": 6, "image": DICE_6}]
        for scoreImage in scoreToImage:
            if(scoreImage["score"] == score[0]):
                self.image_dice_1 = pygame.image.load(scoreImage["image"])
                self.image_dice_1 = pygame.transform.scale(self.image, (DICE_WIDTH, DICE_HEIGHT))
            if(scoreImage["score"] == score[1]):
                self.image_dice_2 = pygame.image.load(scoreImage["image"])
                self.image_dice_2 = pygame.transform.scale(self.image, (DICE_WIDTH, DICE_HEIGHT))
            
        self.score_dice_1 = score[0]
        self.score_dice_2 = score[1]