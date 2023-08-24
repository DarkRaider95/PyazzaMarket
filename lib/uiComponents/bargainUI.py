import pygame
from pygame_gui.elements.ui_selection_list import UISelectionList
from pygame_gui.elements import UIButton, UIPanel, UILabel, UIDropDownMenu
from lib.constants import *

class BargainUI:

    def __init__(self, manager, screen, player, other_players, game):        
        self.manager = manager
        self.screen = screen
        self.__player = player
        self.__other_players = other_players
        self.game = game

    def draw(self):
        # Create a panel
        self.bargain_ui = UIPanel(relative_rect=pygame.Rect(WIDTH // 2 - BARGAIN_UI_WIDTH // 2, 20, BARGAIN_UI_WIDTH, BARGAIN_UI_HEIGHT), manager=self.manager)

        title_rect = pygame.Rect((BARGAIN_UI_WIDTH // 2 - BARGAIN_UI_TITLE_WIDTH // 2, 10), (BARGAIN_UI_TITLE_WIDTH, BARGAIN_UI_TITLE_HEIGHT))
        self.bargain_title = UILabel(title_rect, "Contratta", manager=self.manager, container=self.bargain_ui)

        stock_player_1_rect = pygame.Rect(50, 50, BARGAIN_UI_TITLE_WIDTH, BARGAIN_UI_TITLE_HEIGHT)
        self.bargain_title = UILabel(stock_player_1_rect, "Le cedole di "+self.__player.get_name()+":", manager=self.manager, container=self.bargain_ui)

        #Create multiple selection list for player stocks
        self.stocks_player_1 = UISelectionList(relative_rect=pygame.Rect(50, 100, BARGAIN_SELECTION_LIST_WIDTH, BARGAIN_SELECTION_LIST_HEIGHT), item_list = self.__player.get_stocks_names(),
                                        manager=self.manager, container=self.bargain_ui, allow_multi_select= True)
        player_names = list(map(lambda player: player.get_name(), self.__other_players))

        #Create a selector for the players
        self.player_selector = UIDropDownMenu(options_list=player_names,
                                                starting_option=player_names[0],
                                                relative_rect=pygame.Rect(400, 50, BARGAIN_DROPDOWN_WIDTH, BARGAIN_DROPDOWN_HEIGHT),
                                                manager=self.manager,
                                                container=self.bargain_ui)

        #Create multiple selection list for player stocks
        self.stocks_player_2 = UISelectionList(relative_rect=pygame.Rect(400, 100, BARGAIN_SELECTION_LIST_WIDTH, BARGAIN_SELECTION_LIST_HEIGHT), item_list=self.__other_players[0].get_stocks_names(),
                                        manager=self.manager, container=self.bargain_ui, allow_multi_select= True)

        
        bargain_rect = pygame.Rect(BARGAIN_UI_WIDTH - BARGAIN_UI_BUT_WIDTH * 2 - 30, BARGAIN_UI_HEIGHT - 100, BARGAIN_UI_BUT_WIDTH, BARGAIN_UI_BUT_HEIGHT)
        close_rect = pygame.Rect(BARGAIN_UI_WIDTH - BARGAIN_UI_BUT_WIDTH, BARGAIN_UI_HEIGHT - 100, BARGAIN_UI_BUT_WIDTH, BARGAIN_UI_BUT_HEIGHT)
        

        self.bargain_butt = UIButton(relative_rect=bargain_rect,
                                text="Contratta",
                                container=self.bargain_ui,
                                object_id = 'BARGAIN',
                                manager=self.manager)
        
        self.close_butt = UIButton(relative_rect=close_rect,
                                text="Chiudi",
                                container=self.bargain_ui,
                                object_id = 'CLOSE_BARGAIN',
                                manager=self.manager)
        
    def close_bargain_ui(self):
        self.bargain_ui.kill()
        self.game.bargain_ui = None

    def manage_bargain_events(self, event):
        if hasattr(self, "player_selector") and event.ui_element == self.player_selector:
            player = self.get_player(event.text)
            self.stocks_player_2.set_item_list(player.get_stocks_names())                
        elif hasattr(self, "bargain_butt") and event.ui_element == self.bargain_butt: # pragma: no cover
            pass
            #open confirmation bargain ui and pass the bargains
            #self.close_bargain_ui()
            #self.screen.fill(BLACK)
        elif hasattr(self, "close_butt") and event.ui_element == self.close_butt: # pragma: no cover            
            self.close_bargain_ui()
            self.screen.fill(BLACK)
            self.game.renable_actions()

    def get_player(self, player_name):

        for player in self.__other_players:
            if player.get_name() == player_name:
                return player