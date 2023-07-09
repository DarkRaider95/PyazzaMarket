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

    def stockValue(self):
        value = 0
        for stock in self.stocks:
            value += stock.stock_value

        return value

    def changeBalance(self, balance):
        self.balance += balance
    
    def addStock(self, stocks):
        self.stocks.append(stocks)