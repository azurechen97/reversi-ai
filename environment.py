import numpy as np

class Reversi:
    def __init__(self, init_black={(3, 4), (4, 3)}, init_white={(3, 3), (4, 4)}) -> None:
        self.reset(init_black, init_white)
    
    def reset(self, init_black={(3, 4), (4, 3)}, init_white={(3, 3), (4, 4)}):
        self.board = np.zeros((8, 8), dtype=np.int8)
        self.black_pieces = init_black.copy()
        self.white_pieces = init_white.copy()
        self.refresh_board()
        self.current_player = 1
        self.game_end = False

    def refresh_board(self):
        for p in self.black_pieces:
            self.board[p] = 1
        for p in self.white_pieces:
            self.board[p] = -1
        return self.board

    def print_board(self):
        print(' '.join([' ']+[str(i) for i in range(8)]))
        for i in range(8):
            print(str(i), end=' ')
            for j in range(8):
                if self.board[i,j] == 1:
                    print('●', end=' ')
                elif self.board[i,j] == -1:
                    print('○', end=' ')
                else:
                    print(' ', end=' ')
            print()

    def is_valid_move(self,i,j,can_flip=set(),hint=True):
        # out of bound
        if i >= 8 or i < 0 or j >= 8 or j < 0:
            if hint:
                print("Out of bound!")
            return False
        # overlapping
        if self.board[i,j]!=0:
            if hint:
                print("Overlapping!")
            return False
        # cannot flip anything
        # 180
        l = []
        for k in range(1,j+1):
            if self.board[i,j-k] == -self.current_player:
                l.append((i, j-k))
            else:
                if self.board[i,j-k] == self.current_player:
                    can_flip.update(l)
                break

        # 135
        l = []
        for k in range(1, min(i+1,j+1)):
            if self.board[i-k,j-k] == -self.current_player:
                l.append((i-k, j-k))
            else:
                if self.board[i-k,j-k] == self.current_player:
                    can_flip.update(l)
                break

        # 90
        l = []
        for k in range(1, i+1):
            if self.board[i-k,j] == -self.current_player:
                l.append((i-k, j))
            else:
                if self.board[i-k,j] == self.current_player:
                    can_flip.update(l)
                break

        # 45
        l = []
        for k in range(1, min(i+1, 8-j)):
            if self.board[i-k,j+k] == -self.current_player:
                l.append((i-k, j+k))
            else:
                if self.board[i-k,j+k] == self.current_player:
                    can_flip.update(l)
                break

        # 0
        l = []
        for k in range(1, 8-j):
            if self.board[i,j+k] == -self.current_player:
                l.append((i, j+k))
            else:
                if self.board[i, j+k] == self.current_player:
                    can_flip.update(l)
                break

        # -45
        l = []
        for k in range(1, min(8-i, 8-j)):
            if self.board[i+k,j+k] == -self.current_player:
                l.append((i+k, j+k))
            else:
                if self.board[i+k, j+k] == self.current_player:
                    can_flip.update(l)
                break

        # -90
        l = []
        for k in range(1, 8-i):
            if self.board[i+k,j] == -self.current_player:
                l.append((i+k, j))
            else:
                if self.board[i+k,j] == self.current_player:
                    can_flip.update(l)
                break

        # -135
        l = []
        for k in range(1, min(8-i, j+1)):
            if self.board[i+k,j-k] == -self.current_player:
                l.append((i+k, j-k))
            else:
                if self.board[i+k, j-k] == self.current_player:
                    can_flip.update(l)
                break
        
        if len(can_flip) == 0:
            if hint:
                print("Can\'t flip anything!")
            return False
        return True

    def find_valid_moves(self):
        valid_moves = {}
        searched = np.abs(self.board)
        if self.current_player==1:
            opponent_pieces = self.white_pieces
        else:
            opponent_pieces = self.black_pieces
        for p in opponent_pieces:
            for di in range(-1,2):
                for dj in range(-1,2):
                    if (di!=0 or dj!=0) and (0 <= p[0]+di < 8 and 0 <= p[1]+dj < 8):
                        can_flip = set()
                        if searched[p[0]+di,p[1]+dj]==0 and self.is_valid_move(p[0]+di, p[1]+dj,can_flip,hint=False):
                            valid_moves[(p[0]+di, p[1]+dj)] = can_flip
                            searched[p[0]+di, p[1]+dj] = 1
        return valid_moves

    def make_move(self,i,j,hint=True):
        can_flip = set()
        if not self.is_valid_move(i, j, can_flip, hint):
            if hint:
                print("Not a valid move!")
            return

        self.board[i,j] = self.current_player
        if self.current_player==1:
            self.black_pieces.add((i, j))
        else:
            self.white_pieces.add((i, j))

        for p in can_flip:
            self.board[p] = self.current_player
            if self.current_player == 1:
                self.black_pieces.add(p)
                self.white_pieces.remove(p)
            else:
                self.white_pieces.add(p)
                self.black_pieces.remove(p)

        self.current_player = -self.current_player
        self.print_board()
        return

    def play(self):
        if not self.game_end:
            print("Game start!")
            self.print_board()
            prev_valid = True
            while len(self.black_pieces)+len(self.white_pieces) < 64:
                if self.current_player==1:
                    print("Black's turn!")
                else:
                    print("White's turn!")

                valid_moves = self.find_valid_moves()
                if len(valid_moves) == 0:
                    if not prev_valid:
                        break
                    print("No valid move!")
                    prev_valid = False
                    self.current_player = -self.current_player
                    continue
                prev_valid = True

                print("Enter the coordinate of your move (i j/stop/hint): ")
                command = input()
                try:
                    p = list(map(int, command.split()))
                    if len(p) == 2:
                        self.make_move(p[0], p[1])
                    else:
                        print("Need 2 numbers!")
                except:
                    if command == 'hint':
                        print(valid_moves)
                    elif command == 'stop':
                        break
                    else:
                        print("Not numbers!")

        print("Game over!")
        self.game_end = True
        if len(self.black_pieces)>len(self.white_pieces):
            print("Black wins! {}:{}".format(
                len(self.black_pieces), len(self.white_pieces)))
        elif len(self.black_pieces) < len(self.white_pieces):
            print("White wins! {}:{}".format(
                len(self.black_pieces), len(self.white_pieces)))
        else:
            print("Draw! {}:{}".format(
                len(self.black_pieces), len(self.white_pieces)))
