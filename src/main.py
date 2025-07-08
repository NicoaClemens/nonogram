"""

Main Entry Point to Nonogram application

"""

from board import Board
from solver import solve_nonogram

if __name__ == "__main__":

    b = Board.load_file("./example_clues.txt", type="clue")
    print(b)

    b.PRINT_AFTER_CHANGE = True
    b.SLEEP_AFTER_CHANGE = 0.05

    solution, success = solve_nonogram(b)
    if success:
        print("Solution found:")
        print(solution)
    else:
        print("No solution found.")
