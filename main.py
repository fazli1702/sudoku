import pygame
from sudoku import *

pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT + TIME_GAP))
pygame.display.set_caption('Sudoku')

def main():
    run = True
    start_time = pygame.time.get_ticks()
    key = None
    board = Board(WIN)

    while run:
        run_time = pygame.time.get_ticks() - start_time  # in milliseconds
        selected_node = board.get_selected()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if is_valid_pos(pos):
                    row, col = board.get_row_col(pos)
                    board.select(row, col)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    board.solve_gui()

                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9

                if event.key == pygame.K_RETURN:
                    board.confirm_pencil()

                if event.key == pygame.K_BACKSPACE:
                    if selected_node != None:
                        selected_node.set_pencil(0)

        if selected_node != None and key != None:
            selected_node.set_pencil(key)
            key = None

        board.update(run_time)

if __name__ == '__main__':
    main()