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
        
        
        #create corner1
        curr_x = WIDTH - 10 - CORNER_WIDTH
        curr_y = HEIGHT - 10 - CORNER_HEIGHT
        corner1 = Cell(None, None, None, curr_x, curr_y, self.corner1Image, 0, True)
        self.cells.append(corner1)
        
        #create bottom side
        curr_x, curr_y = self.createSide(curr_x, curr_y, ["ORANGE","LIGHT_BLUE"], self.eventImage, self.fermataLibImage)
        
        #create corner2
        curr_x = curr_x-CORNER_WIDTH
        corner2 = Cell(None, None, None, curr_x, curr_y, self.corner2Image, -90, True)
        self.cells.append(corner2)
        
        #create left side
        curr_x, curr_y = self.createSide(curr_x, curr_y, ["PINK","GREEN"], self.eventImage, self.quotationImage)
        
        #create corner3
        curr_y = curr_y-CORNER_HEIGHT        
        corner3 = Cell(None, None, None, curr_x, curr_y, self.corner3Image, 180, True)
        self.cells.append(corner3)
        
        #create top side
        curr_x = curr_x + CELL_WIDTH
        curr_x, curr_y = self.createSide(curr_x, curr_y, ["RED","BLUE"], self.eventImage, self.chanceImage)
        
        #create corner4
        curr_x = curr_x + CELL_WIDTH
        corner4 = Cell(None, None, None, curr_x, curr_y, self.corner4Image, 90, True)
        self.cells.append(corner4)
        
        #create right side
        curr_y = curr_y+CELL_WIDTH
        curr_x, curr_y = self.createSide(curr_x, curr_y, ["YELLOW","PURPLE"], self.eventImage, self.quotationImage)
    
    def createSide(self, curr_x, curr_y, colors, eventImage, centralImage):        
        x = curr_x
        y = curr_y
        for i in range(0, 9):
            x, y = Board.computeNextCoord(x, y, CELLS_DEF[colors[0]]['side'])
            
            if(i == 2 or i == 6):
                cell = Cell(None, None, None, x, y, eventImage, CELLS_DEF[colors[0]]['angle'])                
            elif(i == 4):
                cell = Cell(None, None, None, x, y, centralImage, CELLS_DEF[colors[0]]['angle'])
            elif (i < 4):
                cellDef = CELLS_DEF[colors[0]]
                cell = Cell(cellDef['color'], cellDef['value'], None, x, y, None, cellDef['angle'])                
            else:
                cellDef = CELLS_DEF[colors[1]]
                cell = Cell(cellDef['color'], cellDef['value'], None, x, y, None, cellDef['angle'])
                
            self.cells.append(cell)

        return x, y
    
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
            car_x = cell.cell_x + ((CELL_WIDTH // totalPlayers) * playerNumber)
            car_y = cell.cell_y + 5
            player.car.rotate(0)
        elif(cell.angle == 180):
            car_x = cell.cell_x + 5
            car_y = cell.cell_y + ((CELL_HEIGHT // totalPlayers) * playerNumber)
            player.car.rotate(-90)
        elif (cell.angle == 90):
            car_x = cell.cell_x + ((CELL_WIDTH // totalPlayers) * playerNumber)
            car_y = cell.cell_y + 5
            player.car.rotate(180)
        

        player.car.move(car_x, car_y)
        player.car.draw(screen)
        #old_cell.draw(screen)
        #screen.blit(cell.surface, (cell.cell_x, cell.cell_y))