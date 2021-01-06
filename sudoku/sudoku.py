import random

def print_board(board):
    for i in range(9):
        string = ''
        for j in range(9):
            row = board[i]
            if j == 3 or j == 6:
                string += ' | '
            string += ' ' + str(row[j]) + ' '
        print(string)
        if i == 2 or i == 5:
            print('-' * 33)
    print('*' * 33)


def find_empty(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None



def valid(board, value, row, col):
    # check row
    for i in range(9):
        if board[row][i] == value and col != i:
            return False

    #check column
    for i in range(9):
        if board[i][col] == value and row != i:
            return False

    # check box
    box_row = (row // 3) * 3
    box_col = (col // 3) * 3

    for i in range(box_row,box_row+3):
        for j in range(box_col, box_col+3):
            if board[i][j] == value and (i, j) !=  (row, col):
                return False

    return True


def solve(board):
    find = find_empty(board)

    if not find:
        return True

    row, col = find

    for i in range(1, 10):
        if valid(board, i, row, col):
            board[row][col] = i
            # print_board(board)

            if solve(board):
                return True
            
            board[row][col] = 0
    
    return False


def random_board():
    board = [[0 for i in range(9)] for j in range(9)]
    row = random.choice([True, False])   # choose between row or col to insert into board

    if row:
        random_row = list(range(1, 10))
        random.shuffle(random_row)
        board[random.randint(0, 8)] = random_row

    else:
        random_col = list(range(1, 10))
        random.shuffle(random_col)
        col_index = random.randint(0, 9)
        for row, ele in zip(board, random_col):
            row[col_index] = ele

    print('INITIAL BOARD')
    print_board(board)

    solve(board)

    print('SOLVED BOARD')
    print_board(board)

    # remove 5 -7 numbers for each row
    for row in board:
        i = random.randint(5, 7)
        cols = random.sample(list(range(9)), i)
        for col in cols:
            row[col] = 0
    
    print('CURRENT BOARD')
    print_board(board)
    return board

