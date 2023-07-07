from .constants import INITIAL_BALANCE
from .car import Car

class Player:
    def __init__(self, playerName, car):
        self.playerName = playerName
        self.balance = INITIAL_BALANCE
        self.position = 0
        self.stocks = []
        self.car = Car(car)
        self.old_position = 0

    def move(self, step):
        self.old_position = self.position
        self.position = (self.position + step) % 40