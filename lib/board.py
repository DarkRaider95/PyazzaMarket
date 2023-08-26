import pygame
from lib.constants import *
from lib.cell import Cell
class Board:
    
    def __init__(self, enableGraphics = True):
        self.__cells = []
        #load images
        self.corner1Image = pygame.image.load(CORNER_1)
        self.corner2Image = pygame.image.load(CORNER_2)
        self.corner3Image = pygame.image.load(CORNER_3)
        self.corner4Image = pygame.image.load(CORNER_4)
        self.eventImage = pygame.image.load(EVENT)
        self.fermataLibImage = pygame.image.load(FREE_STOP)
        self.quotationImage = pygame.image.load(QUOTE_IMAGE)
        self.chanceImage = pygame.image.load(CHANCE)
        self.enableGraphics = enableGraphics

        # creating __cells
        position = 0
        #create corner1
        curr_x = WIDTH - 10 - CORNER_WIDTH
        curr_y = HEIGHT - 10 - CORNER_HEIGHT
        corner1 = Cell(None, START_TYPE, curr_x, curr_y, None, self.corner1Image, position, None, isCorner = True, angle = 0, enableGraphics = self.enableGraphics)
        self.__cells.append(corner1)
        
        #create bottom side
        curr_x, curr_y, position = self.create_side(curr_x, curr_y, ["ORANGE","LIGHT_BLUE"], self.eventImage, self.fermataLibImage, FREE_STOP_TYPE, position)
        
        #create corner2
        curr_x = curr_x-CORNER_WIDTH
        corner2 = Cell(None, STOCKS_PRIZE_TYPE, curr_x, curr_y, None, self.corner2Image, position, None, isCorner = True, angle = -90, enableGraphics = self.enableGraphics)
        self.__cells.append(corner2)
        
        #create left side
        curr_x, curr_y, position = self.create_side(curr_x, curr_y, ["PINK","GREEN"], self.eventImage, self.quotationImage, QUOTATION_TYPE, position)
        
        #create corner3
        curr_y = curr_y-CORNER_HEIGHT        
        corner3 = Cell(None, CHOOSE_STOCK_TYPE, curr_x, curr_y, None, self.corner3Image, position, None, isCorner = True, angle = 180, enableGraphics = self.enableGraphics)
        self.__cells.append(corner3)
        
        #create top side
        curr_x = curr_x + CELL_WIDTH
        curr_x, curr_y, position = self.create_side(curr_x, curr_y, ["RED","BLUE"], self.eventImage, self.chanceImage, CHANCE_TYPE, position)
        
        #create corner4
        curr_x = curr_x + CELL_WIDTH
        corner4 = Cell(None, SIX_HUNDRED_TYPE, curr_x, curr_y, None, self.corner4Image, position, None, isCorner = True, angle = 90, enableGraphics = self.enableGraphics)
        self.__cells.append(corner4)
        
        #create right side
        curr_y = curr_y+CELL_WIDTH
        curr_x, curr_y, position = self.create_side(curr_x, curr_y, ["YELLOW","PURPLE"], self.eventImage, self.quotationImage, QUOTATION_TYPE, position)

    def create_side(self, curr_x, curr_y, colors, eventImage, centralImage, centralType, position): # pragma: no cover      
        x = curr_x
        y = curr_y
        # saving the names of the __cells following the order of the __cells
        names = CELLS_DEF[colors[0]]['names'] + CELLS_DEF[colors[1]]['names']
        logos = CELLS_DEF[colors[0]]['logos'] + CELLS_DEF[colors[1]]['logos']

        for i in range(0, 9):
            x, y = Board.compute_next_coord(x, y, CELLS_DEF[colors[0]]['side'])
            position += 1
            
            if(i == 2 or i == 6): # check if it is an event cell
                cell = Cell(None, EVENTS_TYPE, x, y, None, eventImage, position, None, angle = CELLS_DEF[colors[0]]['angle'], enableGraphics = self.enableGraphics)                
            elif(i == 4): # check if it is a central cell, like free stop, quotation, chance
                cell = Cell(None, centralType, x, y, None, centralImage, position, None, angle = CELLS_DEF[colors[0]]['angle'], enableGraphics = self.enableGraphics)
            elif (i < 4): # check if it is less than 4 that means that it is the first color
                cellDef = CELLS_DEF[colors[0]]
                cell = Cell(cellDef, STOCKS_TYPE, x, y, logos.pop(0), None, position, names.pop(0), enableGraphics = self.enableGraphics)
            else: # otherwise is the second color
                # cell def defines the color, x and y are the position, than logo, image if it is a special one and position is the ordered number of the cell
                cellDef = CELLS_DEF[colors[1]]
                cell = Cell(cellDef, STOCKS_TYPE, x, y, logos.pop(0), None, position, names.pop(0), enableGraphics = self.enableGraphics) 
                
            self.__cells.append(cell)

        return x, y, position + 1
    
    @classmethod
    def compute_next_coord(cls, x: int, y: int, side: str) -> tuple[int, int]:
        if side == 'BOT':
            x = x - CELL_WIDTH
            y = y
        elif side == 'LEFT':
            x = x
            y = y - CELL_WIDTH
        elif side == 'TOP':
            x = x + CELL_WIDTH
            y = y
        else:
            x = x
            y = y + CELL_WIDTH

        return x, y

    def draw(self, screen):  # pragma: no cover
        for cell in self.__cells:
            cell.draw(screen)

    def draw_player_car(self, screen, player, playerNumber, totalPlayers):  # pragma: no cover
        cell = self.__cells[player.get_position()]
        car_x = 0
        car_y = 0

        if (cell.angle == 0):
            car_x = cell.cell_x + 5
            car_y = cell.cell_y + ((CELL_HEIGHT // totalPlayers) * playerNumber)
            player.get_car().rotate(90)
        elif(cell.angle == -90):
            car_x = cell.cell_x + CELL_HEIGHT - ((CELL_HEIGHT // totalPlayers) * (playerNumber+1))
            car_y = cell.cell_y + 5
            player.get_car().rotate(0)
        elif(cell.angle == 180):
            car_x = cell.cell_x + 5
            car_y = cell.cell_y + ((CELL_HEIGHT // totalPlayers) * playerNumber)
            player.get_car().rotate(-90)
        elif (cell.angle == 90):
            car_x = cell.cell_x + CELL_HEIGHT - ((CELL_HEIGHT // totalPlayers) * (playerNumber+1))
            car_y = cell.cell_y + 5
            player.get_car().rotate(180)
        

        player.get_car().move(car_x, car_y)
        player.get_car().draw(screen)

    def get_cell_value(self, position):  # pragma: no cover
        cell = self.__cells[position]
        return cell.get_cell_value()
    
    def get_cell(self, position):  # pragma: no cover
        return self.__cells[position]
    
    def get_availble_stocks(self):
        stocks = []
        for cell in self.__cells:
            if(cell.get_stocks() is not None and len(cell.get_stocks()) > 0):
                stocks.append(cell.get_stocks()[0])

        return stocks
    
    def get_purchasable_stocks(self, balance):
        stocks = []
        for cell in self.__cells:
            if(cell.get_stocks() is not None and 
               len(cell.get_stocks()) > 0 and 
               cell.get_stocks()[0].get_stock_value() <= balance):
                stocks.append(cell.get_stocks()[0])

        return stocks
    
    def remove_stock(self, stock):  # pragma: no cover
        self.__cells[stock.get_position()].sell_stock()

    def get_stock_if_available(self, stockPos):
        for cell in self.__cells:
            if(cell.get_stocks() is not None and len(cell.get_stocks()) > 0 and stockPos == cell.position):
                return cell.sell_stock()
            
        return None
    
    def get_cells(self):  # pragma: no cover
        return self.__cells.copy()
