import numpy as np
import random


class MineState:
    def __init__(self, game_width, game_height, numMine, grid):
        self.__status = "Playing"
        self.__currentGrid = np.ones((game_height, game_width), dtype=int) * (-2)
        self.__grid = grid
        self.mineLeft = numMine
        self.numMine = numMine
        self.game_width = game_width
        self.game_height = game_height

    def lose(self):
        self.__status = "Game Over"
    
    def win(self):
        self.__status = "Win"

    def exit(self):
        self.__status = "Exit"

    def getStatus(self):
        return self.__status
    
    def getMinePos(self):
        mines = np.array(self.numMine)
        for i in range(self.game_height):
            for j in range(self.game_width):
                if self.__currentGrid[i][j] == -3:
                    mines = np.append(mines, [j, i])

    def update(self, x, y, val):
        self.__currentGrid[y][x] = val
        print(f"Updated {x}, {y} to {val}")

    def getCurrentActions(self):
        actions = []
        for i in range(self.game_height):
            for j in range(self.game_width):
                # check if at least one of the neighbors is clicked
                if not self.grid[i][j].clicked:
                    for neighbor in self.grid[i][j].neighbors:
                        if type(neighbor) != int and neighbor.clicked:
                            actions.append((j, i))
                            break
        return actions
    
    def applyAction(self, x, y):
        pass
    
    def getGrid(self):
        return self.__grid
    
    def getCurrentGrid(self):
        return self.__currentGrid
                    