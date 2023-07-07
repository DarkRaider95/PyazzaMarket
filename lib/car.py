import pygame
from .constants import *

class Car:
    def __init__(self, car):
        self.original_image = pygame.image.load(car)
        self.original_image = pygame.transform.scale(self.original_image, (CAR_WIDTH, CAR_HEIGHT))
        self.image = pygame.transform.rotate(self.original_image, 90)
        self.x = 0
        self.y = 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
    
    def move(self, x, y):
        self.x = x
        self.y = y

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.original_image, angle)