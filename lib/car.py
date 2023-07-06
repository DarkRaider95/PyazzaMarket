import pygame
from .constants import *

class Car:
    def __init__(self, car):
        self.image = pygame.image.load(car)
        self.image = pygame.transform.scale(self.image, (CAR_WIDTH, CAR_HEIGHT))
        self.angle = 0
        self.x = 0
        self.y = 0

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self, x, y):
        self.x = x
        self.y = y

    def rotate(self, angle):
        self.angle = angle
        self.image = pygame.transform.rotate(self.image, self.angle)