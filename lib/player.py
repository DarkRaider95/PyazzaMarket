from .constants import INITIAL_BALANCE, CELLS_DEF
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

    def setPosition(self, position):
        self.old_position = self.position
        self.position = position

    def stockValue(self):
        value = 0
        for stock in self.stocks:
            value += stock.stock_value

        return value

    def changeBalance(self, balance):
        self.balance += balance
    
    def addStock(self, stocks):
        self.stocks.append(stocks)

    def sameColorCount(self, color):
        count = 0
        for stock in self.stocks:
            if stock.color == color:
                count += 1
        return count

    def sameCompanyCount(self, stock1): # we check if the player own two stocks of the same company
        for stock2 in self.stocks:
            if stock1.name == stock2.name:
                return True

        return False

    def computePenalty(self, stock):
        sameColorCells = self.sameColorCount(stock.color)
        if sameColorCells >= 3: # if the player has more than 3 stocks of the same color, we will check wich is the right panalty
            return stock.penalties[sameColorCells - 1]
        elif sameColorCells == 2: # we check if the player own two stocks of the same company
            if self.sameCompanyCount(stock):
                return stock.penalties[1]
        return stock.penalties[0] # this will return if the stock of the company is only one