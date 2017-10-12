import pygame
import sys
import random
from pygame.locals import *

# constants/ variables
FPS = 30
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
BOX_SIZE = 20
GAP_SIZE = 1

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (200, 0, 50)
GRAY = (200, 200, 200)


def main():
    global FPS_CLOCK, DISPLAY_SURF, WIDTH, HEIGHT, MINES
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    mouse_x, mouse_y = 0, 0
    pygame.display.set_caption('Minesweeper')
    DISPLAY_SURF.fill(GRAY)

    # menu()
    # pygame.time.wait(2000)
    WIDTH = 30
    HEIGHT = 16
    MINES = 99

    board = get_randomized_board()
    revealed_boxes = generate_revealed_boxes_data(False)

    # storing number of mines
    for i in range(WIDTH):
        for j in range(HEIGHT):
            if (board[i][j] != 'X'):
                board[i][j] = calculate_mines(board, i, j)

    # main game loop
    while True:
        mouse_clicked = False

        DISPLAY_SURF.fill(GRAY)
        draw_board(board, revealed_boxes)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                mouse_clicked = True

        x, y = get_box_at_pixel(mouse_x, mouse_y)
        if(x != None and y != None and not revealed_boxes[x][y] and mouse_clicked):
            revealed_boxes[x][y] = True
            if(board[x][y] == 'X'):
                game_over()
            elif(board[x][y] == 0):
                n = find_neighbours(x, y)
                reveal_boxes(revealed_boxes, n)
                while(len(n) != 0):
                    if(board[n[0][0]][n[0][1]] == 0):
                        n2 = find_neighbours(n[0][0], n[0][1])
                        for i in range(len(n2)):
                            if(revealed_boxes[n2[i][0]][n2[i][1]] == False):
                                n.append(n2[i])
                        reveal_boxes(revealed_boxes, n2)


                    n.remove(n[0])
        # redraw the screen and wait a clock tick
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def menu():
    font_obj = pygame.font.Font('freesansbold.ttf', 32)
    text_surface_obj = font_obj.render('Minesweeper', True, BLACK)
    text_rect_obj = text_surface_obj.get_rect()
    text_rect_obj.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/6)
    DISPLAY_SURF.blit(text_surface_obj, text_rect_obj)

    pygame.display.update()
    FPS_CLOCK.tick(FPS)


def select_mode():
    # pygame.draw.rect(DISPLAY_SURF, BLACK,  )
    pass


# creates randomized board with mines (1)
def get_randomized_board():
    m = MINES
    b = []
    board = []
    for x in range(WIDTH * HEIGHT):
        if m > 0:
            b.append('X')
            m = m - 1
        else:
            b.append(0)
    random.shuffle(b)
    for x in range(WIDTH):
        column = []
        for y in range(HEIGHT):
            column.append(b[0])
            del b[0]
        board.append(column)
    return board


def generate_revealed_boxes_data(val):
    revealed_boxes = []
    for i in range(WIDTH):
        revealed_boxes.append([val] * HEIGHT)
    return revealed_boxes


# returns number of mines surrounding field (x,y)
def calculate_mines(board, x, y):
    n = find_neighbours(x, y)
    count = 0
    for i in n:
        x1 = i[0]
        y1 = i[1]
        if(board[x1][y1] == 'X'):
            count = count + 1
    return count


def left_top_coords_of_box(boxx, boxy):
    left = boxx * (BOX_SIZE + GAP_SIZE)
    top = boxy * (BOX_SIZE + GAP_SIZE)
    return (left, top)


# returns box the given pixel (x,y) belongs to (none if it's a free space pixel)
def get_box_at_pixel(x, y):
    for boxx in range(WIDTH):
        for boxy in range(HEIGHT):
            left, top = left_top_coords_of_box(boxx, boxy)
            box_rect = pygame.Rect(left, top, BOX_SIZE, BOX_SIZE)
            if box_rect.collidepoint(x, y):
                return (boxx, boxy)
    return(None, None)


def draw_board(board, revealed):
    for x in range(WIDTH):
        for y in range(HEIGHT):
            left, top = left_top_coords_of_box(x, y)
            if not revealed[x][y]:
                pygame.draw.rect(DISPLAY_SURF, PINK, (left, top, BOX_SIZE, BOX_SIZE))
            else:
                if(board[x][y] != 'X'):
                    pygame.draw.rect(DISPLAY_SURF, WHITE, (left, top, BOX_SIZE, BOX_SIZE))
                    font_obj = pygame.font.Font('freesansbold.ttf', 12)
                    text_surface_obj = font_obj.render(str(board[x][y]), True, BLACK)
                    text_rect_obj = text_surface_obj.get_rect()
                    text_rect_obj.center = (left + BOX_SIZE/2, top + BOX_SIZE/2)
                    DISPLAY_SURF.blit(text_surface_obj, text_rect_obj)
                else:
                    pygame.draw.rect(DISPLAY_SURF, BLACK, (left, top, BOX_SIZE, BOX_SIZE))


def reveal_boxes(rev, n):
    for i in n:
        x1 = i[0]
        y1 = i[1]
        rev[x1][y1] = True


def find_neighbours(x, y):
    n = []
    if (x > 0):
        if (y > 0):
            n.append((x-1, y-1))
        n.append((x-1, y))
        if (y < HEIGHT - 1):
            n.append((x-1, y+1))
    if (x < WIDTH - 1):
        if (y > 0):
            n.append((x+1, y-1))
        n.append((x+1, y))
        if (y < HEIGHT - 1):
            n.append((x+1, y+1))
    if (y > 0):
        n.append((x, y-1))
    if (y < HEIGHT - 1):
        n.append((x, y+1))
    return n


def game_over():
    pass


if __name__ == '__main__':
    main()