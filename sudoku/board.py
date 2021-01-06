import pygame
from .constant import *
from .sudoku import find_empty, valid, random_board

class Node:
    def __init__(self, value, row, col):
        self.value = value
        self.pencil = 0
        self.row = row
        self.col = col
        self.selected = False

    def set_value(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

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

    def draw(self, win):
        '''display number on window'''
        if self.value != 0:
            x, y = self.get_coord_center()
            draw_text(str(self.value), 40, x, y, BLACK, win)
        # text = FONT.render(str(self.value), True, BLACK)
        # text_rect = text.get_rect(center=self.get_coord_center())
        # win.blit(text, text_rect)


    def highlight(self, win, colour):
        '''highlight square with light blue colour'''
        # gap = 1
        # length = SQUARE_SIZE - (gap)
        # x, y = self.get_coord_topleft()
        # x += gap
        # y += gap
        # pygame.draw.rect(win, colour, ((x, y), (length, length)))
        pygame.draw.rect(win, colour, (self.get_coord_topleft(), (SQUARE_SIZE, SQUARE_SIZE)))

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
        self.seleceted = None

    def get_node(self, row, col):
        return self.nodes[row][col]

    def get_value(self, row, col):
        return self.board[row][col]

    def set_value(self, row, col, i):
        self.board[row][col] = i

    def update(self):
        self.win.fill(WHITE)
        self.draw(self.win)
        pygame.display.update()
    
    def update_nodes(self):
        for row in range(ROWS):
            for col in range(COLS):
                node = self.get_node(row, col)
                node.set_value(self.get_value(row, col))

    def solve_gui(self):
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

    def draw(self, win):
        self.draw_grid(win)
        self.draw_nodes(win)
    