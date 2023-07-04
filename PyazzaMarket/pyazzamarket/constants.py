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

ASSET_PATH = 'PyazzaMarket/assets/'

#assets path
CORNER_1 = ASSET_PATH + 'corner_1.png'
CORNER_2 = ASSET_PATH + 'corner_2.png'
CORNER_3 = ASSET_PATH + 'corner_1.png'
CORNER_4 = ASSET_PATH + 'corner_1.png'
EVENT = ASSET_PATH + 'event.png'
FREE_STOP = ASSET_PATH + 'fermata-libera.png'


#CELLS OBJECT
CELLS_DEF = {
    'ORANGE':{
        'logos': ['gled.png', 'frieskes.png', 'frio.png'],
        'value': 200,
        'color': ORANGE
    },
    'LIGHT_BLUE':{
        'logos': ['finish.png', 'dash.png', 'cuore.png'],
        'value': 280,
        'color': LIGHT_BLUE
    },
    'PINK':{
        'logos': ['zarotti.png', 'ponti.png', 'nostromo.png'],
        'value': 360,
        'color': PINK
    },
    'GREEN':{
        'logos': ['barilla.png', 'euvita.png', 'galbusera.png'],
        'value': 440,
        'color': GREEN
    },
    'RED':{
        'logos': ['lavazza.png', 'mangiaebevi.png', 'stella-artois.png'],
        'value': 500,
        'color': RED
    },
    'BLUE':{
        'logos': ['san-benedetto.png', 'pepsi.png', 'schweppes.png'],
        'value': 600,
        'color': BLUE
    },
    'YELLOW':{
        'logos': ['ibis.png', 'friendies.png', 'yoplait.png'],
        'value': 700,
        'color': YELLOW
    },
    'PURPLE':{
        'logos': ['cavicchioli.png', 'martini.png', 'galup.png'],
        'value': 800,
        'color': PURPLE
    }

}