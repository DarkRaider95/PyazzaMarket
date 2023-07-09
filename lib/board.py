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
        corner1 = Cell(None, curr_x, curr_y, None, self.corner1Image, 0, position, True)
        self.cells.append(corner1)
        
        #create bottom side
        curr_x, curr_y, position = self.createSide(curr_x, curr_y, ["ORANGE","LIGHT_BLUE"], self.eventImage, self.fermataLibImage, position)
        
        #create corner2
        curr_x = curr_x-CORNER_WIDTH
        corner2 = Cell(None, curr_x, curr_y, None, self.corner2Image, -90, position, True)
        self.cells.append(corner2)
        
        #create left side
        curr_x, curr_y, position = self.createSide(curr_x, curr_y, ["PINK","GREEN"], self.eventImage, self.quotationImage, position)
        
        #create corner3
        curr_y = curr_y-CORNER_HEIGHT        
        corner3 = Cell(None, curr_x, curr_y, None, self.corner3Image, 180, position, True)
        self.cells.append(corner3)
        
        #create top side
        curr_x = curr_x + CELL_WIDTH
        curr_x, curr_y, position = self.createSide(curr_x, curr_y, ["RED","BLUE"], self.eventImage, self.chanceImage, position)
        
        #create corner4
        curr_x = curr_x + CELL_WIDTH
        corner4 = Cell(None, curr_x, curr_y, None, self.corner4Image, 90, position, True)
        self.cells.append(corner4)
        
        #create right side
        curr_y = curr_y+CELL_WIDTH
        curr_x, curr_y, position = self.createSide(curr_x, curr_y, ["YELLOW","PURPLE"], self.eventImage, self.quotationImage, position)
    
    def createSide(self, curr_x, curr_y, colors, eventImage, centralImage, position):        
        x = curr_x
        y = curr_y
        for i in range(0, 9):
            x, y = Board.computeNextCoord(x, y, CELLS_DEF[colors[0]]['side'])
            position += 1
            
            if(i == 2 or i == 6):
                cell = Cell(None, x, y, None, eventImage, CELLS_DEF[colors[0]]['angle'], position)                
            elif(i == 4):
                cell = Cell(None, x, y, None, centralImage, CELLS_DEF[colors[0]]['angle'], position)
            elif (i < 4):
                cellDef = CELLS_DEF[colors[0]]
                cell = Cell(cellDef, x, y, None, None, cellDef['angle'], position)
            else:
                cellDef = CELLS_DEF[colors[1]]
                cell = Cell(cellDef, x, y, None, None, cellDef['angle'], position)
                
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