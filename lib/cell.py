import pygame
from lib.constants import *
from lib.stock import Stock


class Cell:
    # we should have name or position in both the cell and the stock in order to now where to put the stock in case the user will return it to the bank
    def __init__(
        self,
        cellDef,
        cellType,
        cell_x,
        cell_y,
        logo_path,
        cellImage,
        position,
        name,
        isCorner=False,
        angle=0,
        enableGraphics=True,
    ):
        self.__stocks = None
        if enableGraphics:
            self.font_stock_value = pygame.font.Font(None, 30)
            self.surface = (
                pygame.Surface((CORNER_WIDTH, CORNER_HEIGHT))
                if isCorner
                else pygame.Surface((CELL_WIDTH, CELL_HEIGHT))
            )
            if cellDef is not None:
                logo_path = LOGOS_DIR + logo_path
                logo = pygame.image.load(logo_path) # aggiungere path completo
                self.__logo = pygame.transform.scale(logo, (CELL_LOGO_WIDTH, CELL_LOGO_HEIGHT))
                cell_color_x = 0
                self.__cell_color_y = (
                    CELL_HEIGHT - CELL_COLOR_HEIGHT
                )
                self.__color_rect = pygame.Rect(
                    cell_color_x, self.__cell_color_y, CELL_COLOR_WIDTH, CELL_COLOR_HEIGHT
                )
                self.__cell_rect = pygame.Rect(
                    0, 0, CELL_WIDTH, CELL_HEIGHT
                )
                self.__scudi_text = self.font_stock_value.render("SCUDI", True, BLACK)
                self.__scudi_x = (CELL_WIDTH - (CELL_WIDTH // 2)) - (self.__scudi_text.get_width() // 2)
                self.__scudi_y = self.__cell_color_y - self.__scudi_text.get_height() - 10
                self.__price_updated = True # at the beginning is equal to true in order to do the first render
        if cellDef is not None:
            self.color = cellDef["color"]
            self.__original_value = cellDef["value"]
            self.__new_value = self.__original_value
            self.__stocks = []
            for _ in range(0, 2):
                self.__stocks.append(Stock(cellDef, position, name, logo_path, enableGraphics))
            self.__stockIndex = cellDef["index"]
            self.angle = cellDef["angle"]
        else:
            self.angle = angle
        self.cell_x = cell_x
        self.cell_y = cell_y
        self.cellImage = cellImage
        self.cellType = cellType
        self.position = position

    def draw(self, screen):
        # if it's not a corner draw a cell
        if self.cellImage is None:
            self.drawCell(screen)
        else:
            self.drawCellImage(screen)

    def drawCell(self, screen):
        # Draw stock and spaces for logo and color
        logo_x = 2 
        logo_y = 5
        pygame.draw.rect(self.surface, WHITE, self.__cell_rect)
        self.surface.blit(self.__logo, (logo_x, logo_y))
        pygame.draw.rect(self.surface, self.color, self.__color_rect)

        # Draw stock price
        if self.__price_updated:
            self.__stock_price = self.font_stock_value.render(str(self.__new_value), True, BLACK)
            self.__price_x = (CELL_WIDTH - (CELL_WIDTH // 2)) - (self.__stock_price.get_width() // 2)
            self.__price_y = self.__cell_color_y - self.__stock_price.get_height() - 30
            self.__price_updated = False
        self.surface.blit(self.__stock_price, (self.__price_x, self.__price_y))

        self.surface.blit(self.__scudi_text, (self.__scudi_x, self.__scudi_y))
        surfaceRotated = None

        if self.angle != 0:
            surfaceRotated = pygame.transform.rotate(self.surface, self.angle)
        if surfaceRotated is not None:
            screen.blit(surfaceRotated, (self.cell_x, self.cell_y))
        else:
            screen.blit(self.surface, (self.cell_x, self.cell_y))

    def drawCellImage(self, screen):
        # Disponi l'immagine sulla finestra
        self.surface.blit(self.cellImage, (0, 0))

        surfaceRotated = None
        if self.angle != 0:
            surfaceRotated = pygame.transform.rotate(self.surface, self.angle)

        if surfaceRotated is not None:
            screen.blit(surfaceRotated, (self.cell_x, self.cell_y))
        else:
            screen.blit(self.surface, (self.cell_x, self.cell_y))

    def get_cell_value(self):
        return self.__new_value

    def get_stocks(self):
        if self.__stocks is None:
            return None
        return self.__stocks.copy()

    def updateCellValue(self, value):
        self.__price_updated = True
        self.__new_value = value

    def get_index(self):
        return self.__stockIndex

    def sell_stock(self):
        if self.__stocks is None:
            return None
        return self.__stocks.pop()

    def add_stock(self, stock):
        if self.__stocks is not None:
            self.__stocks.append(stock)
