import pygame

# window
WIDTH, HEIGHT = 540, 540
ROWS, COLS = 9, 9
SQUARE_SIZE = WIDTH // COLS or HEIGHT // ROWS
TIME_GAP = 50  # extend height of window to display time at bottom

# font
pygame.font.init()
def draw_text(text, font_size, x, y, colour, win):
    font = pygame.font.SysFont(None, font_size)
    text = font.render(text, True, colour)
    text_rect = text.get_rect(center=(x, y))
    win.blit(text, text_rect)

# rgb colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (105, 105, 105)
RED = (255, 0, 0)
LIGHT_RED = (255, 102, 102)   
LIGHT_GREEN = (0, 255, 127)   
LIGHT_BLUE = (178, 236, 255)

def is_valid_pos(pos):
    x, y = pos
    if 0 <= x <= WIDTH and 0 <= y <= HEIGHT:
        return True
    return False