from ai import *
from environment import *


def ai_vs_ai(ai1, ai2, reversi=None, round=100, verbose=False):
    if reversi is None:
        reversi = Reversi()

    
    if reversi.game_end:
        reversi.game_over()
    else:
        print("Game start!")
        reversi.print_board()
        prev_valid = True
        while True:
            if len(reversi.black_pieces)+len(reversi.white_pieces) >= 64:
                reversi.game_over()
                break

            if reversi.current_player == 1:
                print("Black's turn!")
            else:
                print("White's turn!")

            valid_moves = reversi.find_valid_moves()
            if len(valid_moves) == 0:
                print("No valid move!")
                if not prev_valid:
                    reversi.game_over()
                    break
                prev_valid = False
                reversi.current_player = -reversi.current_player
                continue
            prev_valid = True

            if reversi.current_player == self.ai_color:
                best_move = self.find_best_move(reversi, valid_moves)
                reversi.make_move(best_move[0], best_move[1])
            else:
                print("Enter your move (i j) or command (pause/stop/hint):")
                command = input()
                try:
                    p = list(map(int, command.split()))
                    if len(p) == 2:
                        reversi.make_move(p[0], p[1])
                    else:
                        print("Need 2 numbers!")
                except:
                    if command == 'hint':
                        print(valid_moves)
                    elif command == 'stop':
                        reversi.game_over()
                        break
                    elif command == 'pause':
                        break
                    else:
                        print("Not numbers!")
