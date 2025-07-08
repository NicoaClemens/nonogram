# NONOGRAM SOLVER 

Basic nonogram solver. Maybe won't work for boards that need trial and error / backtracking, not sure. Might pretend like the board is solveable and solved even if the clues contradict each other. If clues don't contradict each other but board is still unsolveable it should always return 

## HOW TO USE

Example useage of file in `/src/main.py`. 

`/src/board.py` has basic handling for the board

`/src/solver.py` has the actual solver algorithm, `solve_nonogram()`.

### txt file formats for `board.loadfile()`

examples for usage in `example_clues.txt` and `example_map.txt`

#### clue

- first line -> `<number of rows> <number of cols>`
- second line -> clues for cols; clues seperated by commas, inside clues seperated by spaces
- third line -> clues for rows; same format as aboe

#### map

simply the entries written out; one row per line, cols seperated by spaces

## TODO:
- Fix false positives
- Implement backtracking algorithm
- Implement better API/Interface
- change file storage from txt to json

