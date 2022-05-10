import numpy as np

def num_pieces(reversi):
    '''
    count the number of pieces for this player
    :param board: ndarray
    :param mycolor: -1 or 1
    :return: score
    '''
    return np.sum(reversi.board) * reversi.current_player


def position_score(reversi, Vmap=None):
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
            return np.sum(reversi.board * Vmap) * reversi.current_player
        else:
            return 0
    else:
        if len(reversi.board) == len(Vmap):
            return np.sum(reversi.board * Vmap) * reversi.current_player
        else:
            raise ValueError('Input Vmap should have the same shape with board')

def possible_moves(reversi):
    valid_move = reversi.find_valid_moves()
    return len(valid_move)

def getstable(board, color):
    # function copied from https://zhuanlan.zhihu.com/p/35121997
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
    return stable

def score(reversi, weights=None):
    score_list = [num_pieces(reversi), position_score(reversi), possible_moves(reversi), getstable(reversi.board, reversi.current_player)]
    if weights is None:
        return np.sum(score_list)
    else:
        ret = 0
        for w, s in zip(weights, score_list):
            ret += w * s
        return ret