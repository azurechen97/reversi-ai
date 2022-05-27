from ai import *
from environment import *
import random

def ai_vs_ai(ai1, ai2, reversi=None, round_num=100, random_turn=0, verbose=0):
    # verbose = 0: Nothing
    # verbose = 1: Round number, result
    # verbose = 2: Detailed moves
    # verbose = 3: Print board
    if reversi is None:
        reversi = Reversi()

    black_win = 0
    white_win = 0

    for i in range(round_num):
        if random_turn>0:
            randomize_board(reversi, turn=random_turn)
        if verbose>0:
            print("Round",i)
        if verbose>1:
            print("Game start!")
        if verbose>2:
            reversi.print_board()
        prev_valid = True
        while True:
            if len(reversi.black_pieces)+len(reversi.white_pieces) >= 64:
                reversi.game_over(hint=verbose>0)
                break
            
            if verbose > 1:
                if reversi.current_player == 1:
                    print("Black's turn!")
                else:
                    print("White's turn!")

            valid_moves = reversi.find_valid_moves()
            if len(valid_moves) == 0:
                if verbose > 1:
                    print("No valid move!")
                if not prev_valid:
                    reversi.game_over(hint=verbose>0)
                    break
                prev_valid = False
                reversi.current_player = -reversi.current_player
                continue
            prev_valid = True

            if reversi.current_player == 1:
                best_move = ai1.find_best_move(reversi, valid_moves)
            else:
                best_move = ai2.find_best_move(reversi, valid_moves)

            reversi.make_move(
                best_move[0], best_move[1], verbose > 1, verbose > 2)
            if verbose > 1:
                print("{} plays at ({},{}).".format(
                    "Black" if reversi.current_player == -1 else "White", best_move[0], best_move[1]))
        if reversi.winner == 1:
            black_win += 1
        elif reversi.winner == -1:
            white_win += 1
        reversi.reset()
    
    if verbose>0:
        print("Black:White:Draw={}:{}:{}".format(black_win,white_win,round_num-black_win-white_win))
    
    return black_win, white_win, round_num-black_win-white_win

def randomize_board(reversi, turn=2):
    prev_valid = True
    for _ in range(turn):
        if len(reversi.black_pieces)+len(reversi.white_pieces) >= 64:
            reversi.game_over(hint=False)
            break

        valid_moves = reversi.find_valid_moves()
        if len(valid_moves) == 0:
            if not prev_valid:
                reversi.game_over(hint=False)
                break
            prev_valid = False
            reversi.current_player = -reversi.current_player
            continue
        prev_valid = True

        best_move = random.choice(list(valid_moves.keys()))

        reversi.make_move(
            best_move[0], best_move[1], False, False)
    return reversi

def shuffle_two_lists(a,b):
    c = list(zip(a, b))
    random.shuffle(c)
    a, b = zip(*c)
    return a, b
