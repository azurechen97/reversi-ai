import numpy as np

class Reversi:
    def __init__(self) -> None:
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        self.black_pieces = {(3, 3), (4, 4)}
        self.white_pieces = {(3, 4), (4, 3)}
        self.refresh_board()
        self.current_player = 1
    
    def refresh_board(self):
        for p in self.black_pieces:
            self.board[p[0]][p[1]] = 1
        for p in self.white_pieces:
            self.board[p[0]][p[1]] = -1
        return self.board

    def print_board(self):
        print(' '.join([' ']+[str(i) for i in range(8)]))
        for i in range(8):
            print(str(i), end=' ')
            for j in range(8):
                if self.board[i][j] == 1:
                    print('●', end=' ')
                elif self.board[i][j] == -1:
                    print('○', end=' ')
                else:
                    print(' ', end=' ')
            print()

    def is_valid_move(self,i,j,can_flip):
        # out of bound
        if i >= 8 or i < 0 or j >= 8 or j < 0:
            print("Out of bound!")
            return False
        # overlapping
        if self.board[i][j]!=0:
            print("Overlapping!")
            return False
        # cannot flip anything
        # 180
        l = []
        for k in range(1,j+1):
            if self.board[i][j-k] == -self.current_player:
                l.append((i, j-k))
            else:
                if self.board[i][j-k] == 0:
                    l = []
                break
        can_flip.extend(l)

        # 135
        l = []
        for k in range(1, min(i+1,j+1)):
            if self.board[i-k][j-k] == -self.current_player:
                l.append((i-k, j-k))
            else:
                if self.board[i-k][j-k] == 0:
                    l = []
                break
        can_flip.extend(l)

        # 90
        l = []
        for k in range(1, i+1):
            if self.board[i-k][j] == -self.current_player:
                l.append((i-k, j))
            else:
                if self.board[i-k][j] == 0:
                    l = []
                break
        can_flip.extend(l)

        # 45
        l = []
        for k in range(1, min(i+1, 8-j)):
            if self.board[i-k][j+k] == -self.current_player:
                l.append((i-k, j+k))
            else:
                if self.board[i-k][j+k] == 0:
                    l = []
                break
        can_flip.extend(l)

        # 0
        l = []
        for k in range(1, 8-j):
            if self.board[i][j+k] == -self.current_player:
                l.append((i, j+k))
            else:
                if self.board[i][j+k] == 0:
                    l = []
                break
        can_flip.extend(l)

        # -45
        l = []
        for k in range(1, min(8-i, 8-j)):
            if self.board[i+k][j+k] == -self.current_player:
                l.append((i+k, j+k))
            else:
                if self.board[i+k][j+k] == 0:
                    l = []
                break
        can_flip.extend(l)

        # -90
        l = []
        for k in range(1, 8-i):
            if self.board[i+k][j] == -self.current_player:
                l.append((i+k, j))
            else:
                if self.board[i+k][j] == 0:
                    l = []
                break
        can_flip.extend(l)

        # -135
        l = []
        for k in range(1, min(8-i, j+1)):
            if self.board[i+k][j-k] == -self.current_player:
                l.append((i+k, j-k))
            else:
                if self.board[i+k][j-k] == 0:
                    l = []
                break
        can_flip.extend(l)
        
        if len(can_flip) == 0:
            print("Can\'t flip anything!")
            return False
        return True

    def find_valid_moves(self):
        pass

    def make_move(self,i,j):
        can_flip = []
        if not self.is_valid_move(i, j, can_flip):
            print("Not a valid move!")
            return

        self.board[i][j] = self.current_player
        if self.current_player==1:
            self.black_pieces.add((i, j))
        else:
            self.white_pieces.add((i, j))

        for p in can_flip:
            self.board[p[0]][p[1]] = self.current_player
            if self.current_player == 1:
                self.black_pieces.add(p)
                self.white_pieces.remove(p)
            else:
                self.white_pieces.add(p)
                self.black_pieces.remove(p)

        self.current_player = -self.current_player
        self.print_board()
        return

    def endgame(self):
        pass