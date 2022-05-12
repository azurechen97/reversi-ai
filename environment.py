import numpy as np

class Reversi:
    def __init__(self, size = 8, init_board = None) -> None:
        # init_board can be a dict, with key 1 (black) and key -1 (white), and the values are sets contains the tuples of coordinates
        # init_board can be a numpy array, with 1 (black), -1 (white), and 0 (not occupied)
        self.size = size
        self.reset(init_board)
    
    # reset the game
    def reset(self, init_board=None):    
        if type(init_board) is dict and 1 in init_board and -1 in init_board:
            self.black_pieces = init_board[1].copy()
            self.white_pieces = init_board[-1].copy()
            self.refresh_board()
        elif type(init_board) is np.ndarray and init_board.shape == (self.size,self.size):
            self.board = init_board
            self.refresh_pieces()
        else:
            self.black_pieces = {
                (self.size//2, self.size//2-1), (self.size//2-1, self.size//2)}
            self.white_pieces = {
                (self.size//2-1, self.size//2-1), (self.size//2, self.size//2)}
            self.refresh_board()
            
        self.current_player = 1 # 1=black, -1=white
        self.game_end = False

    # refresh the board with the sets of pieces
    def refresh_board(self):
        self.board = np.zeros((self.size, self.size), dtype=np.int8)
        for p in self.black_pieces:
            if 0<=p[0]<self.size and 0<=p[1]<self.size:
                self.board[p] = 1
        for p in self.white_pieces:
            if 0 <= p[0] < self.size and 0 <= p[1] < self.size:
                self.board[p] = -1
    
    # refresh the sets of pieces with the board
    def refresh_pieces(self):
        self.black_pieces = set()
        self.white_pieces = set()
        bp = np.argwhere(self.board == 1)
        wp = np.argwhere(self.board == -1)
        for k in range(bp.shape[0]):
            self.black_pieces.add((bp[k, 0], bp[k, 1]))
        for k in range(wp.shape[0]):
            self.white_pieces.add((wp[k, 0], wp[k, 1]))

    def print_board(self):
        print(' '.join([' ']+[str(i) for i in range(self.size)]))
        for i in range(self.size):
            print(str(i), end=' ')
            for j in range(self.size):
                if self.board[i,j] == 1:
                    print('●', end=' ')
                elif self.board[i,j] == -1:
                    print('○', end=' ')
                else:
                    print(' ', end=' ')
            print()

    # tell if a move is valid on the current board for current player
    def is_valid_move(self,i,j,can_flip=set(),hint=True):
        # out of bound
        if i >= self.size or i < 0 or j >= self.size or j < 0:
            if hint:
                print("Out of bound!")
            return False
        # overlapping
        if self.board[i,j]!=0:
            if hint:
                print("Overlapping!")
            return False
        # cannot flip anything
        # 180 degree
        l = []
        for k in range(1,j+1):
            if self.board[i,j-k] == -self.current_player:
                l.append((i, j-k))
            else:
                if self.board[i,j-k] == self.current_player:
                    can_flip.update(l)
                break

        # 135 degree
        l = []
        for k in range(1, min(i+1,j+1)):
            if self.board[i-k,j-k] == -self.current_player:
                l.append((i-k, j-k))
            else:
                if self.board[i-k,j-k] == self.current_player:
                    can_flip.update(l)
                break

        # 90 degree
        l = []
        for k in range(1, i+1):
            if self.board[i-k,j] == -self.current_player:
                l.append((i-k, j))
            else:
                if self.board[i-k,j] == self.current_player:
                    can_flip.update(l)
                break

        # 45 degree
        l = []
        for k in range(1, min(i+1, self.size-j)):
            if self.board[i-k,j+k] == -self.current_player:
                l.append((i-k, j+k))
            else:
                if self.board[i-k,j+k] == self.current_player:
                    can_flip.update(l)
                break

        # 0 degree
        l = []
        for k in range(1, self.size-j):
            if self.board[i,j+k] == -self.current_player:
                l.append((i, j+k))
            else:
                if self.board[i, j+k] == self.current_player:
                    can_flip.update(l)
                break

        # -45 degree
        l = []
        for k in range(1, min(self.size-i, self.size-j)):
            if self.board[i+k,j+k] == -self.current_player:
                l.append((i+k, j+k))
            else:
                if self.board[i+k, j+k] == self.current_player:
                    can_flip.update(l)
                break

        # -90 degree
        l = []
        for k in range(1, self.size-i):
            if self.board[i+k,j] == -self.current_player:
                l.append((i+k, j))
            else:
                if self.board[i+k,j] == self.current_player:
                    can_flip.update(l)
                break

        # -135 degree
        l = []
        for k in range(1, min(self.size-i, j+1)):
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

    # find all valid moves on the current board for current player
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
                    if (di != 0 or dj != 0) and (0 <= p[0]+di < self.size and 0 <= p[1]+dj < self.size):
                        can_flip = set()
                        if searched[p[0]+di,p[1]+dj]==0 and self.is_valid_move(p[0]+di, p[1]+dj,can_flip,hint=False):
                            valid_moves[(p[0]+di, p[1]+dj)] = can_flip
                            searched[p[0]+di, p[1]+dj] = 1
        return valid_moves

    # make a move and flip the opponent's pieces
    def make_move(self, i, j, hint=True, trace=True):
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
        if trace:
            self.print_board()
        return

    def game_over(self):
        print("Game over!")
        self.game_end = True
        if len(self.black_pieces) > len(self.white_pieces):
            print("Black wins! {}:{}".format(
                len(self.black_pieces), len(self.white_pieces)))
        elif len(self.black_pieces) < len(self.white_pieces):
            print("White wins! {}:{}".format(
                len(self.black_pieces), len(self.white_pieces)))
        else:
            print("Draw! {}:{}".format(
                len(self.black_pieces), len(self.white_pieces)))
        # print("Reset? (y/n):")
        # if input() == 'y':
        #     self.reset()
        self.reset()

    def play(self):
        if self.game_end:
            self.game_over()
        else:
            print("Game start!")
            self.print_board()
            prev_valid = True
            while True:
                if len(self.black_pieces)+len(self.white_pieces)>=64:
                    self.game_over()
                    break

                if self.current_player==1:
                    print("Black's turn!")
                else:
                    print("White's turn!")

                valid_moves = self.find_valid_moves()
                if len(valid_moves) == 0:
                    print("No valid move!")
                    if not prev_valid:
                        self.game_over()
                        break
                    prev_valid = False
                    self.current_player = -self.current_player
                    continue
                prev_valid = True

                print("Enter your move (i j) or command (pause/stop/hint):")
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
                        self.game_over()
                        break
                    elif command == 'pause':
                        break
                    else:
                        print("Not numbers!")

if __name__ == "__main__":
    reversi = Reversi()
    reversi.play()
