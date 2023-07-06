import pygame
from .constants import *
from .cell import Cell

class Board:
    
    def __init__(self):
        self.cells = []

    def initialiaze_cells(self, screen):
        #load images
        corner1Image = pygame.image.load(CORNER_1)
        corner2Image = pygame.image.load(CORNER_2)
        eventImage = pygame.image.load(EVENT)
        fermataLibImage = pygame.image.load(FREE_STOP)
        #create corner1
        curr_x = WIDTH - 10 - CORNER_WIDTH
        curr_y = HEIGHT - 10 - CORNER_HEIGHT
        corner1 = Cell(None, None, None, curr_x, curr_y, corner1Image, 0)
        self.cells.append(corner1)
        #create bottomSide
        curr_x, curr_y = self.createBottomTriplet(corner1.cell_x, corner1.cell_y, "ORANGE", 2, eventImage)
        #fermata libera        
        cell = Cell(None, None, None, curr_x-CELL_WIDTH, curr_y, fermataLibImage, 0)
        self.cells.append(cell)
        curr_x, curr_y = self.createBottomTriplet(curr_x - CELL_WIDTH, curr_y, "LIGHT_BLUE", 1, eventImage)
        #create corner2
        curr_x = curr_x-CORNER_WIDTH
        corner2 = Cell(None, None, None, curr_x, curr_y, corner2Image, 0)
        self.cells.append(corner2)

        cell = Cell(None, None, None, curr_x, curr_y-CELL_WIDTH, fermataLibImage, -90)        
        self.cells.append(cell)

    
    def createBottomTriplet(self, curr_x, curr_y, color, eventCell, eventImage):
        cellDef = CELLS_DEF[color]
        x = 0
        y = 0
        for i in range(0, 4):
            x = curr_x - CELL_WIDTH * (i + 1)
            y = curr_y
            
            #cell = Cell(cellDef.color, cellDef.value, cellDef.logos[i], x, y, None)
            if(i == eventCell):
                cell = Cell(None, None, None, x, y, eventImage, 0)
                self.cells.append(cell)
            else:
                cell = Cell(cellDef['color'], cellDef['value'], None, x, y, None, 0)
                self.cells.append(cell)

        return x, y

    def draw(self, screen):
        for cell in self.cells:
            cell.draw(screen)

    def drawPlayerCar(self, screen, cellPos, player, playerNumber, totalPlayers):
        cell = self.cells[cellPos]
        if (cellPos % 11 != 0):
            car_x = cell.cell_x + 5
            car_y = cell.cell_y + ((CELL_HEIGHT // totalPlayers) * playerNumber)
        else:
            car_x = cell.cell_x + CELL_HEIGHT // 2
            car_y = cell.cell_y + ((CELL_HEIGHT // totalPlayers) * playerNumber)

        player.car.move(car_x, car_y)
        player.car.rotate(90)
        player.car.draw(screen)