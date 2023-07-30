from .constants import INITIAL_BALANCE, CELLS_DEF
from .car import Car
import time
class Player:
    last_stock_update = None

    def __init__(self, playerName, car):
        self.playerName = playerName
        self.__balance = INITIAL_BALANCE
        self.position = 0
        self.__stocks = []
        self.car = Car(car)
        self.old_position = 0
        self.stockUpdatedAt = time.time()
        self.__skipTurn = False
        self.__freePenalty = False
        self.__freeMartini = False

    def move(self, step):
        self.old_position = self.position
        self.position = (self.position + step) % 40

    def set_position(self, position):
        self.old_position = self.position
        self.position = position

    def stockValue(self):
        value = 0
        for stock in self.__stocks:
            value += stock.get_stock_value()

        return value

    def getName(self):
        return self.playerName

    def change_balance(self, balance):
        self.__balance += balance
    
    def add_stock(self, stock):
        self.__stocks.append(stock)
        self.__stocks = sorted(self.__stocks, key=lambda x: x.get_position())
        Player.last_stock_update = time.time()

    def sameColorCount(self, color):
        count = 0
        for stock in self.__stocks:
            if stock.color == color:
                count += 1
        return count

    def sameCompanyCount(self, stock1): # we check if the player own two stocks of the same company
        for stock2 in self.__stocks:
            if stock1.name == stock2.name:
                return True

        return False

    def computePenalty(self, stock):
        sameColorCells = self.sameColorCount(stock.color)
        if sameColorCells >= 3: # if the player has more than 3 stocks of the same color, we will check wich is the right panalty
            return stock.getPenalty()[sameColorCells - 1]
        elif sameColorCells == 2: # we check if the player own two stocks of the same company
            if self.sameCompanyCount(stock):
                return stock.getPenalty()[1]
        return stock.getPenalty()[0] # this will return if the stock of the company is only one
    
    def getStockByPos(self, stockPos):
        for stock in self.__stocks:
            if stock.get_position() == stockPos:
                return stock
            
        return None
    
    def remove_stock(self, chosen_stock):
        stock_to_remove_index = None
        
        for i, stock in enumerate(self.__stocks):
            if stock.get_position() == chosen_stock.get_position():
                stock_to_remove_index = i

        self.__stocks.pop(stock_to_remove_index)

    def get_stocks(self):
        return self.__stocks.copy()
    
    def skipTurn(self, skip):
        self.__skipTurn = skip

    def getSkipTurn(self):
        return self.__skipTurn
    
    def freePenalty(self, free):
        self.__freePenalty = free

    def getFreePenalty(self):
        return self.__freePenalty
    
    def freeMartini(self, free):
        self.__freeMartini = free

    def getFreeMartini(self):
        return self.__freeMartini

    def get_balance(self):
        return self.__balance