import pygame
from .constant import *
from .sudoku import find_empty, valid, random_board, solve
from copy import deepcopy

class Node:
    def __init__(self, value, row, col):
        self.value = value
        self.pencil = 0
        self.row = row
        self.col = col
        self.selected = False

    def __repr__(self):
        return str(self.value)

    def get_value(self):
        return self.value

    def get_pencil(self):
        return self.pencil

    def set_value(self, value):
        self.value = value

    def set_pencil(self, pencil):
        self.pencil = pencil

    def set_selected(self, select):
        self.selected = select

    def get_pos(self):
        return (self.row, self.col)

    def get_coord_topleft(self):
        '''return coordinate of top left of square'''
        x = self.col * SQUARE_SIZE
        y = self.row * SQUARE_SIZE
        return (x, y)

    def get_coord_center(self):
        '''return coordinate of center of square'''
        x = self.col * SQUARE_SIZE + SQUARE_SIZE // 2
        y = self.row * SQUARE_SIZE + SQUARE_SIZE // 2
        return (x, y)

    def highlight(self, win, colour):
        '''highlight square with light blue colour'''
        pygame.draw.rect(win, colour, (self.get_coord_topleft(), (SQUARE_SIZE, SQUARE_SIZE)))

    def draw(self, win):
        '''display number on window'''
        if self.selected:
            self.highlight(win, LIGHT_BLUE)

        if self.pencil != 0 and self.value == 0:  # draw pencil number
            gap_x, gap_y = 10, 15
            x, y = self.get_coord_topleft()
            draw_text(str(self.pencil), 30, x+gap_x, y+gap_y, GREY, win)

        elif self.value != 0:   # draw value
            x, y = self.get_coord_center()
            draw_text(str(self.value), 40, x, y, BLACK, win)

    def draw_change(self, win, is_valid):
        '''highlight box red/green when solving board (gui)'''
        if is_valid:
            self.highlight(win, LIGHT_GREEN)
        else:
            self.highlight(win, LIGHT_RED)

        self.draw(win)



class Board:
    def __init__(self, win):
        self.board = random_board()
        self.nodes = [[Node(0, row, col) for col in range(COLS)] for row in range(ROWS)]
        self.update_nodes()
        self.win = win
        self.selected = None

    def get_node(self, row, col):
        return self.nodes[row][col]

    def get_value(self, row, col):
        return self.board[row][col]

    def get_selected(self):
        return self.selected

    def get_row_col(self, pos):
        x, y = pos
        row = y // SQUARE_SIZE
        col = x // SQUARE_SIZE
        return row, col

    def set_value(self, row, col, i):
        self.board[row][col] = i

    def update(self, time):
        self.win.fill(WHITE)
        self.draw(self.win)
        self.draw_time(self.win, time)
        pygame.display.update()
    
    def update_nodes(self):
        '''chnage all node value based on self.board'''
        for row in range(ROWS):
            for col in range(COLS):
                node = self.get_node(row, col)
                node.set_value(self.get_value(row, col))

    def unselect_all(self):
        '''set all node.selected to false'''
        for row in self.nodes:
            for node in row:
                node.set_selected(False)


    def select(self, row, col):
        self.unselect_all()
        node = self.get_node(row, col)
        node.set_selected(True)
        self.selected = node

    def confirm_pencil(self):
        node = self.selected
        board = deepcopy(self.board)
        row, col = node.get_pos()
        is_valid = False

        if valid(board, node.get_pencil(), row, col):
            board[row][col] = node.get_pencil()
            if solve(board):
                self.set_value(row, col, node.get_pencil())
                self.update_nodes()
                is_valid = True

        if not is_valid:
            node.set_pencil(0)
            self.draw_wrong()



    def solve_gui(self):
        self.unselect_all()
        self.update_nodes()

        find = find_empty(self.board)
        if not find:
            return True

        row, col = find
        delay = 100
        for i in range(1, 10):
            if valid(self.board, i, row, col):
                self.set_value(row, col, i)
                self.update_nodes()
                node = self.get_node(row, col)
                node.draw_change(self.win, True)
                self.draw_grid(self.win)
                pygame.display.update()
                pygame.time.delay(delay)

                if self.solve_gui():
                    return True

                self.set_value(row, col, 0)
                self.update_nodes()
                node = self.get_node(row, col)
                node.draw_change(self.win, False)
                self.draw_grid(self.win)
                pygame.display.update()
                pygame.time.delay(delay)






    def draw_grid(self, win):
        # draw rows / horizontal line
        for row in range(ROWS + 1):
            width = 3 if row % 3 == 0 else 1
            y = row * SQUARE_SIZE
            pygame.draw.line(win, BLACK, (0, y), (WIDTH, y), width)

        # draw col / vertical line
        for col in range(COLS + 1):
            width = 3 if col % 3 == 0 else 1
            x = col * SQUARE_SIZE
            pygame.draw.line(win, BLACK, (x, 0), (x, HEIGHT), width)

    def draw_nodes(self, win):
        '''display numbers on board'''
        for row in self.nodes:
            for node in row:
                node.draw(win)

    def draw_time(self, win, time):
        '''display time on the bottom of board'''
        time = self.format_time(time)
        draw_text(time, 40, WIDTH - SQUARE_SIZE, HEIGHT + TIME_GAP // 2, BLACK, win)

    def draw_wrong(self):
        '''display wrong text at botton of board'''
        draw_text('WRONG', 40, SQUARE_SIZE, HEIGHT + TIME_GAP // 2, RED, self.win)
        pygame.display.update()
        pygame.time.delay(1000)

    def format_time(self, time):
        time = time // 1000
        s = time % 60
        m = time // 60
        return '{}:{:02}'.format(m, s)

    def draw(self, win):
        self.draw_nodes(win)
        self.draw_grid(win)
    