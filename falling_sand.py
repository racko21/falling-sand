import pygame
import random
import colorsys

pygame.init()

WIDTH, HEIGHT = 400,800
CELL_SIZE = 3
BRUSH_SIZE = 15
EMPTY = (0,0,0)
UPDATE_RATE = 0.01
SPEED = 5

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling Sand Simulator")

class Grid:

    def __init__(self, width, height):

        self.rows    = int(width / CELL_SIZE) +1
        self.columns = int(height / CELL_SIZE) +1

        self.currentGrid  = [[0 for i in range(self.columns)] for j in range(self.rows)]
        self.nextGrid = [[0 for i in range(self.columns)] for j in range(self.rows)]


    def reset_grid(self):
        self.currentGrid  = [[0 for i in range(self.columns)] for j in range(self.rows)]
        self.nextGrid = [[0 for i in range(self.columns)] for j in range(self.rows)]


    def draw_cell(self, x, y, color):

        x = int(x)
        y = int(y)
        z = int(BRUSH_SIZE/2)

        for i in range(max(x-z, 1),min(x+z, self.rows-1)):
            for j in range(max(y-z, 1),min(y+z, self.columns-1)):
                if random.random() < 0.10:
                    self.currentGrid[i][j] = color


    def update_grid(self):

        for y in reversed(range(self.columns-1)):
            if random.random()>0.5:
                for x in range(self.rows-1):
                    if self.currentGrid[x][y] != 0:
                        self.update_cell(x,y)
            else:
                for x in reversed(range(self.rows-1)):
                    if self.currentGrid[x][y] != 0:
                        self.update_cell(x,y)
        self.currentGrid = self.nextGrid


    def update_cell(self, x, y):
        if y < self.columns - 1:
            color = self.currentGrid[x][y]
            if self.currentGrid[x][y+1] == 0:
                self.nextGrid[x][y] = 0
                self.nextGrid[x][y+1] = color
            elif (self.currentGrid[x-1][y+1] == 0) and (self.currentGrid[x+1][y+1] == 0):
                if random.randrange(0,100) < 50:
                    self.nextGrid[x][y] = 0
                    self.nextGrid[x+1][y+1] = color
                else:
                    self.nextGrid[x][y] = 0
                    self.nextGrid[x-1][y+1] = color
            elif self.currentGrid[x-1][y+1] == 0:
                    self.nextGrid[x][y] = 0
                    self.nextGrid[x-1][y+1] = color
            elif self.currentGrid[x+1][y+1] == 0:
                    self.nextGrid[x][y] = 0
                    self.nextGrid[x+1][y+1] = color


    def draw_grid(self):
        for x in range(1, self.rows-1):
            for y in range(self.columns-1):
                color = self.currentGrid[x][y]
                if color != 0:
                    pygame.draw.rect(WINDOW, color, (x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE))


def main():
    running = True
    clock = pygame.time.Clock()
    countdown = UPDATE_RATE
    grid = Grid(WIDTH, HEIGHT)
    hsv = 0.4

    while running:
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        WINDOW.fill(EMPTY)

        sec = clock.get_rawtime()/100
        countdown -= sec

        if countdown < 0.0:
            if pygame.mouse.get_pressed()[0] == 1:
                x, y = pygame.mouse.get_pos()
                rgb = colorsys.hsv_to_rgb(hsv, 0.6, 1)
                rgb = tuple(int(i * 255) for i in rgb)
                grid.draw_cell(x/CELL_SIZE, y/CELL_SIZE, rgb)
                hsv = hsv +0.01

            grid.update_grid()
            grid.draw_grid()
            countdown = UPDATE_RATE

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
