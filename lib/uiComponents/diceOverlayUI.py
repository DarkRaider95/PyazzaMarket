from lib.gameLogic import *
import pygame
from pygame_gui.elements import UIButton, UIPanel, UILabel, UIImage
from lib.constants import *
import time

class DiceOverlay:
    #TODO remove variables that aren't needed
    def __init__(self, __game, message, title, actions_status, twoDices=True) -> None:
        self.__gameUI = __game.get_gameUI()
        self.__game = __game
        self.__establishing_players_order = True # we use this variable to understand when we have launched the __game for the first time
        self.__highestScore = 0 # we save the score for deciding which is the play with the highest score that will start first
        self.__who_will_start = 0 # we save the index of the player that will start first
        self.__same_score = False # we use this variable to understand if we need to throw the dice again for decide who will start first
        self.__second_round_who_start = [] # we save the players that have the same score for decide who will start first
        self.__copy_of_second_round_who_start = [] # we need a copy in order to pop players from the list, and we don't want to modify the original list
        self.__establish_player_again = False # this will be true in case of two or more player score the same number
        self.__test = self.__game.get_test()
        self.__actions_status = actions_status
        self.manager = self.__gameUI.get_manager()
        #dice images
        self.image_dice_1 = pygame.image.load(DICE_1)
        self.image_dice_1 = pygame.transform.scale(
            self.image_dice_1, (DICE_WIDTH, DICE_HEIGHT)
        )
        self.image_dice_2 = pygame.image.load(DICE_1)
        self.image_dice_2 = pygame.transform.scale(
            self.image_dice_2, (DICE_WIDTH, DICE_HEIGHT)
        )

        self.message = message
        self.title = title
        # this is used when we update the dice overlay image to know if the
        # overlay have one or two dices
        self.twoDices = twoDices

    def draw(self):
        surface = pygame.Rect(
            ((WIDTH - DICE_OVERLAY_WIDTH) // 2, (HEIGHT - DICE_OVERLAY_HEIGHT) // 2),
            (DICE_OVERLAY_WIDTH, DICE_OVERLAY_HEIGHT),
        )
        self.diceOverlay = UIPanel(surface, starting_height=2, manager=self.manager)

        title_rect = pygame.Rect(
            ((DICE_OVERLAY_WIDTH - ALERT_MESSAGE_WIDTH) // 2, 10),
            (ALERT_MESSAGE_WIDTH, ALERT_MESSAGE_HEIGHT),
        )
        UILabel(title_rect, self.title, manager=self.manager, container=self.diceOverlay)

        message_rect = pygame.Rect(
            ((DICE_OVERLAY_WIDTH - ALERT_MESSAGE_WIDTH) // 2, 30),
            (ALERT_MESSAGE_WIDTH, ALERT_MESSAGE_HEIGHT),
        )
        UILabel(message_rect, self.message, manager=self.manager, container=self.diceOverlay)

        close_rect = pygame.Rect(
            (
                DICE_OVERLAY_WIDTH - ALERT_BUT_WIDTH - 20,
                DICE_OVERLAY_HEIGHT - ALERT_BUT_HEIGHT - 10,
            ),
            (ALERT_BUT_WIDTH, ALERT_BUT_HEIGHT),
        )

        if self.twoDices:
            imgRect = pygame.Rect(
                (DICE_OVERLAY_WIDTH // 2 - DICE_WIDTH, 65),
                (DICE_WIDTH * 2, DICE_HEIGHT),
            )
            diceSurface = self.createDiceSurface()
            self.diceOverlayImg = UIImage(
                imgRect, diceSurface, manager=self.manager, container=self.diceOverlay
            )

            self.closeDiceOverlayBut = UIButton(
                relative_rect=close_rect,
                text="Chiudi",
                container=self.diceOverlay,
                object_id="CLOSE_DICE_OVERLAY",
                manager=self.manager,
            )
            self.closeDiceOverlayBut.disable()
        else:
            imgRect = pygame.Rect(
                ((DICE_OVERLAY_WIDTH - DICE_WIDTH) // 2, 65), (DICE_WIDTH, DICE_HEIGHT)
            )
            diceSurface = self.createDiceSurface()
            self.diceOverlayImg = UIImage(
                imgRect, diceSurface, manager=self.manager, container=self.diceOverlay
            )
            self.close_die_overlay_but = UIButton(
                relative_rect=close_rect,
                text="Chiudi",
                container=self.diceOverlay,
                object_id="CLOSE_DICE_OVERLAY",
                manager=self.manager,
            )
            self.close_die_overlay_but.disable()


        self.__actions_status.disable_actions()

        throw_rect = pygame.Rect(
            (20, DICE_OVERLAY_HEIGHT - ALERT_BUT_HEIGHT - 10),
            (ALERT_BUT_WIDTH, ALERT_BUT_HEIGHT),
        )
        self.launchOverlayDiceBut = UIButton(
            relative_rect=throw_rect,
            text="Lancia",
            container=self.diceOverlay,
            object_id="CLOSE_DICE_OVERLAY",
            manager=self.manager
        )

    def createDiceSurface(self):
        if self.twoDices:  # guardare se si può aggiornare solo la superficie con blit
            diceSurface = pygame.Surface((DICE_WIDTH * 2, DICE_HEIGHT))
            diceSurface.blit(self.image_dice_1, (0, 0))
            diceSurface.blit(self.image_dice_2, (0 + DICE_WIDTH, 0))
        else:
            diceSurface = pygame.Surface((DICE_WIDTH, DICE_HEIGHT))
            diceSurface.blit(self.image_dice_1, (0, 0))
        return diceSurface

    def draw_dices(self):
        surface = self.createDiceSurface()
        self.__gameUI.screen.blit(surface, (DICE_SURFACE_X, DICE_SURFACE_Y))

    def update_dice(self, score):  # score is a tuple from roll in gameLogic
        scoreToImage = [
            {"score": 1, "image": DICE_1},
            {"score": 2, "image": DICE_2},
            {"score": 3, "image": DICE_3},
            {"score": 4, "image": DICE_4},
            {"score": 5, "image": DICE_5},
            {"score": 6, "image": DICE_6},
        ]
        for scoreImage in scoreToImage:
            if scoreImage["score"] == score[0]:
                self.image_dice_1 = pygame.image.load(scoreImage["image"])
                self.image_dice_1 = pygame.transform.scale(
                    self.image_dice_1, (DICE_WIDTH, DICE_HEIGHT)
                )
            if scoreImage["score"] == score[1]:
                self.image_dice_2 = pygame.image.load(scoreImage["image"])
                self.image_dice_2 = pygame.transform.scale(
                    self.image_dice_2, (DICE_WIDTH, DICE_HEIGHT)
                )

        self.draw_dices()

    def updateDiceOverlay(self, score):
        self.__gameUI.update_dice(score)
        self.update_dice(score)
        self.diceOverlayImg.set_image(self.createDiceSurface())
        self.launchOverlayDiceBut.disable()
        if hasattr(self, "close_die_overlay_but"):
            self.close_die_overlay_but.enable()
        if hasattr(self, "closeDiceOverlayBut"):
            self.closeDiceOverlayBut.enable()

    def closeDiceOverlay(self, players, dice):
         # since screen.fill(BLACK) is already on updateStockboard and
        # dice.draw also we directly call that function
        self.diceOverlay.kill()
        self.__gameUI.updateStockboard(players, time.time(), dice)
        self.__actions_status.renable_actions()

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
            self.updateDiceOverlay(score)
            self.__game.set_square_balance(amount)
            self.__gameUI.update_dice(score)

    def establish_players_order(self): # pragma: no cover
        self.roll_dice()
        if self.__game.get_current_player_index() == len(self.__game.get_players()) - 1:
            self.last_player_logic()

    def restablish_player_order(self): # pragma: no cover
        self.roll_dice()
        if self.__copy_of_second_round_who_start == []:
            self.last_player_logic()

    def roll_dice(self):
        dice = self.__game.get_test_dice()
        score = roll(self.__test, dice)
        self.updateDiceOverlay(score)
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
            self.closeDiceOverlay(self.__game.get_players(), self.__gameUI)
            self.__game.set_current_player_index(self.__copy_of_second_round_who_start.pop(0)) 
            self.__gameUI.updateTurnLabel(self.__game.get_current_player())
            #self.__game.panels_to_show.append(DiceOverlay(self.__game, self.__game.get_current_player().get_name() + ' tira dadi', 'Decisione turni', self.__actions_status))
            self.message = self.__game.get_current_player().get_name() + ' tira dadi'
            self.draw()
        elif self.__establishing_players_order:
            self.closeDiceOverlay(self.__game.get_players(), self.__gameUI)
            self.__game.set_current_player_index((self.__game.get_current_player_index() + 1) % len(self.__game.get_players()))
            self.__gameUI.updateTurnLabel(self.__game.get_current_player())
            #self.__game.panels_to_show.append(DiceOverlay(self.__game, self.__game.get_current_player().get_name() + ' tira dadi', 'Decisione turni', self.__actions_status))
            self.message = self.__game.get_current_player().get_name() + ' tira dadi'
            self.draw()
        else:
            self.closeDiceOverlay(self.__game.get_players(), self.__gameUI)
        #self.__game.current_panel = None
    # getters created for test purposes
    def get_who_will_start(self): # pragma: no cover
        return self.__who_will_start
    
    def get_hihgest_score(self): # pragma: no cover
        return self.__highestScore
    
    def get_second_round_who_start(self): # pragma: no cover
        return self.__second_round_who_start.copy()
    
    def overlay_on(self):
        return self.__establishing_players_order or self.__establish_player_again