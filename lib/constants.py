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

#Board dimensions
CELL_HEIGHT = 150
CELL_WIDTH = 75
CORNER_HEIGHT = 150
CORNER_WIDTH = 150
CELL_LOGO_WIDTH = 71
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

# CAR DIMENSIONS
CAR_WIDTH = 30
CAR_HEIGHT = 65

#CELLS OBJECT
CELLS_DEF = {
    'ORANGE':{
        'logos': ['gled.png', 'frieskes.png', 'frio.png'],
        'value': 200,
        'color': ORANGE,
        'penalty': [60, 160, 160, 200, 260, 500],
        'side': 'BOT',
        'angle': 0
    },
    'LIGHT_BLUE':{
        'logos': ['finish.png', 'dash.png', 'cuore.png'],
        'value': 280,
        'color': LIGHT_BLUE,
        'penalty': [80,220,220,280,360,700],
        'side': 'BOT',
        'angle': 0
    },
    'PINK':{
        'logos': ['zarotti.png', 'ponti.png', 'nostromo.png'],
        'value': 360,
        'color': PINK,
        'penalty': [100, 280, 280, 360, 460, 900],
        'side': 'LEFT',
        'angle': -90
    },
    'GREEN':{
        'logos': ['barilla.png', 'euvita.png', 'galbusera.png'],
        'value': 440,
        'color': GREEN,
        'penalty': [120, 340, 340, 440, 560, 1000],
        'side': 'LEFT',
        'angle': -90
    },
    'RED':{
        'logos': ['lavazza.png', 'mangiaebevi.png', 'stella-artois.png'],
        'value': 500,
        'color': RED,
        'penalty': [140, 380, 380, 500, 660, 1200],
        'side': 'TOP',
        'angle': 180
    },
    'BLUE':{
        'logos': ['san-benedetto.png', 'pepsi.png', 'schweppes.png'],
        'value': 600,
        'color': BLUE,
        'penalty': [160, 460, 460, 600, 760, 1500],
        'side': 'TOP',
        'angle': 180
    },
    'YELLOW':{
        'logos': ['ibis.png', 'friendies.png', 'yoplait.png'],
        'value': 700,
        'color': YELLOW,
        'penalty': [180, 560, 560, 700, 880, 1760],
        'side': 'RIGHT',
        'angle': 90
    },
    'PURPLE':{
        'logos': ['cavicchioli.png', 'martini.png', 'galup.png'],
        'value': 800,
        'color': PURPLE,
        'penalty': [200, 600, 600, 800, 1000, 2000],
        'side': 'RIGHT',
        'angle': 90
    }

}

QUOTATION = ((220,280,410,490,500,300,700,900),
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
             (200,580,360,540,500,550,700,800))