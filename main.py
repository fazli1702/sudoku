import pygame
from sudoku import *

pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sudoku')

def main():
    run = True
    board = Board(WIN)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col(pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    board.solve_gui()

        board.update()

if __name__ == '__main__':
    main()