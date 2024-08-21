class Action:
    def __init__(self, name, grid):
        self.__name = name
        self.__grid = grid

    def get_name(self):
        return self.__name
    
    def get_grid(self):
        return self.__grid