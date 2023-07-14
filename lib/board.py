import pygame
from .constants import *
from .cell import Cell

class Board:
    
    def __init__(self):
        self.cells = []
        #load images
        self.corner1Image = pygame.image.load(CORNER_1)
        self.corner2Image = pygame.image.load(CORNER_2)
        self.corner3Image = pygame.image.load(CORNER_3)
        self.corner4Image = pygame.image.load(CORNER_4)
        self.eventImage = pygame.image.load(EVENT)
        self.fermataLibImage = pygame.image.load(FREE_STOP)
        self.quotationImage = pygame.image.load(QUOTE_IMAGE)
        self.chanceImage = pygame.image.load(CHANCE)

    def initialiaze_cells(self):
        
        position = 0
        #create corner1
        curr_x = WIDTH - 10 - CORNER_WIDTH
        curr_y = HEIGHT - 10 - CORNER_HEIGHT
        corner1 = Cell(None, START_TYPE, curr_x, curr_y, None, self.corner1Image, 0, position, None, True)
        self.cells.append(corner1)
        
        #create bottom side
        curr_x, curr_y, position = self.createSide(curr_x, curr_y, ["ORANGE","LIGHT_BLUE"], self.eventImage, self.fermataLibImage, FREE_STOP_TYPE, position)
        
        #create corner2
        curr_x = curr_x-CORNER_WIDTH
        corner2 = Cell(None, STOCKS_PRIZE_TYPE, curr_x, curr_y, None, self.corner2Image, -90, position, None, True)
        self.cells.append(corner2)
        
        #create left side
        curr_x, curr_y, position = self.createSide(curr_x, curr_y, ["PINK","GREEN"], self.eventImage, self.quotationImage, QUOTATION_TYPE, position)
        
        #create corner3
        curr_y = curr_y-CORNER_HEIGHT        
        corner3 = Cell(None, CHOOSE_STOCK_TYPE, curr_x, curr_y, None, self.corner3Image, 180, position, None, True)
        self.cells.append(corner3)
        
        #create top side
        curr_x = curr_x + CELL_WIDTH
        curr_x, curr_y, position = self.createSide(curr_x, curr_y, ["RED","BLUE"], self.eventImage, self.chanceImage, CHANCE_TYPE, position)
        
        #create corner4
        curr_x = curr_x + CELL_WIDTH
        corner4 = Cell(None, SIX_HUNDRED_TYPE, curr_x, curr_y, None, self.corner4Image, 90, position, None, True)
        self.cells.append(corner4)
        
        #create right side
        curr_y = curr_y+CELL_WIDTH
        curr_x, curr_y, position = self.createSide(curr_x, curr_y, ["YELLOW","PURPLE"], self.eventImage, self.quotationImage, QUOTATION_TYPE, position)
    
    def createSide(self, curr_x, curr_y, colors, eventImage, centralImage, centralType, position):        
        x = curr_x
        y = curr_y
        # saving the names of the cells following the order of the cells
        names = CELLS_DEF[colors[0]]['names'] + CELLS_DEF[colors[1]]['names']
    
        for i in range(0, 9):
            x, y = Board.computeNextCoord(x, y, CELLS_DEF[colors[0]]['side'])
            position += 1
            
            if(i == 2 or i == 6): # check if it is an event cell
                cell = Cell(None, EVENTS_TYPE, x, y, None, eventImage, CELLS_DEF[colors[0]]['angle'], position, None)                
            elif(i == 4): # check if it is a central cell, like free stop, quotation, chance
                cell = Cell(None, centralType, x, y, None, centralImage, CELLS_DEF[colors[0]]['angle'], position, None)
            elif (i < 4): # check if it is less than 4 that means that it is the first color
                cellDef = CELLS_DEF[colors[0]]
                cell = Cell(cellDef, STOCKS_TYPE, x, y, None, None, cellDef['angle'], position, names.pop(0))
            else: # otherwise is the second color
                # cell def defines the color, x and y are the position, than logo, image if it is a special one and position is the ordered number of the cell
                cellDef = CELLS_DEF[colors[1]]
                cell = Cell(cellDef, STOCKS_TYPE, x, y, None, None, cellDef['angle'], position, names.pop(0)) 
                
            self.cells.append(cell)

        return x, y, position + 1
    
    def computeNextCoord(x, y, side):
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


    def draw(self, screen):
        for cell in self.cells:
            cell.draw(screen)

    def drawPlayerCar(self, screen, player, playerNumber, totalPlayers):
        cell = self.cells[player.position]
        #old_cell = self.cells[player.old_position]

        if (cell.angle == 0):
            car_x = cell.cell_x + 5
            car_y = cell.cell_y + ((CELL_HEIGHT // totalPlayers) * playerNumber)
            player.car.rotate(90)
        elif(cell.angle == -90):
            car_x = cell.cell_x + CELL_HEIGHT - ((CELL_HEIGHT // totalPlayers) * (playerNumber+1))
            car_y = cell.cell_y + 5
            player.car.rotate(0)
        elif(cell.angle == 180):
            car_x = cell.cell_x + 5
            car_y = cell.cell_y + ((CELL_HEIGHT // totalPlayers) * playerNumber)
            player.car.rotate(-90)
        elif (cell.angle == 90):
            car_x = cell.cell_x + CELL_HEIGHT - ((CELL_HEIGHT // totalPlayers) * (playerNumber+1))
            car_y = cell.cell_y + 5
            player.car.rotate(180)
        

        player.car.move(car_x, car_y)
        player.car.draw(screen)
    
    def checkIfStockCell(self, player):
        cell = self.cells[player.position]
        return cell.cellImage is not None
    
    def getCellValue(self, position):
        cell = self.cells[position]
        return cell.stock_value
    
    def getCell(self, position):
        return self.cells[position]
    
    def getAvailbleStocks(self):
        stocks = []
        for cell in self.cells:
            if(cell.stocks is not None and len(cell.stocks) > 0):
                stocks.append(cell.stocks[0])

        return stocks
    
    def getPurchasableStocks(self, balance):
        stocks = []
        for cell in self.cells:
            if(cell.stocks is not None and 
               len(cell.stocks) > 0 and 
               cell.stocks[0].stock_value <= balance):
                stocks.append(cell.stocks[0])

        return stocks
    
    def removeStock(self, stock):
        self.cells[stock.position].stocks.pop()

    def getStockIfAvailable(self, stockPos):
        for cell in self.cells:
            if(cell.stocks is not None and len(cell.stocks) > 0 and stockPos == cell.position):
                return cell.stocks.pop()
            
        return None