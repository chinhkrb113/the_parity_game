import pygame, sys
import numpy
import random
import time
import button

# ---------
# CONSTANTS
# ---------
WIDTH = 600
HEIGHT = 600
SQUARE_SIZE = 30
# BOARD_ROWS = 3
# BOARD_COLS = 3

input_rect = pygame.Rect(200, 200, 140, 32)
color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('chartreuse4')
color = color_passive
clock = pygame.time.Clock()

# rgb: red green blue
RED = (255, 0, 0)
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
original_grid_element_color = (52, 31, 151)

# ------
# SCREEN
# ------
pygame.init()

d = numpy.array([[-1, 0], [0, -1]])

# basic font for user typed
base_font = pygame.font.Font(None, 32)

input_rect = pygame.Rect(100, 40, 140, 32)
color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('chartreuse4')
color = color_passive
clock = pygame.time.Clock()

# it will display on screen

def sizeMatrix():
    user_text = ''
    screen = pygame.display.set_mode([300, 170])

    active = False
    # load button images
    start_img = pygame.image.load('start_btn.png').convert_alpha()
    exit_img = pygame.image.load('exit_btn.png').convert_alpha()

    # create button instances
    start_button = button.Button(60, 100,start_img, 0.3)
    exit_button = button.Button(170, 100,exit_img,  0.3)

    label = base_font.render("Size of matrix", True, (color_passive))

    while True:
        for event in pygame.event.get():

            # if user types QUIT then the screen will close
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False

            if event.type == pygame.KEYDOWN:

                # Check for backspace
                if event.key == pygame.K_BACKSPACE:

                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]

                # Unicode standard is used for string
                # formation
                else:
                    user_text += event.unicode

        # it will set background color of screen
        screen.fill((BG_COLOR))

        screen.blit(label, (0, 0))

        if start_button.draw(screen):
            print('START')

            return int(user_text)
        if exit_button.draw(screen):
            pygame.quit()
            sys.exit()

        if active:
            color = color_active
        else:
            color = color_passive

        # draw rectangle and argument passed which should
        # be on screen
        pygame.draw.rect(screen, color, input_rect)

        text_surface = base_font.render(user_text, True, (255, 255, 255))

        # render at position stated in arguments
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        # set width of textfield so that text cannot get
        # outside of user's text input
        input_rect.w = max(100, text_surface.get_width() + 10)

        # display.flip() will update only a portion of the
        # screen to updated, not full area
        pygame.display.flip()

        # clock.tick(60) means that for every second at most
        # 60 frames should be passed.
        clock.tick(60)


def choose():
    labelHowToWin = return_result()
    screen = pygame.display.set_mode([580, 150])

    active = False
    # load button images
    start_img = pygame.image.load('start_btn.png').convert_alpha()
    exit_img = pygame.image.load('exit_btn.png').convert_alpha()

    # create button instances
    start_button = button.Button(190, 90, start_img, 0.3)
    exit_button = button.Button(300, 90, exit_img, 0.3)

    label1 = base_font.render(labelHowToWin, True, (color_passive))
    label2 = base_font.render( "Wanna go first? YES or NO? ", True, (color_passive))
    while True:
        for event in pygame.event.get():

            # if user types QUIT then the screen will close
            if event.type == pygame.QUIT:
                pygame.quit()


        # it will set background color of screen
        screen.fill((BG_COLOR))

        screen.blit(label1, (0, 10))
        screen.blit(label2, (130,50))

        if start_button.draw(screen):
            return 1


        if exit_button.draw(screen):
            return 0


        # display.flip() will update only a portion of the
        # screen to updated, not full area
        pygame.display.flip()

        # n = int(user_text)

        # clock.tick(60) means that for every second at most
        # 60 frames should be passed.
        clock.tick(60)


def generate_data():
    file = open("data.txt", "w")

    file.write(str(n))
    for i in range(n):
        file.write("\n")
        for j in range(n):
            file.write(str(random.choice(range(2))) + " ")
    file.close()


def get_data():
   global n, nrow, ncol, A
   file = open("data.txt", "r")
   n = int(file.readline())
   nrow = ncol = n
   A = numpy.zeros([n + 1, n + 1], dtype=int)
   for i in range(1, n + 1):
      line = file.readline().split()
      for j in range(1, n + 1):
         A[i][j] = int(line[j - 1])
   file.close()


def initialize():
   global S
   S = numpy.zeros([n + 1, n + 1], dtype=int)
   for i in range(1, n + 1):
      for j in range(1, n + 1):
         S[i][j] = S[i - 1][j] + S[i][j - 1] - S[i - 1][j - 1] + A[i][j]


def get_move(i, j):
    move = []
    if i == 0 or j == 0:
        return []
    for x in range(2):
        if (S[i][j] - S[i + d[x][0]][j + d[x][1]]) % 2 == 0:
            move.append(x)
    return move


def dynamic_programming():
    global R
    R = numpy.zeros([n + 1, n + 1], dtype=int)
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            move = get_move(i, j)
            for x in move:
                R[i][j] = max(R[i][j], 1 - R[i + d[x][0]][j + d[x][1]])


