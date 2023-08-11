from lib.constants import INITIAL_BALANCE
from lib.car import Car
import time
from typing import Optional
from lib.stock import Stock

class Player:
    last_stock_update = None

    def __init__(self, playerName, car, bot):
        self.__playerName = playerName
        self.__balance = INITIAL_BALANCE
        self.__position = 0
        self.__stocks = []
        self.__car = Car(car)
        self.__old_position = 0
        self.__set_skip_turn = False
        self.__freePenalty = False
        self.__free_martini = False
        self.__is_bot = bot

    def move(self, step):
        self.__old_position = self.__position
        self.__position = (self.__position + step) % 40

    def set_position(self, position):
        self.__old_position = self.__position
        self.__position = position

    def stock_value(self):
        value = 0
        for stock in self.__stocks:
            value += stock.get_stock_value()

        return value
    
    def add_stock(self, stock):
        self.__stocks.append(stock)
        self.__stocks = sorted(self.__stocks, key=lambda x: x.get_position())
        Player.last_stock_update = time.time()

    def same_color_count(self, color):
        count = 0
        for stock in self.__stocks:
            if stock.color == color:
                count += 1
        return count

    def compute_penalty(self, choosen_stock):
        stock_to_remove_index = None

        same_color_cells = self.same_color_count(choosen_stock.color)
        if same_color_cells >= 3: # if the player has more than 3 stocks of the same color, we will check wich is the right panalty
            return choosen_stock.get_penalty()[same_color_cells - 1]
        elif same_color_cells == 2: # we check if the player own two stocks of the same company
            stocks = self.__stocks.copy() # create a copy of stocks
            
            for i, stock in enumerate(stocks): # cycle for pop choosen_stock
                if stock.get_position() == choosen_stock.get_position():
                    stock_to_remove_index = i
            if stock_to_remove_index is not None:
                stocks.pop(stock_to_remove_index)

            for stock in stocks: # if the stock is the same return the right penalty
                if stock.get_name() == choosen_stock.get_name():
                    return choosen_stock.get_penalty()[1]
        return choosen_stock.get_penalty()[0] # this will return if the stock of the company is only one
    
    def get_stock_by_pos(self, stock_pos) -> Optional[Stock]:
        for stock in self.__stocks:
            if stock.get_position() == stock_pos:
                return stock
            
        return None
    
    def remove_stock(self, chosen_stock):
        stock_to_remove_index = None
        
        for i, stock in enumerate(self.__stocks):
            if stock.get_position() == chosen_stock.get_position():
                stock_to_remove_index = i
        if stock_to_remove_index is not None:
            self.__stocks.pop(stock_to_remove_index)

    # all the getters and setters are below

    def get_stocks(self): # pragma: no cover
        return self.__stocks.copy()
    
    def set_skip_turn(self, skip): # pragma: no cover
        self.__set_skip_turn = skip

    def get_skip_turn(self): # pragma: no cover
        return self.__set_skip_turn
    
    def freePenalty(self, free): # pragma: no cover
        self.__freePenalty = free

    def get_free_penalty(self): # pragma: no cover
        return self.__freePenalty
    
    def set_free_martini(self, free): # pragma: no cover
        self.__free_martini = free

    def get_free_martini(self): # pragma: no cover
        return self.__free_martini

    def get_balance(self): # pragma: no cover
        return self.__balance
    
    def get_name(self): # pragma: no cover
        return self.__playerName
    
    def change_balance(self, balance): # pragma: no cover
        self.__balance += balance

    def get_position(self): # pragma: no cover
        return self.__position
    
    def get_old_position(self): # pragma: no cover
        return self.__old_position
    
    def get_car(self): # pragma: no cover
        return self.__car
    
    def get_is_bot(self): # pragma: no cover
        return self.__is_bot