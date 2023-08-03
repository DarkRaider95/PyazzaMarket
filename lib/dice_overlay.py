from .gameLogic import *

class dice_overlay:
    def __init__(self, gameUI, game) -> None:
        self.gameUI = gameUI
        self.game = game
        self.establishing_players_order = True # we use this variable to understand when we have launched the game for the first time
        self.highestScore = 0 # we save the score for deciding which is the play with the highest score that will start first
        self.who_will_start = 0 # we save the index of the player that will start first
        self.same_score = False # we use this variable to understand if we need to throw the dice again for decide who will start first
        self.second_round_who_start = [] # we save the players that have the same score for decide who will start first
        self.copy_of_second_round_who_start = [] # we need a copy in order to pop players from the list, and we don't want to modify the original list
        self.establish_player_again = False # this will be true in case of two or more player score the same number

    def launch_but_pressed(self):
        # when you throw the dices maybe you are deciding the order of the players
        # or you are in a chance cell
        if self.establishing_players_order:
            self.establish_players_order()
        elif self.establish_player_again:
            self.restablish_player_order()
        else:
            # amount is the amount of money that the player has to pay or receive
            score, amount = chance_logic(self.game.get_current_player(), self.game.get_square_balance())
            self.gameUI.updateDiceOverlay(score)
            self.game.set_square_balance(amount)
            self.gameUI.updateDice(score)

    def establish_players_order(self):
        self.roll_dice()
        if self.game.get_current_player_index() == len(self.game.get_players()) - 1:
            self.last_player_logic()

    def restablish_player_order(self):
        self.roll_dice()
        if self.copy_of_second_round_who_start == []:
            self.last_player_logic()

    def roll_dice(self):
        score = roll()
        self.gameUI.updateDiceOverlay(score)
        diceSum = score[0] + score[1]
        if self.highestScore < diceSum:
            self.who_will_start = self.game.get_current_player_index()
            self.highestScore = diceSum
            self.second_round_who_start = []
            self.same_score = False
        elif self.highestScore == diceSum:
            if self.second_round_who_start == []:
                # when more than two players have the same score we can't add again the first player
                self.second_round_who_start.append(self.who_will_start)
            self.second_round_who_start.append(self.game.get_current_player_index())
            self.same_score = True

    def last_player_logic(self):
        if not self.same_score:
            self.establishing_players_order = False
            self.establish_player_again = False
        if self.same_score:
            self.copy_of_second_round_who_start = self.second_round_who_start.copy()
            self.establish_player_again = True
            self.same_score = False # questo è false per i controlli del secondo round
            self.highestScore = 0

    def close_dice_overlay(self):
        if self.establish_player_again:
            self.gameUI.closeDiceOverlay(self.game.get_players(), self.gameUI)
            self.game.set_current_player_index(self.copy_of_second_round_who_start.pop(0)) 
            self.gameUI.updateTurnLabel(self.game.get_current_player())
            self.gameUI.drawDiceOverlay(self.game.get_current_player().get_name() + ' tira dadi', 'Decisione turni')
        elif self.establishing_players_order:
            self.gameUI.closeDiceOverlay(self.game.get_players(), self.gameUI)
            self.game.set_current_player_index((self.game.get_current_player_index() + 1) % len(self.game.get_players())) 
            self.gameUI.updateTurnLabel(self.game.get_current_player())
            self.gameUI.drawDiceOverlay(self.game.get_current_player().get_name() + ' tira dadi', 'Decisione turni')
        else:
            self.gameUI.closeDiceOverlay(self.game.get_players(), self.gameUI)