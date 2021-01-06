from sudoku import *

def test():
    for i in range(10):
        print('TEST', i)
        board = random_board()
        solve(board)

test()
