from ai import *
from environment import *
import time


def ai_vs_ai(ai1, ai2, reversi=None, round_num=100, verbose=0):
    # verbose = 0: Nothing
    # verbose = 1: Round number, result
    # verbose = 2: Detailed moves
    # verbose = 3: Print board
    if reversi is None:
        reversi = Reversi()
    
    ai1.ai_color = 1
    ai2.ai_color = -1

    black_win = 0
    white_win = 0
    branch_factor_list = []
    time_list = []

    for i in range(round_num):
        if verbose>0:
            print("Round",i)
        if verbose>1:
            print("Game start!")
        if verbose>2:
            reversi.print_board()
        prev_valid = True
        bf = [0, 0]
        tr = [0, 0]

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
            if reversi.current_player == 1:
                bf[0], bf[1] = bf[1]*bf[0]+len(valid_moves), bf[1]+1
                bf[0] /= bf[1]

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

            start = time.time()
            if reversi.current_player == 1:
                best_move = ai1.find_best_move(reversi, valid_moves)
                tr[0], tr[1] = tr[1] * tr[0] + time.time() - start, tr[1] + 1
                tr[0] /= tr[1]
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
        branch_factor_list.append(bf[0])
        time_list.append(tr[0])
        reversi.reset()
    
    if verbose>0:
        print("Black:White:Draw={}:{}:{}".format(black_win,white_win,round_num-black_win-white_win))
        print('Average branch factor = ', round(np.mean(branch_factor_list),2), 'time = ', round(np.mean(time_list), 5), ' s')
    
    return black_win, white_win, round_num-black_win-white_win
