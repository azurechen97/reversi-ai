import pygame, sys
from pygame.locals import *
from environment import *
from ai import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 40

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

basicFont = pygame.font.SysFont(None, 50)

reversi = Reversi()
ai = HardAI()

windowSurface = pygame.display.set_mode((boardRect.width, boardRect.height))
pygame.display.set_caption('Reversi by Aoxue and Song')

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
                        reversi.make_move(row, col, hint=False, trace=False)
            else:
                valid_moves = reversi.find_valid_moves()
                if len(valid_moves) == 0:
                    reversi.current_player = -reversi.current_player
                else:
                    row, col = ai.find_best_move(reversi)
                    reversi.make_move(row, col, hint=False, trace=False)
        
        windowSurface.fill(WHITE)
        windowSurface.blit(boardImage, boardRect, boardRect)

        for row, col in reversi.black_pieces:
            rectDst = pygame.Rect(BOARDX+col*CELLWIDTH,
                                  BOARDY+row*CELLHEIGHT, CELLWIDTH, CELLHEIGHT)
            windowSurface.blit(blackImage, rectDst, blackRect)
        for row, col in reversi.white_pieces:
            rectDst = pygame.Rect(BOARDX+col*CELLWIDTH,
                                  BOARDY+row*CELLHEIGHT, CELLWIDTH, CELLHEIGHT)
            windowSurface.blit(whiteImage, rectDst, whiteRect)
        
        if reversi.is_game_over():
            reversi.game_end = True
            if len(reversi.black_pieces) > len(reversi.white_pieces):
                outputStr = "Black Wins!"
                reversi.winner = 1
            elif len(reversi.black_pieces) < len(reversi.white_pieces):
                outputStr = "White Wins!"
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

        pygame.display.update()
        mainClock.tick(FPS)