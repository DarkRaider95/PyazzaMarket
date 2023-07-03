from .constants import INITIAL_BALANCE

class Player:
    def __init__(self, playerName):
        self.playerName = playerName
        self.balance = INITIAL_BALANCE
        self.stocks = []    