import pygame
import random
import numpy as np
from threading import Thread

"""
Greatly inspired by ixora-0 work on Minesweeper game in Python
https://github.com/ixora-0/Minesweeper
"""


from state import MineState
from human_agent import HumanAgent
from action import Action
from tools import get_action_timed

pygame.init()

bg_color = (192, 192, 192)
grid_color = (128, 128, 128)

game_width = 9  # Change this to increase size
game_height = 9  # Change this to increase size
numMine = 10  # Number of mines
grid_size = 32  # Size of grid (WARNING: make sure to change the images dimension as well)
border = 16  # Left, Right, Bottom border
top_border = 200  # Top border
display_width = grid_size * game_width + border * 2  # Display width
display_height = grid_size * game_height + border + top_border  # Display height
gameDisplay = pygame.display.set_mode((display_width, display_height))  # Create display
timer = pygame.time.Clock()  # Create timer
pygame.display.set_caption("Minesweeper")  # S Set the caption of window

# Import files
spr_emptyGrid = pygame.image.load("Sprites/empty.png")
spr_flag = pygame.image.load("Sprites/flag.png")
spr_grid = pygame.image.load("Sprites/Grid.png")
spr_grid1 = pygame.image.load("Sprites/grid1.png")
spr_grid2 = pygame.image.load("Sprites/grid2.png")
spr_grid3 = pygame.image.load("Sprites/grid3.png")
spr_grid4 = pygame.image.load("Sprites/grid4.png")
spr_grid5 = pygame.image.load("Sprites/grid5.png")
spr_grid6 = pygame.image.load("Sprites/grid6.png")
spr_grid7 = pygame.image.load("Sprites/grid7.png")
spr_grid8 = pygame.image.load("Sprites/grid8.png")
spr_grid7 = pygame.image.load("Sprites/grid7.png")
spr_mine = pygame.image.load("Sprites/mine.png")
spr_mineClicked = pygame.image.load("Sprites/mineClicked.png")
spr_mineFalse = pygame.image.load("Sprites/mineFalse.png")


# Create global values
grid = []  # The main grid
mines = []  # Pos of the mines


# Create funtion to draw texts
def drawText(txt, s, yOff=0):
    screen_text = pygame.font.SysFont("Calibri", s, True).render(txt, True, (0, 0, 0))
    rect = screen_text.get_rect()
    rect.center = (game_width * grid_size / 2 + border, game_height * grid_size / 2 + top_border + yOff)
    gameDisplay.blit(screen_text, rect)


# Create class grid
class Grid:
    def __init__(self, x, y, type, mines=[]):
        self.x = x  # X pos of grid
        self.y = y  # Y pos of grid
        self.clicked = False  # Boolean var to check if the grid has been clicked
        self.mineClicked = False  # Bool var to check if the grid is clicked and its a mine
        self.mineFalse = False  # Bool var to check if the player flagged the wrong grid
        self.flag = False  # Bool var to check if player flagged the grid
        # Create rectObject to handle drawing and collisions
        self.rect = pygame.Rect(border + self.x * grid_size, top_border + self.y * grid_size, grid_size, grid_size)
        self.__val = type  # Value of the grid, -1 is mine
        self.__mines = mines  # List of mines around the grid
        self.neighbors = np.zeros(9, dtype=Grid)  # Neighbors of the grid, when 0 no neighbors

    # Maybe not needed
    def __int__(self):
        if self.clicked:
            return self.__val
        if self.flag:
            return -3
        else:
            return -2
        
    def __str__(self):
        if self.clicked:
            return self.__val.__str__()
        if self.flag:
            return "F"
        else:
            return "U"

    def drawGrid(self):
        # Draw the grid according to bool variables and value of grid
        if self.mineFalse:
            gameDisplay.blit(spr_mineFalse, self.rect)
        else:
            if self.clicked:
                if self.__val == -1:
                    if self.mineClicked:
                        gameDisplay.blit(spr_mineClicked, self.rect)
                    else:
                        gameDisplay.blit(spr_mine, self.rect)
                else:
                    if self.__val == 0:
                        gameDisplay.blit(spr_emptyGrid, self.rect)
                    elif self.__val == 1:
                        gameDisplay.blit(spr_grid1, self.rect)
                    elif self.__val == 2:
                        gameDisplay.blit(spr_grid2, self.rect)
                    elif self.__val == 3:
                        gameDisplay.blit(spr_grid3, self.rect)
                    elif self.__val == 4:
                        gameDisplay.blit(spr_grid4, self.rect)
                    elif self.__val == 5:
                        gameDisplay.blit(spr_grid5, self.rect)
                    elif self.__val == 6:
                        gameDisplay.blit(spr_grid6, self.rect)
                    elif self.__val == 7:
                        gameDisplay.blit(spr_grid7, self.rect)
                    elif self.__val == 8:
                        gameDisplay.blit(spr_grid8, self.rect)

            else:
                if self.flag:
                    gameDisplay.blit(spr_flag, self.rect)
                else:
                    gameDisplay.blit(spr_grid, self.rect)

    def revealGrid(self, state, depth=0):
        if self.clicked:
            return
        self.clicked = True
        if self.flag:
            self.flag = False
            state.mineLeft += 1
        state.update(self.x, self.y, self.__val)
        # Auto reveal if it's a 0
        if self.__val == 0:
            for x in range(-1, 2):
                if self.x + x >= 0 and self.x + x < game_width:
                    for y in range(-1, 2):
                        if self.y + y >= 0 and self.y + y < game_height:
                            if not state.getGrid()[self.y + y][self.x + x].clicked:
                                state.getGrid()[self.y + y][self.x + x].revealGrid(state, depth + 1)
        elif depth == 0 and self.__val == -1:
            state.lose()
            self.mineClicked = True
            # Auto reveal all mines if it's a mine
            print("Revealing all mines")
            for m in self.__mines:
                if not state.getGrid()[m[1]][m[0]].clicked and not state.getGrid()[m[1]][m[0]].flag:
                    state.getGrid()[m[1]][m[0]].revealGrid(state, depth + 1)
            # Auto flag all wrong flags
            for i in range(game_height):
                for j in range(game_width):
                    if state.getGrid()[i][j].flag and state.getGrid()[i][j].__val != -1:
                        state.getGrid()[i][j].mineFalse = True
        

    def updateValue(self, grid):
        # Update the value when all grid is generated
        if self.__val != -1:
            for x in range(-1, 2):
                if self.x + x >= 0 and self.x + x < game_width:
                    for y in range(-1, 2):
                        if self.y + y >= 0 and self.y + y < game_height:
                            if grid[self.y + y][self.x + x].__val == -1:
                                self.__val += 1

        # Set neighbors
        for x in range(-1, 2):
            if self.x + x >= 0 and self.x + x < game_width:
                for y in range(-1, 2):
                    if self.y + y >= 0 and self.y + y < game_height:
                        self.neighbors[(y + 1) * 3 + x + 1] = grid[self.y + y][self.x + x]
        # unset self
        self.neighbors[4] = 0

    def getVal(self):
        if self.clicked:
            return self.__val
        if self.flag:
            return -3
        else:
            return -2
    
    def toggleFlag(self, state):
        if self.flag:
            state.update(self.x, self.y, -2)
            state.mineLeft += 1
        else:
            state.update(self.x, self.y, -3)
            state.mineLeft -= 1
        self.flag = not self.flag
    
    def checkWin(self):
        if self.__val != -1 and not self.clicked:
            return False
        return True

