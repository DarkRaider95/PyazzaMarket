import pygame
from .constants import *
from .stock import Stock

class Cell:
    # we should have name or position in both the cell and the stock in order to now where to put the stock in case the user will return it to the bank
    def __init__(self, cellDef, cell_x, cell_y, logo, cellImage, angle, position, name, isCorner = False):
        if(cellDef is not None):
            self.color = cellDef['color']
            self.stock_value = cellDef['value']
            self.logo = logo
            self.stocks = Cell.initialize_stock(cellDef, position, name)
            self.font_stock_value = pygame.font.Font(None, 30)            
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.cellImage = cellImage
        self.surface = pygame.Surface((CORNER_WIDTH, CORNER_HEIGHT)) if isCorner else pygame.Surface((CELL_WIDTH, CELL_HEIGHT))
        self.angle = angle
        #self.position = position
        

    def initialize_stock(cellDef, position, name):
        stocks = []
        for _ in range(0,2):
            stocks.append(Stock(cellDef, position, name))

        return stocks


    def draw(self, screen):
        #if it's not a corner draw a cell
        if(self.cellImage is None):
            self.drawCell(screen)
        else:
            self.drawCellImage(screen)

    def drawCell(self, screen):
        #Draw stock and spaces for logo and color
        logo_x = 2#self.cell_x + 2
        logo_y = 5#self.cell_y + 5
        cell_color_x = 0#self.cell_x
        cell_color_y = CELL_HEIGHT - CELL_COLOR_HEIGHT#self.cell_y + CELL_HEIGHT - CELL_COLOR_HEIGHT
        cell_rect = pygame.Rect(0, 0, CELL_WIDTH, CELL_HEIGHT)#pygame.Rect(self.cell_x, self.cell_y, CELL_WIDTH, CELL_HEIGHT)
        logorect = pygame.Rect(logo_x, logo_y, CELL_LOGO_WIDTH, CELL_LOGO_HEIGHT)
        colorrect = pygame.Rect(cell_color_x, cell_color_y, CELL_COLOR_WIDTH, CELL_COLOR_HEIGHT)
        pygame.draw.rect(self.surface, WHITE, cell_rect)
        pygame.draw.rect(self.surface, BLACK, logorect)
        pygame.draw.rect(self.surface, self.color, colorrect)

        #Draw stock price
        stock_price = self.font_stock_value.render("  "+ str(self.stock_value) + "\nSCUDI", True, BLACK)
        price_x = (CELL_WIDTH - (CELL_WIDTH // 2)) - (stock_price.get_width() // 2)
        price_y = cell_color_y - stock_price.get_height() - 10
        self.surface.blit(stock_price, (price_x, price_y))

        surfaceRotated = None

        if(self.angle != 0):        
            surfaceRotated = pygame.transform.rotate(self.surface, self.angle)
            
        if(surfaceRotated is not None):
            screen.blit(surfaceRotated, (self.cell_x, self.cell_y))
        else:
            screen.blit(self.surface, (self.cell_x, self.cell_y))

    def drawCellImage(self, screen):
        # Disponi l'immagine sulla finestra
        self.surface.blit(self.cellImage, (0, 0))
        
        surfaceRotated = None
        if(self.angle != 0):            
            surfaceRotated = pygame.transform.rotate(self.surface, self.angle)
            
        if(surfaceRotated is not None):
            screen.blit(surfaceRotated, (self.cell_x, self.cell_y))
        else:
            screen.blit(self.surface, (self.cell_x, self.cell_y))