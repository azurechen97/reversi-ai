import pygame, sys
from pygame.locals import *
from environment import *
from ai import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

CELLWIDTH = 60
CELLHEIGHT = 60
BOARDX = 30
BOARDY = 30

def terminate():
    pygame.quit()
    sys.exit()

pygame.init()
mainClock = pygame.time.Clock()

boardImage = pygame.image.load('resources/board.png')
boardRect = boardImage.get_rect()
blackImage = pygame.image.load('resources/black.png')
blackRect = blackImage.get_rect()
whiteImage = pygame.image.load('resources/white.png')
whiteRect = whiteImage.get_rect()
frameImage = pygame.image.load('resources/frame.png')
frameRect = whiteImage.get_rect()

basicFont = pygame.font.SysFont(None, 50)

def draw_board(reversi, last_move=(-1,-1)):
    windowSurface.fill(WHITE)
    windowSurface.blit(boardImage, boardRect, boardRect)

    for i, j in reversi.black_pieces:
        rectDst = pygame.Rect(BOARDX+j*CELLWIDTH,
                              BOARDY+i*CELLHEIGHT, CELLWIDTH, CELLHEIGHT)
        windowSurface.blit(blackImage, rectDst, blackRect)
    for i, j in reversi.white_pieces:
        rectDst = pygame.Rect(BOARDX+j*CELLWIDTH,
                              BOARDY+i*CELLHEIGHT, CELLWIDTH, CELLHEIGHT)
        windowSurface.blit(whiteImage, rectDst, whiteRect)

    if last_move != (-1,-1):
        rectDst = pygame.Rect(BOARDX+last_move[1]*CELLWIDTH,
                            BOARDY+last_move[0]*CELLHEIGHT, CELLWIDTH, CELLHEIGHT)
        windowSurface.blit(frameImage, rectDst, frameRect)

reversi = Reversi()
ai = HardAI()

windowSurface = pygame.display.set_mode((boardRect.width, boardRect.height))
pygame.display.set_caption('Reversi by Aoxue and Song')

last_move = (-1,-1)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()

        if not reversi.game_end:
            if reversi.current_player == -ai.ai_color:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    valid_moves = reversi.find_valid_moves()
                    if len(valid_moves) == 0:
                        reversi.current_player = -reversi.current_player
                    else:
                        x, y = pygame.mouse.get_pos()
                        col = int((x-BOARDX)/CELLWIDTH)
                        row = int((y-BOARDY)/CELLHEIGHT)
                        reversi.make_move(row, col, hint=True, trace=False)
                        last_move = (row, col)
            else:
                valid_moves = reversi.find_valid_moves()
                if len(valid_moves) == 0:
                    reversi.current_player = -reversi.current_player
                else:
                    row, col = ai.find_best_move(reversi)
                    reversi.make_move(row, col, hint=True, trace=False)
                    last_move = (row, col)

        draw_board(reversi, last_move)
        pygame.display.flip()
        
        if reversi.is_game_over():
            reversi.game_end = True
            if len(reversi.black_pieces) > len(reversi.white_pieces):
                outputStr = "You Win!"
                reversi.winner = 1
            elif len(reversi.black_pieces) < len(reversi.white_pieces):
                outputStr = "You Lose!"
                reversi.winner = -1
            else:
                outputStr = "Draw!"
                reversi.winner = 0
            outputStr += " {}:{}".format(len(reversi.black_pieces),len(reversi.white_pieces))
            text = basicFont.render(outputStr, True, WHITE, BLACK)
            textRect = text.get_rect()
            textRect.centerx = windowSurface.get_rect().centerx
            textRect.centery = windowSurface.get_rect().centery
            windowSurface.blit(text, textRect)
            pygame.display.flip()
            pause = True
            while pause:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pause = False
                        terminate()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            reversi.reset()
                            last_move = (-1, -1)
                            draw_board(reversi, last_move)
                            pygame.display.flip()
                            pause = False
            