def return_result():
    return (
        " The player who goes first has a strategy to always win."
        if R[n][n] == 1
        else "        The first player has no strategy to always win."
    )


def take_move(player, x):
    global nrow, ncol
    print(
        "Computer" if player == 0 else "Player",
        ": delete last",
        "row" if x == 0 else "column",
    )
    nrow += d[x][0]
    ncol += d[x][1]


def computer_move(win):
    w = n * SQUARE_SIZE + 2 * SQUARE_SIZE
    labelComputer1  = base_font.render("This is computer's turn ", True, (color_passive))
    win.blit(labelComputer1,(w ,40))

    move = get_move(nrow, ncol)
    lb2 = "Avaiable move: " + str(move)
    labelComputer2 = base_font.render(lb2, True, color_passive)
    win.blit(labelComputer2,(w ,90))

    labelPlayerWin = base_font.render("Game over, player win", True,(255,0,0))
    if move == []:
        win.blit(labelPlayerWin,(w ,140))
        pygame.display.update()
        time.sleep(10)
        sys.exit()

    pygame.display.update()

    for x in move:
        if R[nrow + d[x][0]][ncol + d[x][1]] == 0:
            take_move(0, x)
            return
    for x in move:
        take_move(0, x)
        return


def player_move(win):
    w = n * SQUARE_SIZE + 2 * SQUARE_SIZE

    labelPlayer1 = base_font.render("This is player's turn", True,(color_passive))
    win.blit(labelPlayer1,(w ,40))

    move = get_move(nrow, ncol)
    label2 = "Avaiable move: " + str(move)
    labelPlayer2 = base_font.render(label2,True,color_passive)
    win.blit(labelPlayer2,(w ,90))

    # load button images
    start_img = pygame.image.load('start_btn.png').convert_alpha()
    exit_img = pygame.image.load('exit_btn.png').convert_alpha()
    start_button = button.Button(w + 40, 140, start_img, 0.3)
    exit_button = button.Button(w + 140, 140, exit_img, 0.3)
    labelComputerWin = base_font.render("Game over, computer win", True, (255,0,0))
    pygame.display.update()
    if move == []:
        win.blit(labelComputerWin,(w ,140))
        pygame.display.update()
        time.sleep(10)
        sys.exit()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if len(move) == 2:

            # create button instances
            start_button = button.Button(w + 40, 140, start_img, 0.3)
            exit_button = button.Button(w + 140, 140, exit_img, 0.3)
            if start_button.draw(win)== True:
                return take_move(1, 0)

            if exit_button.draw(win) == True:
                return take_move(1, 1)

        if len(move) == 1 and move[0] == 0:
            start_button = button.Button(w + 40, 140, start_img, 0.3)
            if start_button.draw(win) == True:
                return take_move(1, 0)

        if len(move) == 1 and move[0] == 1:
            exit_button = button.Button(w + 140, 140, exit_img, 0.3)
            if exit_button.draw(win) == True:

                return take_move(1, 1)
        pygame.display.update()


def game(p,win):
    if p == 0:
        computer_move(win)
        time.sleep(2)
    else:
        player_move(win)
        time.sleep(2)


def draw():
    sub = int(SQUARE_SIZE / 2)
    myfont = pygame.font.SysFont('Comic Sans MS', sub)

    w = nrow * SQUARE_SIZE + 2 * SQUARE_SIZE
    h = ncol * SQUARE_SIZE + 2 * SQUARE_SIZE


    for x in range(0, ncol +1):
        pygame.draw.line(win, (0, 0, 0), (SQUARE_SIZE + SQUARE_SIZE * x, SQUARE_SIZE),
                         (SQUARE_SIZE + SQUARE_SIZE * x, w - SQUARE_SIZE), 2)
    for y in range(0, nrow + 1):
        pygame.draw.line(win, (0, 0, 0), (SQUARE_SIZE, SQUARE_SIZE + SQUARE_SIZE * y),
                         (h - SQUARE_SIZE, SQUARE_SIZE + SQUARE_SIZE * y), 2)
    for i in range(1, nrow+1):
        for j in range(1, ncol+1):
            value = myfont.render(str(A[i][j]), True, original_grid_element_color)
            win.blit(value, ((j) * SQUARE_SIZE + SQUARE_SIZE / 2  - sub/4, (i) * SQUARE_SIZE+SQUARE_SIZE / 2 - sub/2 -2 ))


if __name__ == "__main__":
    n = sizeMatrix()
    generate_data()
    get_data()
    initialize()
    dynamic_programming()
    p = choose()

    pygame.init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        win = pygame.display.set_mode((n * SQUARE_SIZE + 2 * SQUARE_SIZE + 300,
                                           n * SQUARE_SIZE + 2 * SQUARE_SIZE))
        pygame.display.set_caption("The Parity Game")

        win.fill(BG_COLOR)

        draw()
        pygame.display.update()

        game(p, win)
        pygame.display.update()
        p = 1 - p