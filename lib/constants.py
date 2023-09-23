# Window dimensions
WIDTH = 1600
HEIGHT = 1000

# Stock dimensions
STOCK_HEIGHT = 800
STOCK_WIDTH = 700
LOGO_WIDTH = 350
LOGO_HEIGHT = 200
PRICES_HEIGHT = 300
PRICE_WIDTH = 500
# Colori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

FPS = 60

INITIAL_BALANCE = 3000
SQUARE_BALANCE = 2000
CRASH_FEE = 100
TURN_FEE = 300

#Board dimensions
CELL_HEIGHT = 150
CELL_WIDTH = 75
CORNER_HEIGHT = 150
CORNER_WIDTH = 150
CELL_LOGO_WIDTH = 70
CELL_LOGO_HEIGHT = 40
CELL_COLOR_HEIGHT = 35
CELL_COLOR_WIDTH = 75

ASSET_PATH = 'assets/'

#assets path
CORNER_1 = ASSET_PATH + 'corner_1.png'
CORNER_2 = ASSET_PATH + 'corner_2.png'
CORNER_3 = ASSET_PATH + 'corner_3.png'
CORNER_4 = ASSET_PATH + 'corner_4.png'
CAR_YELLOW = ASSET_PATH + 'car_yellow.png'
CAR_BLUE = ASSET_PATH + 'car_blue.png'
CAR_BLACK = ASSET_PATH + 'car_black.png'
CAR_RED = ASSET_PATH + 'car_red.png'
EVENT = ASSET_PATH + 'event.png'
FREE_STOP = ASSET_PATH + 'fermata-libera.png'
QUOTE_IMAGE = ASSET_PATH + 'quotation.png'
CHANCE = ASSET_PATH + 'chance.png'
DICE_1 = ASSET_PATH + 'dice1.png'
DICE_2 = ASSET_PATH + 'dice2.png'
DICE_3 = ASSET_PATH + 'dice3.png'
DICE_4 = ASSET_PATH + 'dice4.png'
DICE_5 = ASSET_PATH + 'dice5.png'
DICE_6 = ASSET_PATH + 'dice6.png'

#PATH OF THE EVENTS IMAGES
EVENTS_DIR = "assets/events/"

#PATH OF STOCK LOGOS
LOGOS_DIR = "assets/cedole/"

#EVENT DIMENSIONS
EVENT_WIDTH = 500
EVENT_HEIGHT = 700

#EVENT TYPES
COLOR_EVENT = 'COLOR_EVENT'
BUY_ANTHING_EVENT = 'BUY_ANTHING_EVENT'
STOP_1 = 'STOP_1'
FREE_PENALTY = 'FREE_PENALTY'
FREE_PENALTY_MARTINI = 'FREE_PENALTY_MARTINI'
EVERYONE_FIFTY_EVENT = 'EVERYONE_FIFTY_EVENT'
GIFT_EVENT = 'GIFT_EVENT'
GET_EVENT = 'GET_EVENT'
PAY_EVENT = 'PAY_EVENT'
GO_EVENT = 'GO_EVENT'
OWN_EVENT = 'OWN_EVENT'
BUY_EVENT = 'BUY_EVENT'
PREVIOUS_PLAYER_GALUP = 'PREVIOUS_PLAYER_GALUP'
NEXT_PLAYER_PAY = 'NEXT_PLAYER_PAY'
# CAR DIMENSIONS
CAR_WIDTH = 27
CAR_HEIGHT = 57

# DICE DIMENSIONS
DICE_WIDTH = 50
DICE_HEIGHT = 50
DICE_SURFACE_X = 460
DICE_SURFACE_Y = 800

# STOCK BOARD DIMENSIONS
STOCKBOARD_WIDTH = 222
STOCKBOARD_HEIGHT = 334

#CELLS OBJECT
CELLS_DEF = {
    'ORANGE':{
        'logos': ['gled.png', 'friskies.png', 'frio.png'],
        'value': 200,
        'color': ORANGE,
        'penalty': [60, 160, 160, 200, 260, 500],
        'side': 'BOT',
        'angle': 0,
        'names': ['gled', 'friskies', 'frio'],
        'index': 0
    },
    'LIGHT_BLUE':{
        'logos': ['finish.png', 'dash.png', 'cuore.png'],
        'value': 280,
        'color': LIGHT_BLUE,
        'penalty': [80,220,220,280,360,700],
        'side': 'BOT',
        'angle': 0,
        'names': ['finish', 'dash', 'cuore'],
        'index': 1
    },
    'PINK':{
        'logos': ['zarotti.png', 'ponti.jpg', 'nostromo.png'],
        'value': 360,
        'color': PINK,
        'penalty': [100, 280, 280, 360, 460, 900],
        'side': 'LEFT',
        'angle': -90,
        'names': ['zarotti', 'ponti', 'nostromo'],
        'index': 2
    },
    'GREEN':{
        'logos': ['barilla.png', 'euvita.png', 'galbusera.png'],
        'value': 440,
        'color': GREEN,
        'penalty': [120, 340, 340, 440, 560, 1000],
        'side': 'LEFT',
        'angle': -90,
        'names': ['barilla', 'euvita', 'galbusera'],
        'index': 3
    },
    'RED':{
        'logos': ['lavazza.png', 'mangia-e-bevi.png', 'stella-artois.png'],
        'value': 500,
        'color': RED,
        'penalty': [140, 380, 380, 500, 660, 1200],
        'side': 'TOP',
        'angle': 180,
        'names': ['lavazza', 'mangiaebevi', 'stella-artois'],
        'index': 4
    },
    'BLUE':{
        'logos': ['san-benedetto.png', 'pepsi.png', 'schweppes.png'],
        'value': 600,
        'color': BLUE,
        'penalty': [160, 460, 460, 600, 760, 1500],
        'side': 'TOP',
        'angle': 180,
        'names': ['san-benedetto', 'pepsi', 'schweppes'],
        'index': 5
    },
    'YELLOW':{
        'logos': ['ibis.png', 'frendies.png', 'yoplait.png'],
        'value': 700,
        'color': YELLOW,
        'penalty': [180, 560, 560, 700, 880, 1760],
        'side': 'RIGHT',
        'angle': 90,
        'names': ['ibis', 'frendies', 'yoplait'],
        'index': 6
    },
    'PURPLE':{
        'logos': ['cavicchioli.jpg', 'martini.png', 'galup.png'],
        'value': 800,
        'color': PURPLE,
        'penalty': [200, 600, 600, 800, 1000, 2000],
        'side': 'RIGHT',
        'angle': 90,
        'names': ['cavicchioli', 'martini', 'galup'],
        'index': 7
    }

}

