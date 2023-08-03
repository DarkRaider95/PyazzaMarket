from .gameLogic import *

class DiceOverlay:
    def __init__(self, __game) -> None:
        self.__gameUI = __game.get_gameUI()
        self.__game = __game
        self.__establishing_players_order = True # we use this variable to understand when we have launched the __game for the first time
        self.__highestScore = 0 # we save the score for deciding which is the play with the highest score that will start first
        self.__who_will_start = 0 # we save the index of the player that will start first
        self.__same_score = False # we use this variable to understand if we need to throw the dice again for decide who will start first
        self.__second_round_who_start = [] # we save the players that have the same score for decide who will start first
        self.__copy_of_second_round_who_start = [] # we need a copy in order to pop players from the list, and we don't want to modify the original list
        self.__establish_player_again = False # this will be true in case of two or more player score the same number

    def launch_but_pressed(self): # pragma: no cover
        # when you throw the dices maybe you are deciding the order of the players
        # or you are in a chance cell
        if self.__establishing_players_order:
            self.establish_players_order()
        elif self.__establish_player_again:
            self.restablish_player_order()
        else:
            # amount is the amount of money that the player has to pay or receive
            score, amount = chance_logic(self.__game.get_current_player(), self.__game.get_square_balance())
            self.__gameUI.updateDiceOverlay(score)
            self.__game.set_square_balance(amount)
            self.__gameUI.updateDice(score)

    def establish_players_order(self): # pragma: no cover
        self.roll_dice()
        if self.__game.get_current_player_index() == len(self.__game.get_players()) - 1:
            self.last_player_logic()

    def restablish_player_order(self): # pragma: no cover
        self.roll_dice()
        if self.__copy_of_second_round_who_start == []:
            self.last_player_logic()

    def roll_dice(self):
        score = roll()
        self.__gameUI.updateDiceOverlay(score)
        diceSum = score[0] + score[1]
        if self.__highestScore < diceSum:
            self.__who_will_start = self.__game.get_current_player_index()
            self.__highestScore = diceSum
            self.__second_round_who_start = []
            self.__same_score = False
        elif self.__highestScore == diceSum:
            if self.__second_round_who_start == []:
                # when more than two players have the same score we can't add again the first player
                self.__second_round_who_start.append(self.__who_will_start)
            self.__second_round_who_start.append(self.__game.get_current_player_index())
            self.__same_score = True

    def last_player_logic(self): # pragma: no cover
        if not self.__same_score:
            self.__establishing_players_order = False
            self.__establish_player_again = False
        if self.__same_score:
            self.__copy_of_second_round_who_start = self.__second_round_who_start.copy()
            self.__establish_player_again = True
            self.__same_score = False # questo è false per i controlli del secondo round
            self.__highestScore = 0

    def close_dice_overlay(self): # pragma: no cover
        if self.__establish_player_again:
            self.__gameUI.closeDiceOverlay(self.__game.get_players(), self.__gameUI)
            self.__game.set_current_player_index(self.__copy_of_second_round_who_start.pop(0)) 
            self.__gameUI.updateTurnLabel(self.__game.get_current_player())
            self.__gameUI.drawDiceOverlay(self.__game.get_current_player().get_name() + ' tira dadi', 'Decisione turni')
        elif self.__establishing_players_order:
            self.__gameUI.closeDiceOverlay(self.__game.get_players(), self.__gameUI)
            self.__game.set_current_player_index((self.__game.get_current_player_index() + 1) % len(self.__game.get_players())) 
            self.__gameUI.updateTurnLabel(self.__game.get_current_player())
            self.__gameUI.drawDiceOverlay(self.__game.get_current_player().get_name() + ' tira dadi', 'Decisione turni')
        else:
            self.__gameUI.closeDiceOverlay(self.__game.get_players(), self.__gameUI)

    # getters created for test purposes
    def get_who_will_start(self): # pragma: no cover
        return self.__who_will_start
    
    def get_hihgest_score(self): # pragma: no cover
        return self.__highestScore
    
    def get_second_round_who_start(self): # pragma: no cover
        return self.__second_round_who_start.copy()