import numpy as np
import itertools
import copy

from board import Board

def generate_line_possibilities(length, clues):
    if not clues:
        return [[0] * length]
    
    total_blocks = sum(clues)
    min_required = total_blocks + len(clues) - 1
    if min_required > length:
        return []

    def build(index, remaining_clues):
        if not remaining_clues:
            yield [0] * (length - index)
            return
        max_start = length - (sum(remaining_clues) + len(remaining_clues) - 1)
        for i in range(max_start + 1):
            prefix = [0] * i + [1] * remaining_clues[0]
            if index + len(prefix) < length:
                prefix += [0]
            for suffix in build(index + len(prefix), remaining_clues[1:]):
                yield prefix + suffix
    results = list(build(0, clues))
    return results, len(results)

def consensus_array(arrays):
    result = []
    for values in zip(*arrays):
        if -1 in values:
            result.append(-1)
        elif len(set(values)) > 1:
            result.append(-1)
        elif values[0] == 0:
            result.append(0)
        elif values[0] == 1:
            result.append(1)
        else:
            raise ValueError("Unexpected value in consensus array calculation.")
    return result

def possibility_matches_current(p, current):
    return all(c == -1 or c == p[i] for i, c in enumerate(current))

def solve_nonogram(board: Board):

    hasChangedAnything = True
    while hasChangedAnything:

        hasChangedAnything = False
        
        # iterate over the board, 
        # row by row  

        for i in range(board.size_y):
            row_clue = board.row_clues[i]
            row = board.board[i]
            
            possibilities, _ = generate_line_possibilities(board.size_x, row_clue)

            possibilities = [p for p in possibilities if possibility_matches_current(p, row)]

            if not possibilities:
                continue
           
            consensus = consensus_array(possibilities)
            
            if not np.array_equal(consensus, row):
                board.board[i] = consensus
                hasChangedAnything = True
                board.hasChanged()
        
        # column by column

        for j in range(board.size_x):
            col_clue = board.col_clues[j]
            col = board.board[:, j]
            
            possibilities, _ = generate_line_possibilities(board.size_y, col_clue)            

            possibilities = [p for p in possibilities if possibility_matches_current(p, col)]

            if not possibilities:
                continue
            
            consensus = consensus_array(possibilities)
            
            if not np.array_equal(consensus, col):
                board.board[:, j] = consensus
                hasChangedAnything = True
                board.hasChanged()

    if np.all(board.board != -1):
        return board, True
    else:
        return board, False

