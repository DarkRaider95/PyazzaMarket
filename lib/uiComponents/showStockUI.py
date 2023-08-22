import pygame
from pygame_gui.elements import UIButton, UIPanel, UILabel, UIImage
from lib.gameLogic import transfer_stock, check_if_can_buy_stock, sell_stock_to_bank, solve_bankrupt
from lib.constants import *

class ShowStockUI:
    def __init__(self, game, stocks, player = None):
        self.game = game
        self.gameUI = game.get_gameUI()
        self.screen = self.gameUI.get_screen()
        self.manager = self.gameUI.get_manager()
        self.player = player
        self.action_status = game.get_actions_status()
        self.stocks = stocks

    def show_stocks_ui(self, title):
        self.showedStock = 0
        self.draw_stock_ui(title, True)

    def show_buy_anything_stock(self, title):
        self.showedStock = 0
        self.draw_stock_ui(title, False)
        buyRect = pygame.Rect((STOCK_UI_WIDTH - STOCK_UI_BUT_WIDTH - 10, STOCK_UI_HEIGHT - STOCK_UI_BUT_HEIGHT - 10), (STOCK_UI_BUT_WIDTH, STOCK_UI_BUT_HEIGHT))

        self.buyAnyBut = UIButton(relative_rect=buyRect,
                                text="Compra quale vuoi",
                                container=self.stocksUi,
                                object_id = 'BUY_ANYTHING',
                                manager=self.manager)
        
    def show_choose_stock_to_auction(self):
        if self.player is not None:
            self.showedStock = 0
            self.draw_stock_ui("Cedole di" + self.player.get_name()+ "cosa vuoi mettere all'asta", False)
            stockRect = pygame.Rect((STOCK_UI_WIDTH - STOCK_UI_BUT_WIDTH - 10, STOCK_UI_HEIGHT - STOCK_UI_BUT_HEIGHT - 10), (STOCK_UI_BUT_WIDTH, STOCK_UI_BUT_HEIGHT))

            self.stockToAuction = UIButton(relative_rect=stockRect,
                                    text="Metti all'asta",
                                    container=self.stocksUi,
                                    object_id = 'STOCK_TO_AUCTION',
                                    manager=self.manager)
        
    def show_choose_stock(self, title):
        self.showedStock = 0
        self.draw_stock_ui(title, True)
        chooseRect = pygame.Rect((STOCK_UI_WIDTH - STOCK_UI_BUT_WIDTH - 10, STOCK_UI_HEIGHT - STOCK_UI_BUT_HEIGHT - 10), (STOCK_UI_BUT_WIDTH, STOCK_UI_BUT_HEIGHT))

        self.chooseBut = UIButton(relative_rect=chooseRect,
                                text="Scegli",
                                container=self.stocksUi,
                                object_id = 'CHOOSE_STOCK',
                                manager=self.manager)
        
    def show_buy_auctioned_stock(self):
        self.showedStock = 0
        self.draw_stock_ui("Sei l'unico partecipante all'asta vuoi comprare o lasciare alla banca?", True)
        buy_auct_rect = pygame.Rect((STOCK_UI_WIDTH - STOCK_UI_BUT_WIDTH - 200, STOCK_UI_HEIGHT - STOCK_UI_BUT_HEIGHT - 10), (STOCK_UI_BUT_WIDTH, STOCK_UI_BUT_HEIGHT))

        self.buy_auct_stock = UIButton(relative_rect=buy_auct_rect,
                                text="Compra",
                                container=self.stocksUi,
                                object_id = 'BUY_AUCT_STOCK',
                                manager=self.manager)
        
        if self.player.get_balance() < self.stocks[0].get_stock_value():
            self.buy_auct_stock.disable()
        
        leave_bank_rect = pygame.Rect((STOCK_UI_WIDTH - STOCK_UI_BUT_WIDTH - 10, STOCK_UI_HEIGHT - STOCK_UI_BUT_HEIGHT - 10), (STOCK_UI_BUT_WIDTH, STOCK_UI_BUT_HEIGHT))

        self.leave_to_bank_auct = UIButton(relative_rect=leave_bank_rect,
                                text="Lascia",
                                container=self.stocksUi,
                                object_id = 'LEAVE_AUCT_STOCK',
                                manager=self.manager)
        
    def show_bankrupt_stock(self):
        self.showedStock = 0
        self.draw_stock_ui("Sei in banca rotta a vendi o metti all'asta?", False)
        bankrupt_rect = pygame.Rect((STOCK_UI_WIDTH - STOCK_UI_BUT_WIDTH - 200, STOCK_UI_HEIGHT - STOCK_UI_BUT_HEIGHT - 10), (STOCK_UI_BUT_WIDTH, STOCK_UI_BUT_HEIGHT))

        self.auction_bankrupt = UIButton(relative_rect=bankrupt_rect,
                                text="Metti all'asta",
                                container=self.stocksUi,
                                object_id = 'BANKRUPT_AUCT',
                                manager=self.manager)
        
        leave_bank_rect = pygame.Rect((STOCK_UI_WIDTH - STOCK_UI_BUT_WIDTH - 10, STOCK_UI_HEIGHT - STOCK_UI_BUT_HEIGHT - 10), (STOCK_UI_BUT_WIDTH, STOCK_UI_BUT_HEIGHT))

        self.leave_to_bank_bankrupt = UIButton(relative_rect=leave_bank_rect,
                                text="Lascia alla banca",
                                container=self.stocksUi,
                                object_id = 'LEAVE_BANK_BANKRUPT',
                                manager=self.manager)
        
    def show_move_to_stock(self, title):
        self.showedStock = 0
        self.draw_stock_ui(title, False)
        chooseRect = pygame.Rect((STOCK_UI_WIDTH - STOCK_UI_BUT_WIDTH - 10, STOCK_UI_HEIGHT - STOCK_UI_BUT_HEIGHT - 10), (STOCK_UI_BUT_WIDTH, STOCK_UI_BUT_HEIGHT))

        self.chooseMoveBut = UIButton(relative_rect=chooseRect,
                                text="Scegli",
                                container=self.stocksUi,
                                object_id = 'CHOOSE_AND_MOVE',
                                manager=self.manager)

    def get_showed_stock(self):
        return self.stocks[self.showedStock]

    def draw_stock_ui(self, title, close):
        panel_rect = pygame.Rect((WIDTH // 2 - STOCK_UI_WIDTH // 2, 20), (STOCK_UI_WIDTH, STOCK_UI_HEIGHT))
        self.stocksUi = UIPanel(panel_rect, starting_height= 2, manager=self.manager)
        
        title_rect = pygame.Rect((STOCK_UI_WIDTH // 2 - STOCK_UI_TITLE_WIDTH // 2, 10), (STOCK_UI_TITLE_WIDTH, STOCK_UI_TITLE_HEIGHT))
        UILabel(title_rect, title, manager=self.manager, container=self.stocksUi)

        nextRect = pygame.Rect((STOCK_UI_WIDTH - 30 - STOCK_UI_BUT_WIDTH, STOCK_UI_HEIGHT // 2 - STOCK_UI_BUT_HEIGHT // 2), (STOCK_UI_BUT_WIDTH, STOCK_UI_BUT_HEIGHT))
        prevRect = pygame.Rect((30, STOCK_UI_HEIGHT // 2 - STOCK_UI_BUT_HEIGHT // 2), (STOCK_UI_BUT_WIDTH, STOCK_UI_BUT_HEIGHT))
        closeRect = pygame.Rect((STOCK_UI_WIDTH - STOCK_UI_BUT_WIDTH, 0), (STOCK_UI_BUT_WIDTH, STOCK_UI_BUT_HEIGHT))

        self.nextStock = UIButton(relative_rect=nextRect,
                                text=">",
                                container=self.stocksUi,
                                object_id = 'NEXT_STOCK',
                                manager=self.manager)
        
        self.previousStock = UIButton(relative_rect=prevRect,
                                text="<",
                                container=self.stocksUi,
                                object_id = 'PREV_STOCK',
                                manager=self.manager)
        if(close):
            self.closeStock = UIButton(relative_rect=closeRect,
                                    text="X",
                                    container=self.stocksUi,
                                    object_id = 'CLOSE_STOCK_UI',
                                    manager=self.manager)
        
        stockImageRect = pygame.Rect((STOCK_UI_WIDTH // 2 - STOCK_WIDTH // 2, 60), (STOCK_WIDTH, STOCK_HEIGHT))        
        
        currStock =self.stocks[self.showedStock]
        currStock.draw()
        self.stockImage = UIImage(stockImageRect, currStock.surface, container=self.stocksUi, manager=self.manager)
        
    def show_next_stock(self):
        self.showedStock = (self.showedStock + 1) % len(self.stocks)
        currStock =self.stocks[self.showedStock]
        currStock.draw()
        self.stockImage.set_image(currStock.surface)    
    
    def show_previous_stock(self):
        self.showedStock = (self.showedStock - 1) % len(self.stocks)
        currStock =self.stocks[self.showedStock]
        currStock.draw()
        self.stockImage.set_image(currStock.surface)
    
    def close_stock_ui(self):
        self.stocksUi.kill()
        self.game.showStockUI = None

    def manage_stock_events(self, event, players, curr_player):
        if hasattr(self, "nextStock") and event.ui_element == self.nextStock: # pragma: no cover            
            self.show_next_stock()
        elif hasattr(self, "previousStock") and event.ui_element == self.previousStock: # pragma: no cover            
            self.show_previous_stock()
        elif hasattr(self, "closeStock") and event.ui_element == self.closeStock: # pragma: no cover                     
            self.close_stock_ui()
            self.screen.fill(BLACK)
            self.gameUI.draw_dices()
        elif hasattr(self, "chooseBut") and event.ui_element == self.chooseBut: # pragma: no cover            
            chosen_stock = self.get_showed_stock()
            curr_player.add_stock(chosen_stock)
            curr_player.change_balance(-chosen_stock.get_stock_value())
            self.game.get_board().remove_stock(chosen_stock)
            self.close_stock_ui()
            self.screen.fill(BLACK)
            self.gameUI.draw_dices()
            self.gameUI.updateAllPlayerLables(players)
            self.action_status.renable_actions()
            self.action_status.set_show_stock(True)            
        elif hasattr(self, "chooseMoveBut") and event.ui_element == self.chooseMoveBut: # pragma: no cover
            chosen_stock = self.get_showed_stock()
            board = self.game.get_board()
            curr_cell = board.get_cell(chosen_stock.get_position())
            curr_player.set_position(chosen_stock.get_position())            
            self.close_stock_ui()
            self.screen.fill(BLACK)
            self.gameUI.draw_dices()
            self.action_status.renable_actions()
            if check_if_can_buy_stock(curr_cell, curr_player):
                self.action_status.set_buy_property(True)
        elif hasattr(self, "buyAnyBut") and event.ui_element == self.buyAnyBut: # pragma: no cover
            chosen_stock = self.get_showed_stock()
            board = self.game.get_board()
            transfer_stock(board, curr_player, chosen_stock)
            self.gameUI.updateAllPlayerLables(players)
            self.action_status.renable_actions()
        elif hasattr(self, "stockToAuction") and event.ui_element == self.stockToAuction:
            #if there are still some showStockToAuction I have to show another one and create the auction object
            if len(self.game.listShowStockToAuction) > 0:
                self.game.add_auction(self.player, self.get_showed_stock())                
                self.close_stock_ui()
                self.screen.fill(BLACK)
                showStock = self.game.listShowStockToAuction.pop(0)
                self.game.showStockUI = showStock
                showStock.show_choose_stock_to_auction()
            else: # I have to start the auctions if the showStockToAuction are finished
                self.game.add_auction(self.player, self.get_showed_stock())                
                self.close_stock_ui()
                self.screen.fill(BLACK)                
                self.game.showStockUI = None
                self.game.start_first_auction()
        #case only one bidder bought stock
        elif hasattr(self, "buy_auct_stock") and event.ui_element == self.buy_auct_stock:
            
            transfer_stock(self.game.get_board(), self.player, self.get_showed_stock(), True)
            self.gameUI.updateAllPlayerLables(players)
            self.close_stock_ui()
            self.screen.fill(BLACK)

            self.start_or_end_the_auctions()
        #case only one bidder left stock
        elif hasattr(self, "leave_to_bank_auct") and event.ui_element == self.leave_to_bank_auct:
            sell_stock_to_bank(self.game.get_board(), self.get_showed_stock())
            self.gameUI.updateAllPlayerLables(players)
            self.close_stock_ui()
            self.screen.fill(BLACK)

            self.start_or_end_the_auctions()
        #sell to bank in case of bankrupt
        elif hasattr(self, "leave_to_bank_bankrupt") and event.ui_element == self.leave_to_bank_bankrupt:
            sell_stock_to_bank(self.game.get_board(), self.get_showed_stock())
            self.gameUI.updateAllPlayerLables(players)
            self.close_stock_ui()
            self.screen.fill(BLACK)
            self.game.is_debt_solved(self.player)
            
        #start an auction in case of bankrupt
        elif hasattr(self, "auction_bankrupt") and event.ui_element == self.auction_bankrupt:            
            self.game.add_auction(self.player, self.get_showed_stock())                
            self.close_stock_ui()
            self.screen.fill(BLACK)                
            self.game.showStockUI = None
            self.game.start_first_auction()

    #logic to start or end the auctions
    def start_or_end_the_auctions(self):
        if len(self.game.listShowStockToAuction) > 0:#the auction is one started with the quotation logic
            showStock = self.game.listShowStockToAuction.pop(0)
            self.game.showStockUI = showStock
            showStock.show_buy_auctioned_stock()
        elif self.player.is_in_debt():#the auction is one started with a bankrupt
            self.game.is_debt_solved(self.player)
        else:
            self.action_status.renable_actions()
            self.game.showStockUI = None