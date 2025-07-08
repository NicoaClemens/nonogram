"""


Board class for Nonogram game

"""

import numpy as np
from time import sleep

SLEEP_AFTER_CHANGE = 0 

class Board:
    """
    Board class for Nonogram game
    Represents a 2D grid where each cell can be filled or empty.
    1 = filled, 0 = empty, -1 = unknown (not yet filled or empty)
    """

    def __init__(self, size_x, size_y):
        """
        Initialize the board with given dimensions.

        :param size_x: Width of the board

        :param size_y: Height of the board
        """
        self.size_x = size_x
        self.size_y = size_y
        self.board = np.array([[-1 for _ in range(size_x)] for _ in range(size_y)])
        self.row_clues = []
        self.col_clues = []
        self.SLEEP_AFTER_CHANGE = SLEEP_AFTER_CHANGE 
        self.PRINT_AFTER_CHANGE = False

    def gen_clues(self):
        """
        Generate clues for the current board state.
        Clues are lists of integers representing the lengths of consecutive filled cells in each row and column.
        """
        if np.any(self.board == -1):
            raise ValueError("Board contains unknown cells (-1). Cannot generate clues for unknown boards.")

        self.row_clues = []
        self.col_clues = []

        for i in range(self.size_y):
            row = self.board[i]
            clues = []
            count = 0
            for val in row:
                if val == 1:
                    count += 1
                elif count > 0:
                    clues.append(count)
                    count = 0
            if count > 0:
                clues.append(count)
            self.row_clues.append(clues)
            
        for j in range(self.size_x):
            col = self.board[:, j]
            clues = []
            count = 0
            for val in col:
                if val == 1:
                    count += 1
                elif count > 0:
                    clues.append(count)
                    count = 0
            if count > 0:
                clues.append(count)
            self.col_clues.append(clues)

    def fill(self, map):
        """
        Fill the board with the given map.

        :param map: 2D list of integers (0 or 1)
        """
        if len(map) != self.size_y or any(len(row) != self.size_x for row in map):
            raise ValueError("Map size does not match board size.")
        self.board = np.array(map)
        self.size_x = len(map[0])
        self.size_y = len(map)
        self.gen_clues()
    
    def load_file(self, filename, type="clue"):
        """
        Load clues from a file.
        
        :param filename: Name of the file to load
        :param type: Type of data to load, either "clue" or "map"
        """
        with open(filename, 'r') as file:
            if type == "clue":
                self.row_clues = [list(map(int, line.split())) for line in file]
                self.col_clues = [list(map(int, line.split())) for line in file]
            elif type == "map":
                map_data = [list(map(int, line.split())) for line in file]
                self.fill(map_data)
            else:
                raise ValueError("Invalid type specified. Use 'clue' or 'map'.")
            
    def load_file(filename, type="map"):
        """
        Generates a new board from a file containing clues or a map.
        
        :param filename: Name of the file to load
        :param type: Type of data to load, either "clue" or "map"
        """

        b = Board(0, 0) 
        with open(filename, 'r') as file:
            if type == "map":
                map_data = [list(map(int, line.split())) for line in file]
                b = Board(len(map_data[0]), len(map_data))
                b.fill(map_data)
                return b
            elif type == "clue":
                """
                File format for clues:
                first line: <number of rows> <number of columns>
                second line: <row clues> (comma-separated sets of integers; each integer in a set is separated by a space)
                third line: <column clues> (same format as row clues)
                """
                first_line = file.readline().strip(" ")
                size_x, size_y = map(int, first_line.split())
                b = Board(size_x, size_y)
                b.row_clues = [list(map(int, clue.split())) for clue in file.readline().strip().split(',')]
                b.col_clues = [list(map(int, clue.split())) for clue in file.readline().strip().split(',')]
                return b

    def check_clues(self):
        """
        Check if the current board state matches the clues.
        
        :return: True if the board matches the clues, False otherwise
        """
        return self.row_clues == [self._generate_clue(row) for row in self.board] and self.col_clues == [self._generate_clue(self.board[:, col]) for col in range(self.size_x)]
    
    def hasChanged(self):
        """
        Function to be run when the board has changed. 
        """

        if self.PRINT_AFTER_CHANGE: 
            print(self)
        sleep(self.SLEEP_AFTER_CHANGE)  

    def __str__(self):
        """
        Returns a string representation of the board with row and column clues.
        Filled cell = █, Empty = ·, Unknown = space
        """
        if not self.row_clues or not self.col_clues:
            self.gen_clues()

        max_row_clues = max(len(clue) for clue in self.row_clues)
        max_col_clues = max(len(clue) for clue in self.col_clues)

        padded_col_clues = []
        for i in range(max_col_clues):
            line = []
            for clue in self.col_clues:
                if len(clue) < max_col_clues - i:
                    line.append(" ")
                else:
                    line.append(str(clue[i - (max_col_clues - len(clue))]))
            padded_col_clues.append(line)

        lines = []

        for line in padded_col_clues:
            lines.append(" " * (max_row_clues * 3) + " ".join(f"{x:>2}" for x in line))

        for row_idx, row in enumerate(self.board):
            row_clue_str = " ".join(f"{x:>2}" for x in self.row_clues[row_idx])
            row_clue_str = row_clue_str.rjust(max_row_clues * 3)
            row_cells = []
            for cell in row:
                if cell == 1:
                    row_cells.append("███")
                elif cell == 0:
                    row_cells.append(" · ")
                else:
                    row_cells.append("   ")
            lines.append(f"{row_clue_str} " + "".join(row_cells))

        return "\n".join(lines)
    