def generateMines(width, height, numMine):
    mines = np.zeros((numMine, 2), dtype=int)
    for c in range(numMine):
        pos = ([random.randrange(0, width),
               random.randrange(0, height)])
        # Check if the mine is already there
        while (pos == mines).all(axis=1).any():
            pos = np.array([random.randrange(0, width),
                   random.randrange(0, height)])
        mines[c] = pos
    return mines

def generateGrid(width, height, mines):
    grid = np.zeros((height, width), dtype=Grid)
    for j in range(height):
        for i in range(width):
            if ((i, j) == mines).all(axis=1).any():
                grid[j][i] = Grid(i, j, -1, mines)
            else:
                grid[j][i] = Grid(i, j, 0)
    for j in range(height):
        for i in range(width):
            grid[j][i].updateValue(grid)
    return grid
    

def gameLoop():
    t = 0  # Set time to 0

    state = MineState(game_width, 
                      game_height, 
                      numMine, 
                      generateGrid(game_width, game_height, generateMines(game_width, game_height, numMine)))
    agent = HumanAgent()


    # Main Loop
    while state.getStatus() != "Exit":
        # Reset screen
        gameDisplay.fill(bg_color)

        # Check if won
        w = True
        for i in state.getGrid():
            for j in i:
                j.drawGrid()
                if not j.checkWin():
                    w = False
        if w and state.getStatus() != "Exit":
            state.win()

        # Draw Texts
        if state.getStatus() != "Game Over" and state.getStatus() != "Win":
            t += 1
        elif state.getStatus() == "Game Over":
            drawText("Game Over!", 50, -230)
            drawText("R to restart", 35, -180)
        else:
            drawText("You WON!", 50, -230)
            drawText("R to restart", 35, -180)
        # Draw time
        s = str(t // 30)
        screen_text = pygame.font.SysFont("Calibri", 50).render(s, True, (0, 0, 0))
        gameDisplay.blit(screen_text, (border, border))
        # Draw mine left
        screen_text = pygame.font.SysFont("Calibri", 50).render(state.mineLeft.__str__(), True, (0, 0, 0))
        gameDisplay.blit(screen_text, (display_width - border - 50, border))

        pygame.display.update()  # Update screen
        pygame.display.update()  # Update screen


        action = get_action_timed(agent, state, 1/30)
        if action:
            match action.get_name():
                case "Exit":
                    state.exit()
                case "Restart":
                    state.exit()
                    gameLoop()
                case "Flag":
                    action.get_grid().toggleFlag(state) if not action.get_grid().clicked else None
                case "Reveal":
                    # ignore if flagged
                    if action.get_grid().flag:
                        continue
                    # If player left clicked of the grid
                    action.get_grid().revealGrid(state)
                    print(f"Revealed {action.get_grid().x}, {action.get_grid().y}")
                    # Toggle flag off
                    # If it's a mine
                    if action.get_grid().getVal() == -1:
                        state.lose()
                        action.get_grid().mineClicked = True

        timer.tick(30)  # Tick fps

gameLoop()
pygame.quit()
quit()
