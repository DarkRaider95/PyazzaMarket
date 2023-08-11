import pygame

from lib.auction import Auction
from lib.uiComponents.showStockUI import ShowStockUI
from lib.uiComponents.gameUI import GameUI
from lib.constants import (
    FPS,
    WIDTH,
    HEIGHT,
    CHOOSE_STOCK_TYPE,
    FREE_STOP_TYPE,
    CHANCE_TYPE,
    QUOTATION,
)
from lib.board import Board
from lib.player import Player
from lib.event import Event
from lib.gameLogic import *
import pygame_gui
from collections import deque
import time
import random
from lib.dice_overlay import DiceOverlay
from state_manager.actions_status import ActionsStatus
from ai.bot import Bot
from typing import Optional


class Game:
    def __init__(self, width, height, clock, players, test=False, gui=True):
        self.clock = clock
        self.width = width
        self.height = height
        self.running = True
        self.__actions_status = ActionsStatus()
        self.__players = []
        # creating events
        events = Event.initialize_events()
        self.events = deque(events)
        random.shuffle(self.events)
        self.__squareBalance = 2000
        random.shuffle(QUOTATION)  # this function do an inplace shuffle to QUOTATION
        self.new_quotation = deque(
            QUOTATION
        )  # this function create a ring list that work using rotate()
        self.__test = test  # used to input the dice value in the test
        self.__test_dice = (0, 0)  # used when the game is running in test mode
        self.__auctions = []
        self.currentAuction: Optional[Auction] = None
        self.listShowStockToAuction = []
        self.__gui = gui
        self.__current_player_index = 0
        self.__square_balance = SQUARE_BALANCE

        if gui:
            # when we run the ai we don't need to initialize the gui
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("PyazzaMarket")
            self.board = Board()
            self.__gameUI = GameUI(self.screen, self.clock, self.__actions_status)
            self.dice_overlay = DiceOverlay(self)
        self.__bot = Bot(self)

        Player.last_stock_update = time.time()
        for player in players:
            self.__players.append(
                Player(player["name"], player["color"], player["bot"])
            )

    def start(self):  # pragma: no cover
        self.board.draw(self.screen)
        self.__gameUI.draw_dices()
        self.__gameUI.draw_actions_ui()
        self.__gameUI.draw_leaderboard(
            self.get_players(),
            self.__square_balance,
            self.__players[self.__current_player_index],
        )
        self.__gameUI.draw_stockboard(self.get_players())

        self.__gameUI.drawDiceOverlay(
            self.__players[self.__current_player_index].get_name() + " tira dadi",
            "Decisione turni",
        )
        # we will handle the next players in the while loop

        for index, player in enumerate(self.get_players()):
            self.board.draw_player_car(self.screen, player, index, len(self.__players))

        while self.running:
            self.clock.tick(FPS)

            if self.__players[self.__current_player_index].get_is_bot():
                self.__bot.play()

            for event in pygame.event.get():
                self.manage_events(event)
                self.__gameUI.manager.process_events(event)

            # Now we update at all turn the stockboard for avoiding
            self.__gameUI.updateStockboard(
                self.get_players(), Player.last_stock_update, self.__gameUI
            )
            self.board.draw(self.screen)
            self.__gameUI.renable_actions()
            for i, player in enumerate(self.get_players()):
                self.board.draw_player_car(
                    self.screen, player, i, len(self.get_players())
                )

            time_delta = self.clock.tick(FPS) / 1000.0
            self.__gameUI.manager.update(time_delta)
            self.__gameUI.manager.draw_ui(self.screen)
            pygame.display.update()

    def set_skip_turn(self):  # pragma: no cover
        curr_player = self.__players[self.__current_player_index]
        while curr_player.get_skip_turn():
            curr_player.set_skip_turn(False)
            self.__current_player_index = (self.__current_player_index + 1) % len(
                self.get_players()
            )
            curr_player = self.__players[self.__current_player_index]

    def turn(self):
        tiro_doppio = False
        self.__actions_status.set_throw_dices(False)
        self.__actions_status.set_pass_turn(True)
        score = roll(self.__test, self.__test_dice)
        self.__gameUI.update_dice(score)
        # is double
        if is_double(score):
            self.__actions_status.set_pass_turn(False)
            self.__actions_status.set_throw_dices(True)
            tiro_doppio = True

        curr_player = self.__players[self.__current_player_index]
        curr_player.move(score[0] + score[1])
        cell = self.board.get_cells()[curr_player.get_position()]
        # check turn and crash before any other events or effect of the cells
        check_turn(curr_player)
        crash = check_crash(self.get_players(), self.__current_player_index)
        if tiro_doppio and crash:
            self.__gameUI.drawAlert("Doppio e incidente!")
        elif tiro_doppio:
            self.__gameUI.drawAlert("Tiro doppio!")
        elif crash:
            self.__gameUI.drawAlert("Incidente!")
        # case cell with stock
        if cell.cellType == STOCKS_TYPE:
            # curr_player.move(10)
            self.enable_buy_button(cell, curr_player)
            # we need to create a copy of the list in order to perform some edit of the list later
            check_for_penalty(
                self.board.get_cells(), self.get_players(), self.__current_player_index
            )
        # case special cell
        else:
            self.special_cell_logic(cell, curr_player)

        self.__gameUI.updateAllPlayerLables(self.get_players())

    def manage_events(self, event):
        curr_player = self.__players[self.__current_player_index]

        if event.type == pygame.QUIT:
            self.running = False

        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if (
                hasattr(self.__gameUI, "launchDice")
                and event.ui_element == self.__gameUI.launchDice
            ):
                self.turn()
            elif (
                hasattr(self.__gameUI, "buyButton")
                and event.ui_element == self.__gameUI.buyButton
            ):
                buy_stock(self.board.get_cells(), curr_player)
                self.__gameUI.updateAllPlayerLables(self.get_players())
                self.__actions_status.set_buy_property(False)
                self.__actions_status.enable_show_stock(curr_player)
            elif (
                hasattr(self.__gameUI, "passButton")
                and event.ui_element == self.__gameUI.passButton
            ):
                self.__current_player_index = (self.__current_player_index + 1) % len(
                    self.get_players()
                )
                self.set_skip_turn()
                self.__gameUI.updateTurnLabel(curr_player)
                self.__actions_status.set_throw_dices(True)
                self.__actions_status.set_pass_turn(False)
                self.__actions_status.set_buy_property(False)
                self.__actions_status.enable_show_stock(curr_player)
            elif (
                hasattr(self.__gameUI, "showStocks")
                and event.ui_element == self.__gameUI.showStocks
            ):
                self.disable_actions()
                self.showStockUI = ShowStockUI(self)
                self.showStockUI.show_stocks_ui(
                    curr_player.get_stocks(), "Le cedole di " + curr_player.get_name()
                )
            elif (
                hasattr(self, "showStockUI")
                and hasattr(self.__gameUI, "eventBut")
                and event.ui_element == self.__gameUI.eventBut
            ):
                self.__gameUI.updateTurnLabel(
                    self.__players[self.__current_player_index]
                )
                self.__actions_status.set_throw_dices(True)
                self.__actions_status.set_pass_turn(False)
                self.__actions_status.set_buy_property(False)
                self.__actions_status.enable_show_stock(curr_player)
            elif (
                hasattr(self, "showStockUI")
                and hasattr(self.showStockUI, "nextStock")
                and event.ui_element == self.showStockUI.nextStock
            ):
                self.showStockUI.show_next_stock()
            elif (
                hasattr(self, "showStockUI")
                and hasattr(self.showStockUI, "previousStock")
                and event.ui_element == self.showStockUI.previousStock
            ):
                self.showStockUI.show_previous_stock()
            elif (
                hasattr(self, "showStockUI")
                and hasattr(self.showStockUI, "closeStock")
                and event.ui_element == self.showStockUI.closeStock
            ):
                self.showStockUI.close_stock_ui()
                self.screen.fill(BLACK)
                self.__gameUI.draw_dices()
                self.renable_actions()
            elif (
                hasattr(self, "showStockUI")
                and hasattr(self.showStockUI, "chooseBut")
                and event.ui_element == self.showStockUI.chooseBut
            ):
                chosen_stock = self.showStockUI.get_showed_stock()
                curr_player.add_stock(chosen_stock)
                curr_player.change_balance(-chosen_stock.get_stock_value())
                self.board.remove_stock(chosen_stock)
                self.showStockUI.close_stock_ui()
                self.screen.fill(BLACK)
                self.__gameUI.draw_dices()
                self.__gameUI.updateAllPlayerLables(self.get_players())
                self.renable_actions()
            elif (
                hasattr(self, "showStockUI")
                and hasattr(self.showStockUI, "chooseMoveBut")
                and event.ui_element == self.showStockUI.chooseMoveBut
            ):
                chosen_stock = self.showStockUI.get_showed_stock()
                curr_cell = self.board.get_cell(chosen_stock.get_position())
                curr_player.set_position(chosen_stock.get_position())
                self.enable_buy_button(curr_cell, curr_player)
                self.showStockUI.close_stock_ui()
                self.screen.fill(BLACK)
                self.__gameUI.draw_dices()
                self.renable_actions()
            elif (
                hasattr(self.__gameUI, "eventBut")
                and event.ui_element == self.__gameUI.eventBut
            ):
                self.events_logic(curr_player)
                self.__gameUI.closeEventUi()
                self.screen.fill(BLACK)
                self.__gameUI.draw_dices()
                self.__gameUI.updateAllPlayerLables(self.get_players())
                self.renable_actions()
            elif (
                hasattr(self, "showStockUI")
                and hasattr(self.showStockUI, "buyAnyBut")
                and event.ui_element == self.showStockUI.buyAnyBut
            ):
                chosen_stock = self.showStockUI.get_showed_stock()
                curr_player = self.__players[self.__current_player_index]
                transfer_stock(self.board, curr_player, chosen_stock)
                self.__gameUI.updateAllPlayerLables(self.get_players())
                self.renable_actions()
            elif (
                hasattr(self.__gameUI, "closeAlertBut")
                and event.ui_element == self.__gameUI.closeAlertBut
            ):
                self.__gameUI.closeAlert(self.get_players(), self.__gameUI)
            elif (
                hasattr(self.__gameUI, "closeDiceOverlayBut")
                and event.ui_element == self.__gameUI.closeDiceOverlayBut
            ):
                self.dice_overlay.close_dice_overlay()
                if not self.dice_overlay.overlay_on():
                    self.__current_player_index = self.dice_overlay.get_who_will_start()
                    self.__gameUI.updateTurnLabel(
                        self.__players[self.__current_player_index]
                    )
                    self.__actions_status.set_throw_dices(True)
            elif (
                hasattr(self.__gameUI, "launchOverlayDiceBut")
                and event.ui_element == self.__gameUI.launchOverlayDiceBut
            ):
                self.dice_overlay.launch_but_pressed()
            # elif self.currentAuction is not None:
            # self.manage_auction_events(event)
            elif self.showStockUI is not None:
                self.showStockUI.manage_stock_events(
                    event, self.get_players(), curr_player
                )
            else:  # pragma: no cover
                print("Evento non gestito")
        elif event.type == pygame.KEYDOWN and self.__test:
            if event.key == pygame.K_0:  # or pygame.K_KP0:
                self.set_test_dice(0)
                print("Test dice set to 0")
            elif event.key == pygame.K_1:  # or pygame.K_KP1:
                self.set_test_dice(1)
            elif event.key == pygame.K_2:  # or pygame.K_KP2:
                self.set_test_dice(2)
            elif event.key == pygame.K_3:  # or pygame.K_KP3:
                self.set_test_dice(3)
            elif event.key == pygame.K_4:  # or pygame.K_KP4:
                self.set_test_dice(4)
            elif event.key == pygame.K_5:  # or pygame.K_KP5:
                self.set_test_dice(5)
            elif event.key == pygame.K_6:  # or pygame.K_KP6:
                self.set_test_dice(6)
            elif event.key == pygame.K_7:  # or pygame.K_KP7:
                self.set_test_dice(7)
            elif event.key == pygame.K_8:  # or pygame.K_KP8:
                self.set_test_dice(8)
            elif event.key == pygame.K_9:  # or pygame.K_KP9:
                self.set_test_dice(9)
            elif event.key == pygame.K_SPACE:
                self.__test_dice = (0, 0)
                self.__gameUI.update_dice((1, 1))
            elif event.key == pygame.K_RETURN:
                if self.__test_dice != (0, 0):
                    if self.dice_overlay.overlay_on():
                        self.dice_overlay.launch_but_pressed()
                    else:
                        self.turn()
                    self.__test_dice = (0, 0)
                    self.__gameUI.update_dice((1, 1))

    def start_first_auction(self):
        self.currentAuction = self.__auctions.pop(0)
        self.currentAuction.start_auction()

    def manage_auction_events(self, event):
        if (
            hasattr(self.currentAuction, "raiseBid")
            and event.ui_element == self.currentAuction.raiseBid
        ):
            self.currentAuction.raise_bid()
        elif (
            hasattr(self.currentAuction, "lowerBid")
            and event.ui_element == self.currentAuction.lowerBid
        ):
            self.currentAuction.lower_bid()
        elif (
            hasattr(self.currentAuction, "bidBut")
            and event.ui_element == self.currentAuction.bidBut
        ):
            self.currentAuction.bid_but()
        elif (
            hasattr(self.currentAuction, "newtBidder")
            and event.ui_element == self.currentAuction.nextBidder
        ):
            self.currentAuction.pass_bid()
        elif (
            hasattr(self.currentAuction, "retireAuction")
            and event.ui_element == self.currentAuction.retireAuction
        ):
            self.currentAuction.retire_auction()
            if self.currentAuction.is_finished():
                # if there are other auctions open next otherwise close it
                if len(self.__auctions) > 0:
                    self.currentAuction.auctionUI.kill()
                    self.screen.fill(BLACK)
                    self.currentAuction = self.__auctions.pop(0)
                    self.currentAuction.start_auction()
                else:
                    self.currentAuction.auctionUI.kill()
                    self.currentAuction = None
                    self.screen.fill(BLACK)
                    self.__gameUI.updateAllPlayerLables(self.get_players())
                    self.renable_actions()

    def set_test_dice(self, value):
        if self.__test_dice[0] == 0:
            self.__test_dice = (value, 0)
        elif self.__test_dice[1] == 0:
            self.__test_dice = (self.__test_dice[0], value)
            self.__gameUI.update_dice(self.__test_dice)

    def enable_buy_button(self, cell, player):  # pragma: no cover
        if check_if_can_buy_stock(cell, player):
            self.__actions_status.set_buy_property(True)
        else:
            self.__actions_status.set_buy_property(False)

    def special_cell_logic(self, cell, player):  # pragma: no cover
        if cell.cellType == START_TYPE:
            start_logic(player)
        elif cell.cellType == EVENTS_TYPE:
            self.disable_actions()
            self.__gameUI.showEventUi(self.events[0])
        elif cell.cellType == STOCKS_PRIZE_TYPE:
            stock_prize_logic(player)
        elif cell.cellType == QUOTATION_TYPE:
            quotation_logic(self.get_players(), self.board, self.new_quotation, self)

            # create one showStockToAuction for every player that has a stock
            for player in self.get_players():
                # if they have stock I have to create panel to show stock
                if len(player.get_stocks()) > 0:
                    self.listShowStockToAuction.append(ShowStockUI(self, player))

            showStock = self.listShowStockToAuction.pop(0)
            self.showStockUI = showStock
            showStock.show_choose_stock_to_auction()
        elif cell.cellType == CHOOSE_STOCK_TYPE:
            stocks = self.board.get_availble_stocks()
            self.disable_actions()
            self.showStockUI = ShowStockUI(self)
            self.showStockUI.show_move_to_stock(
                stocks, "Scegli su quale cedola vuoi spostarti"
            )
        elif cell.cellType == FREE_STOP_TYPE:
            stocks = self.board.get_purchasable_stocks(player.get_balance())
            self.disable_actions()
            self.showStockUI = ShowStockUI(self)
            self.showStockUI.show_choose_stock(stocks, "Scegli quale vuoi comprare")
        elif cell.cellType == SIX_HUNDRED_TYPE:
            six_hundred_logic(player)
        elif cell.cellType == CHANCE_TYPE:
            self.__gameUI.drawDiceOverlay(
                self.__players[self.__current_player_index].get_name() + " tira dadi",
                "Riserva monetaria",
                False,
            )

    def events_logic(self, player):
        event = self.events[0]

        if event.evenType == COLOR_EVENT:
            pass
        elif event.evenType == BUY_ANTHING_EVENT:
            stocks = self.board.get_availble_stocks()
            for p in self.__players:
                if p != player:
                    stocks.extend(player.get_stocks())
            self.disable_actions()
            self.showStockUI = ShowStockUI(self)
            self.showStockUI.show_buy_anything_stock(
                stocks, "Scegli quale vuoi comprare (Nessuno può opporsi alla vendita)"
            )
        elif event.evenType == STOP_1:
            player.set_skip_turn(True)
        elif event.evenType == FREE_PENALTY:
            player.freePenalty(True)
        elif event.evenType == FREE_PENALTY_MARTINI:
            player.set_free_martini(True)
        elif event.evenType == EVERYONE_FIFTY_EVENT:
            every_one_fifty(self.get_players())
        elif event.evenType == PREVIOUS_PLAYER_GALUP:
            previousPlayerIndex = (self.__current_player_index - 1) % len(
                self.__players
            )
            previousPlayer = self.__players[previousPlayerIndex]
            previousPlayer.set_position(39)
            playerOwnStock = who_owns_stock(self.get_players(), 39)[
                0
            ]  # bisogna ragionare come gestire questo caso se ci sono più giocatori quale penalità prendo quella più alta o quella più bassa?
            stock = playerOwnStock.get_stock_by_pos(39)
            amount = playerOwnStock.compute_penalty(stock)
            previousPlayer.change_balance(amount)
        elif event.evenType == NEXT_PLAYER_PAY:
            nextPlayerIndex = (self.__current_player_index + 1) % len(self.__players)
            nextPlayer = self.__players[nextPlayerIndex]
            nextPlayer.change_balance(-200)
        elif event.evenType == GIFT_EVENT:
            effectData = event.effectData
            stock = self.board.get_stock_if_available(effectData["stockIndex"])
            if stock is not None:
                player.add_stock(stock)
            else:
                player.change_balance(effectData["amount"])
        elif event.evenType == GET_EVENT:
            effectData = event.effectData

            if "from" in effectData.keys():
                fromWho = effectData["from"]
                if fromWho == "others":
                    get_money_from_others(
                        self.get_players(),
                        self.__current_player_index,
                        effectData["amount"],
                    )
            else:
                player.change_balance(effectData["amount"])
        elif event.evenType == GO_EVENT:
            self.go_event_logic(player, event)
        elif event.evenType == PAY_EVENT:
            effectData = event.effectData

            if "to" in effectData.keys():
                toWho = effectData["to"]
                if toWho == "others":
                    pay_money_to_others(
                        self.get_players(),
                        self.__current_player_index,
                        effectData["amount"],
                    )
            else:
                player.change_balance(-effectData["amount"])
        elif event.evenType == OWN_EVENT:
            effectData = event.effectData

            owners = who_owns_stock_by_name(self.get_players(), effectData["stockName"])

            if len(owners) > 0:
                for owner in owners:
                    update_owner_balance(
                        owner,
                        effectData["stockName"],
                        effectData["getAmount"],
                        effectData["each"],
                    )

            if effectData["othersPayValue"] is not None:
                update_others_balance(
                    self.__players, owners, effectData["othersPayValue"]
                )

        elif event.evenType == BUY_EVENT:
            stock = self.board.get_stock_if_available(effectData["stockIndex"])
            if stock is not None:
                player.add_stock(stock)
                player.change_balance(-stock.get_original_value())
            else:
                print("BUY CASE START NEGOTIATION")
                pass  # avviare trattativa con proprietario

        # rotate the events list
        self.events.rotate(-1)

    def go_event_logic(self, player, event):
        effectData = event.effectData

        if effectData["startCheck"]:
            passStart = check_start_pass(player, effectData["destination"])
            if passStart:
                player.change_balance(300)

        if effectData["pass"] is not None:
            passAmount = compute_pass_amount(
                self.__players,
                self.__current_player_index,
                effectData["pass"],
                effectData["destination"],
            )
            player.change_balance(passAmount)

        if effectData["someone"]:  # implement interface to choose someone
            print("GOTO SOMEONE CASE")
            pass

        if effectData["buy"]:
            stock = self.board.get_stock_if_available(effectData["destination"])
            if stock is not None:
                player.add_stock(stock)
                player.change_balance(-stock.get_original_value())
            else:
                print("GOTO BUY CASE START NEGOTIATION")
                pass  # implement gui to start negotiation with owner

        if effectData["get"] is not None:
            player.change_balance(effectData["get"])

        player.set_position(effectData["destination"])

    def add_auction(self, player, stock):
        players = filter(
            lambda obj: obj.get_name() == player.get_name(), self.get_players()
        )
        self.__auctions.append(
            Auction(self.__gameUI.manager, self.screen, player, players, stock)
        )

    def disable_actions(self):  # pragma: no cover
        """This function disable the action in the status manager and in the ui"""
        self.__actions_status.disable_actions()
        if self.__gui:
            self.__gameUI.disableActions()

    def renable_actions(self):  # pragma: no cover
        """This function reenable the action in the status manager and in the ui"""
        if self.__gui:
            self.__gameUI.renable_actions()
        self.__actions_status.renable_actions()

    def set_square_balance(self, new_balance):  # pragma: no cover
        self.__square_balance += new_balance
        if self.__square_balance < 0:
            self.__square_balance = 0
        self.__gameUI.updateSquareBalanceLabel(self.__square_balance)

    def get_players(self):  # pragma: no cover
        return self.__players.copy()

    def get_square_balance(self):  # pragma: no cover
        return self.__square_balance

    def get_current_player(self):  # pragma: no cover
        return self.__players[self.__current_player_index]

    def get_current_player_index(self):  # pragma: no cover
        return self.__current_player_index

    def set_current_player_index(self, index):  # pragma: no cover
        self.__current_player_index = index

    def get_gameUI(self):  # pragma: no cover
        return self.__gameUI

    def get_test(self):  # pragma: no cover
        return self.__test

    def get_test_dice(self):  # pragma: no cover
        return self.__test_dice

    def get_actions_status(self):  # pragma: no cover
        return self.__actions_status