# QUOTATION FOR ORANGE, LIGHT_BLUE, PINK, GREEN, RED, BLUE, YELLOW, PURPLE
QUOTATION = [(220,280,410,490,500,300,700,900),
             (180,280,380,340,500,600,700,800),
             (600,280,360,240,500,600,200,600),
             (200,380,360,390,500,600,1100,1000),
             (250,180,160,440,500,700,700,400),
             (200,280,260,390,500,400,700,200),
             (220,280,260,540,500,600,700,800),
             (200,280,560,540,200,550,700,800),
             (200,260,360,490,500,600,700,900),
             (200,280,310,140,700,600,700,800),
             (200,230,460,340,500,650,700,800),
             (200,580,360,540,500,550,700,800)]

#UI dimesions
ACTIONS_WIDTH = 400
ACTIONS_HEIGHT = 250
STATUS_WIDTH = 500
STATUS_HEIGHT = 300
LABEL_WIDTH = 70
LABEL_HEIGHT = 30
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 30
LEADERBOARD_WIDTH = 400
LEADERBOARD_HEIGHT = 230
LEADERBOARD_LABEL_WIDTH = 250
STOCK_UI_WIDTH = 1000
STOCK_UI_HEIGHT = 900
STOCK_UI_BUT_WIDTH = 100
STOCK_UI_BUT_HEIGHT = 100
STOCK_UI_TITLE_WIDTH = 300
STOCK_UI_TITLE_HEIGHT = 50
EVENT_UI_WIDTH = 1000
EVENT_UI_HEIGHT = 900
EVENT_UI_TITLE_WIDTH = 300
EVENT_UI_TITLE_HEIGHT = 50
EVENT_UI_BUT_WIDTH = 100
EVENT_UI_BUT_HEIGHT = 100
ALERT_HEIGHT = 100
ALERT_WIDTH = 300
ALERT_MESSAGE_HEIGHT = 20
ALERT_MESSAGE_WIDTH = 150
ALERT_BUT_HEIGHT = 30
ALERT_BUT_WIDTH = 100
#AUCTION UI DIMENSIONS
AUCTION_UI_WIDTH = 1000
AUCTION_UI_HEIGHT = 900
AUCTION_UI_BUT_WIDTH = 100
AUCTION_UI_BUT_HEIGHT = 100
AUCTION_UI_TITLE_WIDTH = 300
AUCTION_UI_TITLE_HEIGHT = 50
AUCTION_BID_TEXT_HEIGHT = 40
AUCTION_BID_TEXT_WIDTH = 100
AUCTION_RL_BID_BUT_WIDTH = 50
AUCTION_RL_BID_BUT_HEIGHT = 50

#DICE GUI
DICE_OVERLAY_HEIGHT = 170
DICE_OVERLAY_WIDTH = 250
THROW_DICE_BUT_HEIGHT = 50
THROW_DICE_BUT_WIDTH = 50

#BARGAIN UI DIMENSIONS
BARGAIN_UI_WIDTH = 1000
BARGAIN_UI_HEIGHT = 900
BARGAIN_UI_BUT_WIDTH = 100
BARGAIN_UI_BUT_HEIGHT = 100
BARGAIN_UI_TITLE_WIDTH = 300
BARGAIN_UI_TITLE_HEIGHT = 50
BARGAIN_SELECTION_LIST_HEIGHT = 300
BARGAIN_SELECTION_LIST_WIDTH = 300
BARGAIN_DROPDOWN_WIDTH = 200
BARGAIN_DROPDOWN_HEIGHT = 30

#TAKE SOMEONE UI DIMENSIONS
TAKE_SOMEONE_UI_WIDTH = 400
TAKE_SOMEONE_UI_HEIGHT = 400
TAKE_SOMEONE_UI_BUT_WIDTH = 100
TAKE_SOMEONE_UI_BUT_HEIGHT = 100
TAKE_SOMEONE_UI_TITLE_WIDTH = 300
TAKE_SOMEONE_UI_TITLE_HEIGHT = 50
TAKE_SOMEONE_DROPDOWN_WIDTH = 200
TAKE_SOMEONE_DROPDOWN_HEIGHT = 30

#CELL TYPES
START_TYPE = 'START'
EVENTS_TYPE = 'EVENT'
FREE_STOP_TYPE = 'FREE_STOP'
STOCKS_PRIZE_TYPE = 'STOCKS_PRIZE'
QUOTATION_TYPE = 'QUOTATION'
CHOOSE_STOCK_TYPE = 'CHOOSE_STOCK'
CHANCE_TYPE = 'CHANCE'
SIX_HUNDRED_TYPE = '600_PRIZE'
STOCKS_TYPE = 'STOCKS'