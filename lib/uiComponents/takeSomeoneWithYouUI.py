import pygame
from pygame_gui.elements import UIButton, UIPanel, UILabel, UIDropDownMenu
from lib.gameLogic import transfer_stock, check_if_can_buy_stock, sell_stock_to_bank, solve_bankrupt
from lib.constants import *
from lib.uiComponents.bargainUI import BargainUI

class TakeSomeoneWithYouUI:
    def __init__(self, game, other_players, position):
        self.game = game
        self.gameUI = game.get_gameUI()
        self.screen = self.gameUI.get_screen()
        self.manager = self.gameUI.get_manager()
        self.__other_players = other_players
        self.__selected_player = other_players[0]
        self.__position = position

    def draw(self):
        # Create a panel
        self.take_someone_ui = UIPanel(relative_rect=pygame.Rect(WIDTH // 2 - TAKE_SOMEONE_UI_WIDTH // 2, 20, TAKE_SOMEONE_UI_WIDTH, TAKE_SOMEONE_UI_HEIGHT), starting_height=2, manager=self.manager)

        title_rect = pygame.Rect((TAKE_SOMEONE_UI_WIDTH // 2 - TAKE_SOMEONE_UI_TITLE_WIDTH // 2, 10), (TAKE_SOMEONE_UI_TITLE_WIDTH, TAKE_SOMEONE_UI_TITLE_HEIGHT))
        self.bargain_title = UILabel(title_rect, "Chi vuoi portare con te?", manager=self.manager, container=self.take_someone_ui)

        player_names = list(map(lambda player: player.get_name(), self.__other_players))

        #Create a selector for the players
        self.player_selector = UIDropDownMenu(options_list=player_names,
                                                starting_option=player_names[0],
                                                relative_rect=pygame.Rect(TAKE_SOMEONE_UI_WIDTH // 2 - TAKE_SOMEONE_DROPDOWN_WIDTH // 2, TAKE_SOMEONE_UI_HEIGHT // 2 - TAKE_SOMEONE_DROPDOWN_HEIGHT // 2, TAKE_SOMEONE_DROPDOWN_WIDTH, TAKE_SOMEONE_DROPDOWN_HEIGHT),
                                                manager=self.manager,
                                                container=self.take_someone_ui)
        
        take_rect = pygame.Rect(TAKE_SOMEONE_UI_WIDTH // 2 - TAKE_SOMEONE_UI_BUT_WIDTH // 2, TAKE_SOMEONE_UI_HEIGHT - TAKE_SOMEONE_UI_BUT_HEIGHT - 50, TAKE_SOMEONE_UI_BUT_WIDTH, TAKE_SOMEONE_UI_BUT_HEIGHT)

        self.take_someone_butt = UIButton(relative_rect=take_rect,
                                text="Scegli",
                                container=self.take_someone_ui,
                                object_id = 'CHOOSE_WHO',
                                manager=self.manager)

    def close_take_someone_ui(self):
        self.take_someone_ui.kill()
        self.game.current_window = None
        self.screen.fill(BLACK)
        self.game.renable_actions()

    def manage_events(self, event):
        if hasattr(self, "player_selector") and event.ui_element == self.player_selector:
            self.__selected_player = self.get_player(event.text)
        if hasattr(self, "take_someone_butt") and event.ui_element == self.take_someone_butt: # pragma: no cover        
            self.__selected_player.set_position(self.__position)
            self.close_take_someone_ui()
            
    def get_player(self, player_name):

        for player in self.__other_players:
            if player.get_name() == player_name:
                return player