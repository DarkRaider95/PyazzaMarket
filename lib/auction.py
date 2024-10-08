import pygame
from pygame_gui.elements import UIButton, UIPanel, UILabel
from lib.constants import *
from lib.gameLogic import finished_auction_logic


class Auction:
    def __init__(self, manager, screen, owner, bidders, stock, board, game, game_ui):
        self.startPrice = 0
        self.endPrice = 0
        self.current_bid = 0
        self.manager = manager
        self.screen = screen
        self.__owner = owner
        self.__stock = stock
        self.__finished = False
        self.__bidders = bidders
        self.current_bidder = 0
        self.bids = [0] * len(self.__bidders)
        self.startPrice = self.__stock.get_new_value()
        self.current_bid = self.__stock.get_new_value()
        self.__winner = None
        self.__board = board
        self.__game = game
        self.__game_ui = game_ui

    def draw(self):
        currBidderName = self.__bidders[self.current_bidder].get_name()

        panel_rect = pygame.Rect(
            (WIDTH // 2 - AUCTION_UI_WIDTH // 2, 20),
            (AUCTION_UI_WIDTH, AUCTION_UI_HEIGHT),
        )
        self.auctionUI = UIPanel(panel_rect, starting_height=2, manager=self.manager)

        title_rect = pygame.Rect(
            (AUCTION_UI_WIDTH // 2 - AUCTION_UI_TITLE_WIDTH // 2, 10),
            (AUCTION_UI_TITLE_WIDTH, AUCTION_UI_TITLE_HEIGHT),
        )
        self.auctionTitle = UILabel(
            title_rect, "ASTA", manager=self.manager, container=self.auctionUI
        )

        highest_bid_rect = pygame.Rect(
            (AUCTION_UI_WIDTH // 2 - AUCTION_UI_TITLE_WIDTH // 2, 30),
            (AUCTION_UI_TITLE_WIDTH, AUCTION_UI_TITLE_HEIGHT),
        )
        self.stockInAuction = UILabel(
            highest_bid_rect,
            "Quanto offri per: " + self.__stock.get_name() + "?",
            manager=self.manager,
            container=self.auctionUI,
        )

        current_bidder_rect = pygame.Rect(
            (
                AUCTION_UI_WIDTH // 2
                - AUCTION_UI_TITLE_WIDTH // 2
                - AUCTION_UI_TITLE_WIDTH
                - 20,
                AUCTION_UI_HEIGHT // 2,
            ),
            (AUCTION_UI_TITLE_WIDTH, AUCTION_UI_TITLE_HEIGHT),
        )
        self.currentBidderText = UILabel(
            current_bidder_rect,
            "Offerta di " + currBidderName + ":",
            manager=self.manager,
            container=self.auctionUI,
        )

        bid_text_rect = pygame.Rect(
            (
                AUCTION_UI_WIDTH // 2 - AUCTION_BID_TEXT_WIDTH // 2,
                AUCTION_UI_HEIGHT // 2,
            ),
            (AUCTION_BID_TEXT_WIDTH, AUCTION_BID_TEXT_HEIGHT),
        )
        self.currentBidText = UILabel(
            bid_text_rect,
            str(self.startPrice),
            manager=self.manager,
            container=self.auctionUI,
        )

        raiseBidRect = pygame.Rect(
            (bid_text_rect.x + AUCTION_BID_TEXT_WIDTH + 30, AUCTION_UI_HEIGHT // 2),
            (AUCTION_RL_BID_BUT_WIDTH, AUCTION_RL_BID_BUT_HEIGHT),
        )
        lowerBidRect = pygame.Rect(
            (
                bid_text_rect.x
                + AUCTION_BID_TEXT_WIDTH
                + AUCTION_RL_BID_BUT_WIDTH
                + 30,
                AUCTION_UI_HEIGHT // 2,
            ),
            (AUCTION_RL_BID_BUT_WIDTH, AUCTION_RL_BID_BUT_HEIGHT),
        )
        bidRect = pygame.Rect(
            (
                AUCTION_UI_WIDTH // 2 - AUCTION_UI_BUT_WIDTH * 1.5,
                AUCTION_UI_HEIGHT // 2 + 100,
            ),
            (AUCTION_UI_BUT_WIDTH, AUCTION_UI_BUT_HEIGHT),
        )
        nextRect = pygame.Rect(
            (
                AUCTION_UI_WIDTH // 2 - AUCTION_UI_BUT_WIDTH // 2,
                AUCTION_UI_HEIGHT // 2 + 100,
            ),
            (AUCTION_UI_BUT_WIDTH, AUCTION_UI_BUT_HEIGHT),
        )
        retireRect = pygame.Rect(
            (
                AUCTION_UI_WIDTH // 2 + AUCTION_UI_BUT_WIDTH // 2,
                AUCTION_UI_HEIGHT // 2 + 100,
            ),
            (AUCTION_UI_BUT_WIDTH, AUCTION_UI_BUT_HEIGHT),
        )

        self.raiseBid = UIButton(
            relative_rect=raiseBidRect,
            text="+",
            container=self.auctionUI,
            object_id="RAISE_BID",
            manager=self.manager,
        )

        self.lowerBid = UIButton(
            relative_rect=lowerBidRect,
            text="-",
            container=self.auctionUI,
            object_id="LOWER_BID",
            manager=self.manager,
        )

        self.bidBut = UIButton(
            relative_rect=bidRect,
            text="OFFRI",
            container=self.auctionUI,
            object_id="BID_BUT",
            manager=self.manager,
        )

        self.nextBidder = UIButton(
            relative_rect=nextRect,
            text="PASSA",
            container=self.auctionUI,
            object_id="PASS_BID",
            manager=self.manager,
        )

        self.retireAuction = UIButton(
            relative_rect=retireRect,
            text="RITIRATI",
            container=self.auctionUI,
            object_id="RETIRE_AUCTION",
            manager=self.manager,
        )

    def round_text_bid(self):
        remainder = self.current_bid % 10
        if remainder < 5:
            rounded_number = self.current_bid - remainder
        else:
            rounded_number = self.current_bid + (10 - remainder)

        self.currentBidText.set_text(str(rounded_number))
        self.current_bid = rounded_number

    def raise_bid(self):
        curr_bidder = self.__bidders[self.current_bidder]
        current_bidder_balance = curr_bidder.get_balance()

        if self.current_bid + 10 > current_bidder_balance:
            self.current_bid = current_bidder_balance
        else:
            self.current_bid += 10

        self.currentBidText.set_text(str(self.current_bid))

    def lower_bid(self):
        maxBidIndex = self.find_max_bid()
        if self.current_bid - 10 > max(self.startPrice, self.bids[maxBidIndex]):
            self.current_bid -= 10
        else:
            self.current_bid = max(self.startPrice, self.bids[maxBidIndex])
        self.currentBidText.set_text(str(self.current_bid))

    def bid_but(self):
        if not hasattr(self, "currentHighestBid"):
            highest_bid_rect = pygame.Rect(
                (AUCTION_UI_WIDTH // 2 - AUCTION_UI_TITLE_WIDTH // 2, 50),
                (AUCTION_UI_TITLE_WIDTH, AUCTION_UI_TITLE_HEIGHT),
            )
            self.currentHighestBid = UILabel(
                highest_bid_rect,
                "L'offerta più alta è di " + self.__bidders[self.current_bidder].get_name(),
                manager=self.manager,
                container=self.auctionUI,
            )
        else:
            self.currentHighestBid.set_text(
                "L'offerta più alta è di " + self.__bidders[self.current_bidder].get_name()
            )
        self.round_text_bid()
        self.bids[self.current_bidder] = self.current_bid

        # remove the bidders that haven't enough balance
        self.remove_bidders_who_cant_afford()

        if len(self.__bidders) > 1:
            self.current_bidder = (self.current_bidder + 1) % len(self.__bidders)
            self.currentBidderText.set_text(
                "Offerta di " + self.__bidders[self.current_bidder].get_name()
            )
            self.disable_retire()
        else:  # if there is only one bidder and he has bidded it means he has won the auction
            self.__winner = self.__bidders[0]
            self.__finished = True

    def pass_bid(self):
        self.current_bidder = (self.current_bidder + 1) % len(self.__bidders)
        self.currentBidderText.set_text(
            "Offerta di " + self.__bidders[self.current_bidder].get_name()
        )
        self.current_bid = max(self.bids[self.find_max_bid()], self.startPrice)
        self.currentBidText.set_text(str(self.current_bid))
        self.disable_retire()

    def retire_auction(self):
        self.__bidders.pop(self.current_bidder)
        self.bids.pop(self.current_bidder)

        if (
            len(self.__bidders) == 0
        ):  # if there aren't any bidders and it means no one won so the stock will be sold to the bank
            self.__finished = True
            self.__winner = None
        elif(
            len(self.__bidders) == 1 and self.bids[0] > 0
        ): # if there is only one bidder and he has bidded it means he has won the auction
            self.__finished = True
            self.__winner = self.__bidders[0]
        else:
            # the current bidder was the last I have to set 0 as the next bidder otherwise I don't have to change the index
            if (
                self.current_bidder == len(self.__bidders) - 1
                or len(self.__bidders) == 1
            ):
                self.current_bidder = 0

            self.currentBidderText.set_text(
                "Offerta di " + self.__bidders[self.current_bidder].get_name()
            )
            self.current_bid = max(self.bids[self.find_max_bid()], self.startPrice)
            self.currentBidText.set_text(str(self.current_bid))
            self.disable_retire()


    def manage_events(self, event, players=None, curr_player=None):        
        if (
            hasattr(self, "raiseBid")
            and event.ui_element == self.raiseBid
        ):
            self.raise_bid()
        elif (
            hasattr(self, "lowerBid")
            and event.ui_element == self.lowerBid
        ):
            self.lower_bid()
        elif (
            hasattr(self, "bidBut")
            and event.ui_element == self.bidBut
        ):
            self.bid_but()
            if self.is_finished():
                finished_auction_logic(self.__board, self)
                self.open_next_if_present()
        elif (
            hasattr(self, "nextBidder")
            and event.ui_element == self.nextBidder
        ):
            self.pass_bid()
        elif (
            hasattr(self, "retireAuction")
            and event.ui_element == self.retireAuction
        ):
            self.retire_auction()
            if self.is_finished():
                finished_auction_logic(self.__board, self)
                self.open_next_if_present()
                
    def open_next_if_present(self):
        auctions = self.__game.get_auctions()
        # if there are other auctions open next otherwise close it
        if len(auctions) > 0:
            self.auctionUI.kill()
            self.screen.fill(BLACK)
            self.__game.currentAuction = auctions.pop(0)
            self.__game.current_panel = None
            self.__game.panels_to_show.append(self.__game.currentAuction)
            #self.currentAuction.draw()
        else:
            self.auctionUI.kill()
            self.__game.currentAuction = None
            self.__game.current_panel = None
            self.screen.fill(BLACK)
            self.__game_ui.updateAllPlayerLables(self.__game.get_players())
            self.__game.renable_actions()

    def find_max_bid(self):
        max_value = self.bids[0]
        max_index = 0
        for i in range(1, len(self.bids)):
            if self.bids[i] > max_value:
                max_value = self.bids[i]
                max_index = i

        return max_index

    def remove_bidders_who_cant_afford(self):
        bidders_to_remove = []
        bidders_length = len(self.__bidders)

        for index, bidder in enumerate(self.__bidders):
            if bidder.get_balance() < self.current_bid:
                bidders_to_remove.append(index)

        for remove_index in bidders_to_remove:
            self.__bidders.pop(remove_index)
            self.bids.pop(remove_index)

            if remove_index == bidders_length - 1 or len(self.__bidders) == 1:
                self.current_bidder = 0

    def disable_retire(self):
        if self.current_bidder == self.find_max_bid() and sum(self.bids) > 0:
            self.retireAuction.disable()
        else:
            self.retireAuction.enable()

    def is_finished(self):
        return self.__finished

    def get_owner(self):
        return self.__owner

    def get_stock(self):
        return self.__stock

    def get_bidders(self):
        return self.__bidders

    def get_winner_bid(self):
        return self.bids[0]

    def get_winner(self):
        return self.__winner
