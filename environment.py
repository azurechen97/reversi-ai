import numpy as np

class Reversi:
    def __init__(self) -> None:
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        self.black_pieces = [(3, 3), (4, 4)]
        self.white_pieces = [(3, 4), (4, 3)]
        self.refresh_board()
        self.black_move = True
    
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

    def is_valid_move(self,i,j):
        # out of bound
        if i >= 8 or i < 0 or j >= 8 or j < 0:
            print("Out of bound!")
            return False
        # overlapping
        if (i, j) in self.black_pieces or (i, j) in self.white_pieces:
            print("Overlapping!")
            return False
        # cannot flip anything
        return True

    def find_valid_moves(self):
        pass

    def make_move(self,i,j):
        if not self.is_valid_move(i,j):
            print("Not a valid move!")
            return
        self.board[i][j] = 1 if self.black_move else -1
        if self.black_move:
            self.black_pieces.append((i, j))
        else:
            self.white_pieces.append((i, j))
        self.black_move = not self.black_move
        self.print_board()
        return

    def endgame(self):
        pass