import numpy as np


class Score:
    def __init__(self, method:list = None, weight:list = None):
        if method is not None and method is not None:
            assert len(method) == len(weight), 'Method and weight should have the same length'
        if method is None:
            method = ['num_pieces', 'position_score', 'possible_moves', 'getstable']
        self.method = method
        self.weight = weight

    def num_pieces(self, reversi):
        return np.sum(reversi.board)

    def position_score(self, reversi, Vmap=None):
        if Vmap is None:
            if len(reversi.board) == 8:
                Vmap = np.array([[500, -25, 10, 5, 5, 10, -25, 500],
                                 [-25, -45, 1, 1, 1, 1, -45, -25],
                                 [10, 1, 3, 2, 2, 3, 1, 10],
                                 [5, 1, 2, 1, 1, 2, 1, 5],
                                 [5, 1, 2, 1, 1, 2, 1, 5],
                                 [10, 1, 3, 2, 2, 3, 1, 10],
                                 [-25, -45, 1, 1, 1, 1, -45, -25],
                                 [500, -25, 10, 5, 5, 10, -25, 500]])
                return np.sum(reversi.board * Vmap)
            else:
                return 0
        else:
            if len(reversi.board) == len(Vmap):
                return np.sum(reversi.board * Vmap) * reversi.current_player
            else:
                raise ValueError('Input Vmap should have the same shape with board')

    def possible_moves(self, reversi):
        valid_move = reversi.find_valid_moves()
        return len(valid_move) * reversi.current_player

    def getstable(self, reversi):
        board = reversi.board
        color = reversi.current_player
        # function copied from https://zhuanlan.zhihu.com/p/35121997
        # 角、边、8个方向 都无空位的稳定子
        stable = [0,0,0]

        cind1 = [0,0,7,7]
        cind2 = [0,7,7,0]
        inc1 = [0,1,0,-1]
        inc2 = [1,0,-1,0]
        stop = [0,0,0,0]
        for i in range(4):
            if board[cind1[i]][cind2[i]] == color:
                stop[i] = 1
                stable[0] += 1
                for j in range(1,7):
                    if board[cind1[i]+inc1[i]*j][cind2[i]+inc2[i]*j] != color:
                        break
                    else:
                        stop[i] = j + 1
                        stable[1] += 1
        for i in range(4):
            if board[cind1[i]][cind2[i]] == color:
                for j in range(1,7-stop[i-1]):
                    if board[cind1[i]-inc1[i-1]*j][cind2[i]-inc2[i-1]*j] != color:
                        break
                    else:
                        stable[1] += 1
        colfull = np.zeros((8, 8), dtype=np.int)
        colfull[:,np.sum(abs(board), axis = 0) == 8] = True
        rowfull = np.zeros((8, 8), dtype=np.int)
        rowfull[np.sum(abs(board), axis = 1) == 8,:] = True
        diag1full = np.zeros((8, 8), dtype=np.int)
        for i in range(15):
            diagsum = 0
            if i <= 7:
                sind1 = i
                sind2 = 0
                jrange = i+1
            else:
                sind1 = 7
                sind2 = i-7
                jrange = 15-i
            for j in range(jrange):
                diagsum += abs(board[sind1-j][sind2+j])
            if diagsum == jrange:
                for k in range(jrange):
                    diag1full[sind1-j][sind2+j] = True
        diag2full = np.zeros((8, 8), dtype=np.int)
        for i in range(15):
            diagsum = 0
            if i <= 7:
                sind1 = i
                sind2 = 7
                jrange = i+1
            else:
                sind1 = 7
                sind2 = 14-i
                jrange = 15-i
            for j in range(jrange):
                diagsum += abs(board[sind1-j][sind2-j])
            if diagsum == jrange:
                for k in range(jrange):
                    diag2full[sind1-j][sind2-j] = True
        stable[2] = sum(sum(np.logical_and(np.logical_and(np.logical_and(colfull, rowfull), diag1full), diag2full)))
        return sum(stable) * reversi.current_player

    def eval(self, reversi):
        score_list = []
        for m in self.method:
            score_list.append(eval('self.'+m)(reversi))
        if self.weight is None:
            return np.sum(score_list)
        else:
            ret = 0
            for w, s in zip(self.weight, score_list):
                ret += w * s
            return ret

class ScoreAdvanced(Score):
    def __init__(self, method: list = None, weight: list = None) -> None:
        super().__init__(method, weight)
    
    def possible_moves(self, reversi):
        valid_move = reversi.find_valid_moves()
        return -1/(len(valid_move)+1e-5) * reversi.current_player
    
    def eval(self, reversi):
        if reversi.is_game_over():
            if reversi.winner is None:
                reversi.game_over(hint=False)
            return reversi.current_player*1e6
            
        score_list = []
        for m in self.method:
            score_list.append(eval('self.'+m)(reversi))
        if self.weight is None:
            return np.sum(score_list)
        else:
            ret = 0
            for w, s in zip(self.weight, score_list):
                ret += w * s
            return ret
