import pygame
from pygame_gui.elements.ui_selection_list import UISelectionList
from pygame_gui.elements import (
    UIButton,
    UIPanel,
    UILabel,
    UIDropDownMenu,
    UITextEntryLine,
)
from lib.constants import *
import re
from lib.player import Player

from lib.gameLogic import transfer_stock


class BargainUI:
    def __init__(
        self, manager, screen, current_player: Player, other_players: list[Player], game
    ):
        self.manager = manager
        self.screen = screen
        self.__player = current_player
        self.__other_players = other_players
        self.game = game
        self.showed_player: Player = other_players[0]
        self.stocks_given = []
        self.stocks_got = []
        # initialize the list with the amount of money given or received for each player
        self.exchange_values = [0] * len(other_players)
        # since the exchange_values is a list of positive int, we need to keep track of who will receive and who will give
        self.exchange_direction = ["Dai"] * len(other_players)
        self.showed_player_index = 0

    def draw(self):
        # Create a panel
        self.bargain_ui = UIPanel(
            relative_rect=pygame.Rect(
                WIDTH // 2 - BARGAIN_UI_WIDTH // 2,
                20,
                BARGAIN_UI_WIDTH,
                BARGAIN_UI_HEIGHT,
            ),
            starting_height=2,
            manager=self.manager,
        )

        title_rect = pygame.Rect(
            (BARGAIN_UI_WIDTH // 2 - BARGAIN_UI_TITLE_WIDTH // 2, 10),
            (BARGAIN_UI_TITLE_WIDTH, BARGAIN_UI_TITLE_HEIGHT),
        )
        self.bargain_title = UILabel(
            title_rect, "Contratta", manager=self.manager, container=self.bargain_ui
        )

        stock_player_1_rect = pygame.Rect(
            50, 50, BARGAIN_UI_TITLE_WIDTH, BARGAIN_UI_TITLE_HEIGHT
        )
        self.bargain_title = UILabel(
            stock_player_1_rect,
            "Le cedole di " + self.__player.get_name() + ":",
            manager=self.manager,
            container=self.bargain_ui,
        )

        # Create multiple selection list for player stocks
        self.stocks_player_1 = UISelectionList(
            relative_rect=pygame.Rect(
                50, 100, BARGAIN_SELECTION_LIST_WIDTH, BARGAIN_SELECTION_LIST_HEIGHT
            ),
            item_list=self.__player.get_stocks_names(),
            manager=self.manager,
            container=self.bargain_ui,
            allow_multi_select=True,
        )
        player_names = list(map(lambda player: player.get_name(), self.__other_players))

        # Create a selector for the players
        self.player_selector = UIDropDownMenu(
            options_list=player_names,
            starting_option=player_names[0],
            relative_rect=pygame.Rect(
                400, 50, BARGAIN_DROPDOWN_WIDTH, BARGAIN_DROPDOWN_HEIGHT
            ),
            manager=self.manager,
            container=self.bargain_ui,
        )

        # Create multiple selection list for player stocks
        self.stocks_player_2 = UISelectionList(
            relative_rect=pygame.Rect(
                400, 100, BARGAIN_SELECTION_LIST_WIDTH, BARGAIN_SELECTION_LIST_HEIGHT
            ),
            item_list=self.__other_players[0].get_stocks_names(),
            manager=self.manager,
            container=self.bargain_ui,
            allow_multi_select=True,
        )

        bargains_label_rect = pygame.Rect(
            (
                50,
                BARGAIN_UI_HEIGHT
                - 110
                - BARGAIN_SELECTION_LIST_HEIGHT
                - BARGAIN_UI_TITLE_HEIGHT,
            ),
            (BARGAIN_UI_TITLE_WIDTH, BARGAIN_UI_TITLE_HEIGHT),
        )
        self.bargains_label = UILabel(
            bargains_label_rect,
            "Scambi",
            manager=self.manager,
            container=self.bargain_ui,
        )
        # Create multiple selection list for bargains
        self.bargains_selection_list = UISelectionList(
            relative_rect=pygame.Rect(
                50,
                BARGAIN_UI_HEIGHT - 100 - BARGAIN_SELECTION_LIST_HEIGHT,
                BARGAIN_SELECTION_LIST_WIDTH,
                BARGAIN_SELECTION_LIST_HEIGHT,
            ),
            item_list=[],
            manager=self.manager,
            container=self.bargain_ui,
            allow_multi_select=True,
        )

        bargain_rect = pygame.Rect(
            BARGAIN_UI_WIDTH - BARGAIN_UI_BUT_WIDTH * 2 - 30,
            BARGAIN_UI_HEIGHT - 100,
            BARGAIN_UI_BUT_WIDTH,
            BARGAIN_UI_BUT_HEIGHT,
        )
        add_bargain_rect = pygame.Rect(
            50 + BARGAIN_SELECTION_LIST_WIDTH + 20,
            BARGAIN_UI_HEIGHT - 400,
            BARGAIN_UI_BUT_WIDTH,
            BARGAIN_UI_BUT_HEIGHT,
        )
        remove_bargain_rect = pygame.Rect(
            50 + BARGAIN_SELECTION_LIST_WIDTH + 20,
            BARGAIN_UI_HEIGHT - 300,
            BARGAIN_UI_BUT_WIDTH,
            BARGAIN_UI_BUT_HEIGHT,
        )
        close_rect = pygame.Rect(
            BARGAIN_UI_WIDTH - BARGAIN_UI_BUT_WIDTH,
            BARGAIN_UI_HEIGHT - 100,
            BARGAIN_UI_BUT_WIDTH,
            BARGAIN_UI_BUT_HEIGHT,
        )

        self.bargain_butt = UIButton(
            relative_rect=bargain_rect,
            text="Contratta",
            container=self.bargain_ui,
            object_id="BARGAIN",
            manager=self.manager,
        )

        self.add_bargain_butt = UIButton(
            relative_rect=add_bargain_rect,
            text="Aggiungi scambio",
            container=self.bargain_ui,
            object_id="ADD_BARGAIN",
            manager=self.manager,
        )

        self.remove_bargain_butt = UIButton(
            relative_rect=remove_bargain_rect,
            text="Rimuovi Scambio",
            container=self.bargain_ui,
            object_id="REMOVE_BARGAIN",
            manager=self.manager,
        )

        self.close_butt = UIButton(
            relative_rect=close_rect,
            text="Chiudi",
            container=self.bargain_ui,
            object_id="CLOSE_BARGAIN",
            manager=self.manager,
        )

        money_excange_label_rect = pygame.Rect(
            (
                BARGAIN_UI_WIDTH // 2 + 130,
                BARGAIN_UI_HEIGHT
                - 110
                - BARGAIN_SELECTION_LIST_HEIGHT
                - BARGAIN_UI_TITLE_HEIGHT,
            ),
            (BARGAIN_UI_TITLE_WIDTH, BARGAIN_UI_TITLE_HEIGHT),
        )

        self.money_excange_label = UILabel(
            money_excange_label_rect,
            "Denaro da scambiare",
            manager=self.manager,
            container=self.bargain_ui,
        )

        self.money_excange = UITextEntryLine(
            relative_rect=pygame.Rect(BARGAIN_UI_WIDTH // 2 + 200, 500, 200, 40),
            manager=self.manager,
            container=self.bargain_ui,
            parent_element=self.bargain_ui,
            object_id="money_excange",
            initial_text="0",
        )
        self.money_excange.set_allowed_characters("numbers")

        self.draw_give_or_receive()
  
    def close_ui(self):
        self.bargain_ui.kill()
        self.game.bargain_ui = None
        self.game.current_panel = None

    def manage_events(self, event, players=None, current_player=None):
        if (
            hasattr(self, "player_selector")
            and event.ui_element == self.player_selector
        ):
            player = self.get_player(event.text)
            self.showed_player = player  # type: ignore
            self.update_stocks()
            self.money_excange.set_text(str(self.exchange_values[self.showed_player_index]))
            self.give_or_receive.kill()
            self.draw_give_or_receive()
        elif (
            hasattr(self, "add_bargain_butt")
            and event.ui_element == self.add_bargain_butt
        ):  # pragma: no cover
            self.add_bargains()
            self.update_stocks()
        elif (
            hasattr(self, "remove_bargain_butt")
            and event.ui_element == self.remove_bargain_butt
        ):  # pragma: no cover
            self.remove_bargains()
            self.update_stocks()
        elif (
            hasattr(self, "bargain_butt") and event.ui_element == self.bargain_butt
        ):  # pragma: no cover
            # process the bargains and close the window
            self.process_bargains()
            self.close_ui()
            self.screen.fill(BLACK)
            self.game.renable_actions()
        elif (
            hasattr(self, "close_butt") and event.ui_element == self.close_butt
        ):  # pragma: no cover
            self.close_ui()
            self.screen.fill(BLACK)
            self.game.renable_actions()
        elif hasattr(self, "money_excange") and event.ui_element == self.money_excange:
            if event.text == "":
                self.allow_money_excange(0)
            else:
                self.allow_money_excange(int(event.text))
        elif (
            hasattr(self, "give_or_receive")
            and event.ui_element == self.give_or_receive
        ):
            self.exchange_direction[self.showed_player_index] = event.text
            self.allow_money_excange(self.exchange_values[self.showed_player_index])

    def get_player(self, player_name):
        for i, player in enumerate(self.__other_players):
            if player.get_name() == player_name:
                self.showed_player_index = i
                return player

    def draw_give_or_receive(self):
        self.give_or_receive = UIDropDownMenu(
            options_list=["Dai", "Ricevi"],
            starting_option=self.exchange_direction[self.showed_player_index],
            relative_rect=pygame.Rect(
                BARGAIN_UI_WIDTH // 2 + 200,
                550,
                BARGAIN_DROPDOWN_WIDTH,
                BARGAIN_DROPDOWN_HEIGHT,
            ),
            manager=self.manager,
            container=self.bargain_ui,
        )

    def allow_money_excange(self, amount):
        """
        With dai the current player give money to the selected player
        which is named showed_player. So if the current player has enough 
        money there is no problem, otherwise we set the number to the maximum
        possibile. The opposite apply when we have setted Ricevi.
        """
        self.exchange_values[self.showed_player_index] = amount
        if self.exchange_direction[self.showed_player_index] == "Dai":
            if self.current_player_virtual_balance() < 0:
                self.exchange_values[self.showed_player_index] += self.current_player_virtual_balance()
        else:
            if self.showed_player_virtual_balance() < 0:
                self.exchange_values[self.showed_player_index] += self.showed_player_virtual_balance()
        self.money_excange.set_text(str(self.exchange_values[self.showed_player_index]))

    def current_player_virtual_balance(self):
        virtual_balance = self.__player.get_balance()
        for i, amount in enumerate(self.exchange_values):
            if self.exchange_direction[i] == "Dai":
                virtual_balance -= amount
            else:
                virtual_balance += amount
        return virtual_balance

    def showed_player_virtual_balance(self):
        return self.showed_player.get_balance() - self.exchange_values[self.showed_player_index]

    @staticmethod
    def get_stock(stock_name, player):
        for stock in player.get_stocks():
            if stock.get_name() == stock_name:
                return stock

    def add_bargains(self):
        stocks_player_1 = self.stocks_player_1.get_multi_selection()
        stocks_player_2 = self.stocks_player_2.get_multi_selection()

        if len(stocks_player_1) > 0 and len(stocks_player_2) > 0:
            bargains_to_add = []
            for stock_name in stocks_player_1:
                bargains_to_add.append(
                    "GIVE --> :" + stock_name + ": " + self.showed_player.get_name()
                )
                self.stocks_given.append(
                    {"stock": stock_name, "player": self.showed_player.get_name()}
                )

            for stock_name in stocks_player_2:
                bargains_to_add.append(
                    "GET <-- :" + stock_name + ": " + self.showed_player.get_name()
                )
                self.stocks_got.append(
                    {"stock": stock_name, "player": self.showed_player.get_name()}
                )

            self.bargains_selection_list.add_items(bargains_to_add)

    def remove_bargains(self):
        bargains_to_remove = self.bargains_selection_list.get_multi_selection()

        if len(bargains_to_remove) > 0:
            for bargain in bargains_to_remove:
                matches = re.finditer(":", bargain)
                indexes = [match.start() for match in matches]
                stock_name = bargain[indexes[0] + 1 : indexes[1]]

                if bargain[:3] == "GET":
                    new_stocks_got = []
                    for stock_got in self.stocks_got:
                        if stock_name != stock_got["stock"]:
                            new_stocks_got.append(stock_got)
                    self.stocks_got = new_stocks_got
                else:
                    new_stocks_given = []
                    for stock_given in self.stocks_given:
                        if stock_name != stock_given["stock"]:
                            new_stocks_given.append(stock_given)

                    self.stocks_given = new_stocks_given

            self.bargains_selection_list.remove_items(bargains_to_remove)

    def update_stocks(self):
        player1_stocks = self.__player.get_stocks_names()
        player2_stocks = self.showed_player.get_stocks_names()
        player2_name = self.showed_player.get_name()

        player1_stocks_to_show = []

        for stock_name in player1_stocks:
            ok_to_show = True
            for stock_given in self.stocks_given:
                if stock_name == stock_given["stock"]:
                    ok_to_show = False

            if ok_to_show:
                player1_stocks_to_show.append(stock_name)

        player2_stocks_to_show = []
        if len(self.stocks_got) > 0:
            for stock_name in player2_stocks:
                ok_to_show = True
                for stock_got in self.stocks_got:
                    if (
                        player2_name == stock_got["player"]
                        and stock_name == stock_got["stock"]
                    ):
                        ok_to_show = False

                if ok_to_show:
                    player2_stocks_to_show.append(stock_name)
        else:
            player2_stocks_to_show = player2_stocks

        self.stocks_player_1.set_item_list(player1_stocks_to_show)
        self.stocks_player_2.set_item_list(player2_stocks_to_show)

    def process_bargains(self):
        # here we transfer the stocks from the self.player to the player in the bargain
        for stock_given in self.stocks_given:
            stock = BargainUI.get_stock(stock_given["stock"], self.__player)
            player = self.get_player(stock_given["player"])
            transfer_stock(None, player, stock)

        # here we transfer the stocks from the player in the bargain to self.player
        for stock_got in self.stocks_got:
            player = self.get_player(stock_got["player"])
            stock = BargainUI.get_stock(stock_got["stock"], player)
            transfer_stock(None, self.__player, stock)

        # update current player balance
        for  amount, give_or_receive in zip(self.exchange_values, self.exchange_direction):
            if give_or_receive == "Dai":
                self.__player.change_balance(-amount)
            else:
                self.__player.change_balance(amount)

        # update other players balance
        for amount, give_or_receive, player in zip(self.exchange_values, self.exchange_direction, self.__other_players):
            if give_or_receive == "Dai":
                player.change_balance(amount)
            else:
                player.change_balance(-amount)

        self.game.get_gameUI().updateAllPlayerLables(self.game.get_players())