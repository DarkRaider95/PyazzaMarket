from .constants import INITIAL_BALANCE
from .car import Car

class Player:
    def __init__(self, playerName, car):
        self.playerName = playerName
        self.balance = INITIAL_BALANCE
        self.position = 0
        self.stocks = []
        self.car = Car(car)