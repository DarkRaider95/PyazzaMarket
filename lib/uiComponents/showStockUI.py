import pygame
from pygame_gui.elements import UIButton, UIPanel, UILabel, UIImage
from lib.auction import Auction

from lib.gameLogic import transfer_stock
from ..constants import *

class ShowStockUI:
    def __init__(self, game, gameUI, screen, player = None):
        self.game = game
        self.gameUI = gameUI
        self.screen = screen
        self.manager = gameUI.manager        
        self.chooseMoveBut = None
        self.chooseBut = None
        self.buyAnyBut = None
        self.eventBut = None
        self.nextStock = None
        self.previousStock = None
        self.stockToAuction = None
        self.stocks = None
        self.player = player

    def show_stocks_ui(self, stocks, title):
        self.stocks = stocks
        self.showedStock = 0
        self.draw_stock_ui(title, True)

    def show_buy_anything_stock(self, stocks, title):
        self.stocks = stocks
        self.showedStock = 0
        self.draw_stock_ui(title, False)
        buyRect = pygame.Rect((STOCK_UI_WIDTH - STOCK_UI_BUT_WIDTH - 10, STOCK_UI_HEIGHT - STOCK_UI_BUT_HEIGHT - 10), (STOCK_UI_BUT_WIDTH, STOCK_UI_BUT_HEIGHT))

        self.buyAnyBut = UIButton(relative_rect=buyRect,
                                text="Compra quale vuoi",
                                container=self.stocksUi,
                                object_id = 'BUY_ANYTHING',
                                manager=self.manager)
        
    def show_choose_stock_to_auction(self):
        self.stocks = self.player.get_stocks()
        self.showedStock = 0
        self.draw_stock_ui("Cedole di" + self.get_name()+ "cosa vuoi mettere all'asta", False)
        stockRect = pygame.Rect((STOCK_UI_WIDTH - STOCK_UI_BUT_WIDTH - 10, STOCK_UI_HEIGHT - STOCK_UI_BUT_HEIGHT - 10), (STOCK_UI_BUT_WIDTH, STOCK_UI_BUT_HEIGHT))

        self.stockToAuction = UIButton(relative_rect=stockRect,
                                text="Metti all'asta",
                                container=self.stocksUi,
                                object_id = 'STOCK_TO_AUCTION',
                                manager=self.manager)
        
    def show_choose_stock(self, stocks, title):
        self.stocks = stocks
        self.showedStock = 0
        self.draw_stock_ui(title, True)
        chooseRect = pygame.Rect((STOCK_UI_WIDTH - STOCK_UI_BUT_WIDTH - 10, STOCK_UI_HEIGHT - STOCK_UI_BUT_HEIGHT - 10), (STOCK_UI_BUT_WIDTH, STOCK_UI_BUT_HEIGHT))

        self.chooseBut = UIButton(relative_rect=chooseRect,
                                text="Scegli",
                                container=self.stocksUi,
                                object_id = 'CHOOSE_STOCK',
                                manager=self.manager)
        
    def show_move_to_stock(self, stocks, title):
        self.stocks = stocks
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


    def manage_stock_events(self, event, players, currPlayer):
        
        if event.ui_element == self.nextStock: # pragma: no cover            
            self.show_next_stock()
        elif event.ui_element == self.previousStock: # pragma: no cover            
            self.show_previous_stock()
        elif event.ui_element == self.closeStock: # pragma: no cover                     
            self.close_stock_ui()
            self.screen.fill(BLACK)
            self.gameUI.draw_dices()
            self.gameUI.renableActions()
        elif event.ui_element == self.chooseBut: # pragma: no cover            
            chosen_stock = self.get_showed_stock()
            currPlayer.add_stock(chosen_stock)
            currPlayer.change_balance(-chosen_stock.get_stock_value())
            self.game.board.remove_stock(chosen_stock)
            self.close_stock_ui()
            self.screen.fill(BLACK)
            self.gameUI.draw_dices()
            self.gameUI.updateAllPlayerLables(players)
            self.gameUI.renableActions()
        elif event.ui_element == self.chooseMoveBut: # pragma: no cover            
            chosen_stock = self.get_showed_stock()
            curr_cell = self.game.board.get_cell(chosen_stock.get_position())
            currPlayer.set_position(chosen_stock.get_position())
            self.game.enableBuyButton(curr_cell, currPlayer)
            self.close_stock_ui()
            self.screen.fill(BLACK)
            self.gameUI.draw_dices()
            self.gameUI.renableActions()
        elif event.ui_element == self.buyAnyBut: # pragma: no cover
            chosen_stock = self.get_showed_stock()
            transfer_stock(self.game.board, currPlayer, chosen_stock)
            self.gameUI.updateAllPlayerLables(players)
            self.gameUI.renableActions()
        elif event.ui_element == self.stockToAuction:
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