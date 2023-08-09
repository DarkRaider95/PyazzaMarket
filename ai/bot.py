import pygame_gui

class FakeEvent:
    def __init__(self, event_type, ui_element):
        self.type = event_type
        self.ui_element = ui_element

class Bot:
    def __init__(self, game) -> None:
        self.__game = game
        self.__actions_status = game.get_actions_status()
        self.__gameUI = game.get_gameUI()

    def play(self) -> None:
        if self.__actions_status.get_throw_dices():
            self.__game.manage_events(FakeEvent(pygame_gui.UI_BUTTON_PRESSED, self.__gameUI.launchDice))

""" 
    def manage_events(self, event):
        if event.type == pygame.QUIT:
            self.running = False

        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.gameUI.launchDice:
                self.turn()
            elif event.ui_element == self.gameUI.buyButton:
                curr_player = self.__players[self.__current_player_index]
                buy_stock(self.board.get_cells(), curr_player)
                self.gameUI.updateAllPlayerLables(self.get_players())
                self.__actions_status.set_buy_property(False)
                self.gameUI.enableShowStockButton(self.__players[self.__current_player_index])
            elif event.ui_element == self.gameUI.passButton:
                self.__current_player_index = (self.__current_player_index + 1) % len(self.get_players())
                self.set_skip_turn()
                self.gameUI.updateTurnLabel(self.__players[self.__current_player_index])
                self.__actions_status.set_throw_dices(True)
                self.__actions_status.set_pass_turn(False)
                self.__actions_status.set_buy_property(False)
                self.gameUI.enableShowStockButton(self.__players[self.__current_player_index])
            elif event.ui_element == self.gameUI.showStocks:  # pragma: no cover
                curr_player = self.__players[self.__current_player_index]
                self.disable_actions()
                self.gameUI.showStocksUi(curr_player.get_stocks(), "Le cedole di " + curr_player.get_name())
            elif event.ui_element == self.gameUI.nextStock:  # pragma: no cover
                curr_player = self.__players[self.__current_player_index]
                self.gameUI.showNextStock()
            elif event.ui_element == self.gameUI.previousStock:  # pragma: no cover
                curr_player = self.__players[self.__current_player_index]
                self.gameUI.showPreviousStock()
            elif event.ui_element == self.gameUI.closeStock:  # pragma: no cover
                self.gameUI.closeStockUi()
                self.screen.fill(BLACK)
                self.gameUI.draw_dices()
                self.renable_actions()
            elif event.ui_element == self.gameUI.chooseBut:  # pragma: no cover
                curr_player = self.__players[self.__current_player_index]
                chosen_stock = self.gameUI.getShowedStock()
                curr_player.add_stock(chosen_stock)
                curr_player.change_balance(-chosen_stock.get_stock_value())
                self.board.remove_stock(chosen_stock)
                self.gameUI.closeStockUi()
                self.screen.fill(BLACK)
                self.gameUI.draw_dices()
                self.gameUI.updateAllPlayerLables(self.get_players())
                self.renable_actions()
            elif event.ui_element == self.gameUI.chooseMoveBut:  # pragma: no cover
                curr_player = self.__players[self.__current_player_index]
                chosen_stock = self.gameUI.getShowedStock()
                curr_cell = self.board.get_cell(chosen_stock.get_position())
                curr_player.set_position(chosen_stock.get_position())
                self.enableBuyButton(curr_cell, curr_player)
                self.gameUI.closeStockUi()
                self.screen.fill(BLACK)
                self.gameUI.draw_dices()
                # self.__actions_status.set_pass_turn(True)
                # self.gameUI.showStocks.enable()
                self.renable_actions()
            elif event.ui_element == self.gameUI.eventBut:  # pragma: no cover
                curr_player = self.__players[self.__current_player_index]
                self.events_logic(curr_player)
                self.gameUI.closeEventUi()
                self.screen.fill(BLACK)
                self.gameUI.draw_dices()
                self.gameUI.updateAllPlayerLables(self.get_players())
                self.renable_actions()
            elif event.ui_element == self.gameUI.buyAnyBut:  # pragma: no cover
                chosen_stock = self.gameUI.getShowedStock()
                curr_player = self.__players[self.__current_player_index]
                transfer_stock(self.board, curr_player, chosen_stock)
                self.gameUI.updateAllPlayerLables(self.get_players())
                self.renable_actions()
            elif event.ui_element == self.gameUI.closeAlertBut:  # pragma: no cover
                self.gameUI.closeAlert(self.get_players(), self.gameUI)
            elif event.ui_element == self.gameUI.closeDiceOverlayBut:  # pragma: no cover
                self.dice_overlay.close_dice_overlay()
                if not self.dice_overlay.overlay_on():
                    self.__current_player_index = self.dice_overlay.get_who_will_start()
                    self.gameUI.updateTurnLabel(self.__players[self.__current_player_index])
                    self.__actions_status.set_throw_dices(True)
            elif event.ui_element == self.gameUI.launchOverlayDiceBut:  # pragma: no cover
                self.dice_overlay.launch_but_pressed()
            elif self.auction is not None:
                self.manage_auction_events(event)
            else:  # pragma: no cover
                print("Evento non gestito")
 """