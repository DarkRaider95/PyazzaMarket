import pygame
from pygame_gui.elements import UIButton, UIPanel, UILabel, UITextEntryLine
from .constants import *

class Auction:

    def __init__(self, manager, screen):
        self.startPrice = 0
        self.endPrice = 0
        self.currentBid = 0
        self.currentBidder = None
        self.bidders = None
        self.manager = manager
        self.screen = screen
        self.nextBidder = None
        self.retireAutction = None
        self.bidBut = None
        self.raiseBid = None
        self.lowerBid = None        
        self.bids = None
        self.stock = None
        self.__finished = False

    def start_auction(self, start_price, bidders, stock):
        self.startPrice = start_price
        self.currentBid = start_price
        self.bidders = bidders
        self.currentBidder = 0
        self.bids = [0] * len(bidders)
        self.stock = stock

        self.draw_auction()

    def draw_auction(self):
        currBidderName = self.bidders[self.currentBidder].get_name()

        panel_rect = pygame.Rect((WIDTH // 2 - AUCTION_UI_WIDTH // 2, 20), (AUCTION_UI_WIDTH, AUCTION_UI_HEIGHT))
        self.auctionUI = UIPanel(panel_rect, starting_height= 2, manager=self.manager)
        
        title_rect = pygame.Rect((AUCTION_UI_WIDTH // 2 - AUCTION_UI_TITLE_WIDTH // 2, 10), (AUCTION_UI_TITLE_WIDTH, AUCTION_UI_TITLE_HEIGHT))
        self.auctionTitle = UILabel(title_rect, "ASTA", manager=self.manager, container=self.auctionUI)

        highest_bid_rect = pygame.Rect((AUCTION_UI_WIDTH // 2 - AUCTION_UI_TITLE_WIDTH // 2, 30), (AUCTION_UI_TITLE_WIDTH, AUCTION_UI_TITLE_HEIGHT))
        self.stockInAuction = UILabel(highest_bid_rect, "Quanto offri per: "+ self.stock.get_name() + "?", manager=self.manager, container=self.auctionUI)

        highest_bid_rect = pygame.Rect((AUCTION_UI_WIDTH // 2 - AUCTION_UI_TITLE_WIDTH // 2, 50), (AUCTION_UI_TITLE_WIDTH, AUCTION_UI_TITLE_HEIGHT))
        self.currentHighestBid = UILabel(highest_bid_rect, "L'offerta più alta è di "+ currBidderName, manager=self.manager, container=self.auctionUI)

        current_bidder_rect = pygame.Rect((AUCTION_UI_WIDTH // 2 - AUCTION_UI_TITLE_WIDTH // 2 - AUCTION_UI_TITLE_WIDTH - 20, AUCTION_UI_HEIGHT // 2), (AUCTION_UI_TITLE_WIDTH, AUCTION_UI_TITLE_HEIGHT))
        self.currentBidderText = UILabel(current_bidder_rect, "Offerta di "+ currBidderName+ ":", manager=self.manager, container=self.auctionUI)


        #bid_text_rect = pygame.Rect((WIDTH // 2 - AUCTION_BID_TEXT_WIDTH, AUCTION_UI_HEIGHT // 2), (AUCTION_BID_TEXT_WIDTH, AUCTION_BID_TEXT_HEIGHT))
        bid_text_rect = pygame.Rect((AUCTION_UI_WIDTH // 2 - AUCTION_BID_TEXT_WIDTH // 2, AUCTION_UI_HEIGHT // 2), (AUCTION_BID_TEXT_WIDTH, AUCTION_BID_TEXT_HEIGHT))
        self.currentBidText = UILabel(bid_text_rect, str(self.startPrice), manager=self.manager, container=self.auctionUI)
        #self.currentBidText = UITextEntryLine(relative_rect=bid_text_rect,
        #                                        manager=self.manager,
        #                                        object_id="AUCTION_BID_TEXT",
        #                                        initial_text=str(self.startPrice))

        raiseBidRect = pygame.Rect((bid_text_rect.x + AUCTION_BID_TEXT_WIDTH + 30, AUCTION_UI_HEIGHT // 2), (AUCTION_RL_BID_BUT_WIDTH, AUCTION_RL_BID_BUT_HEIGHT))
        lowerBidRect = pygame.Rect((bid_text_rect.x + AUCTION_BID_TEXT_WIDTH + AUCTION_RL_BID_BUT_WIDTH + 30, AUCTION_UI_HEIGHT // 2), (AUCTION_RL_BID_BUT_WIDTH, AUCTION_RL_BID_BUT_HEIGHT))
        bidRect = pygame.Rect((AUCTION_UI_WIDTH // 2 - AUCTION_UI_BUT_WIDTH * 1.5, AUCTION_UI_HEIGHT // 2 + 100), (AUCTION_UI_BUT_WIDTH, AUCTION_UI_BUT_HEIGHT))
        nextRect = pygame.Rect((AUCTION_UI_WIDTH // 2 - AUCTION_UI_BUT_WIDTH // 2, AUCTION_UI_HEIGHT // 2 + 100), (AUCTION_UI_BUT_WIDTH, AUCTION_UI_BUT_HEIGHT))
        retireRect = pygame.Rect((AUCTION_UI_WIDTH // 2  + AUCTION_UI_BUT_WIDTH // 2, AUCTION_UI_HEIGHT // 2 + 100), (AUCTION_UI_BUT_WIDTH, AUCTION_UI_BUT_HEIGHT))
        #bidRect = pygame.Rect((AUCTION_UI_WIDTH // 3 - AUCTION_UI_BUT_WIDTH, AUCTION_UI_HEIGHT // 2 + 100), (AUCTION_UI_BUT_WIDTH, AUCTION_UI_BUT_HEIGHT))
        #nextRect = pygame.Rect((AUCTION_UI_WIDTH // 3 * 2 - AUCTION_UI_BUT_WIDTH, AUCTION_UI_HEIGHT // 2 + 100), (AUCTION_UI_BUT_WIDTH, AUCTION_UI_BUT_HEIGHT))
        #retireRect = pygame.Rect((AUCTION_UI_WIDTH - AUCTION_UI_WIDTH // 3 - AUCTION_UI_BUT_WIDTH, AUCTION_UI_HEIGHT // 2 + 100), (AUCTION_UI_BUT_WIDTH, AUCTION_UI_BUT_HEIGHT))

        self.raiseBid = UIButton(relative_rect=raiseBidRect,
                                text="+",
                                container=self.auctionUI,
                                object_id = 'RAISE_BID',
                                manager=self.manager)
        
        self.lowerBid = UIButton(relative_rect=lowerBidRect,
                                text="-",
                                container=self.auctionUI,
                                object_id = 'LOWER_BID',
                                manager=self.manager)
        
        self.bidBut = UIButton(relative_rect=bidRect,
                                text="OFFRI",
                                container=self.auctionUI,
                                object_id = 'BID_BUT',
                                manager=self.manager)
        
        self.nextBidder = UIButton(relative_rect=nextRect,
                                text="PASSA",
                                container=self.auctionUI,
                                object_id = 'PASS_BID',
                                manager=self.manager)
        
        self.retireAutction = UIButton(relative_rect=retireRect,
                                text="RITIRATI",
                                container=self.auctionUI,
                                object_id = 'RETIRE_AUCTION',
                                manager=self.manager)
        
    def round_text_bid(self):
        remainder = self.currentBid % 10
        if remainder < 5:
            rounded_number = self.currentBid - remainder
        else:
            rounded_number = self.currentBid + (10 - remainder)

        #self.currentBidText.text = str(rounded_number)
        self.currentBidText.set_text(str(rounded_number))
        self.currentBid = rounded_number

    def raise_bid(self):
        self.currentBid += 10
        #self.currentBidText.text = str(self.currentBid)
        self.currentBidText.set_text(str(self.currentBid))
        
    def lower_bid(self):
        self.currentBid -= 10
        #self.currentBidText.text = str(self.currentBid)
        self.currentBidText.set_text(str(self.currentBid))

    def bid_but(self):
        self.currentHighestBid.set_text("L'offerta più alta è di "+ self.bidders[self.currentBidder].get_name())
        self.round_text_bid()
        self.bids[self.currentBidder] = self.currentBid
        self.currentBidder = (self.currentBidder +  1) % len(self.bidders)
        self.currentBidderText.set_text("Offerta di "+ self.bidders[self.currentBidder].get_name())
        
    def pass_bid(self):
        self.currentBidder = (self.currentBidder +  1) % len(self.bidders)
        self.currentBidderText.set_text("Offerta di "+ self.bidders[self.currentBidder].get_name())
    
    def retire_auction(self):
        nextBidder = (self.currentBidder +  1) % len(self.bidders)
        self.bidders.pop(self.currentBidder)
        self.currentBidder = nextBidder
        self.currentBidderText.set_text("Offerta di "+ self.bidders[nextBidder].get_name())
        maxBidIndex = self.find_max_bid()
        self.currentHighestBid.set_text("L'offerta più alta è di "+ self.bidders[maxBidIndex].get_name())
        if len(self.bidders) == 1:
            self.finished = True
    
    def find_max_bid(self):
        max_value = self.bids[0]
        max_index = 0
        for i in range(1, len(self.bids)):
            if self.bids[i] > max_value:
                max_value = self.bids[i]
                max_index = i

        return max_index
    
    def is_finished(self):
        return self.__finished