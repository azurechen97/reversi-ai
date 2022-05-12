import copy

import numpy as np
from environment import *
from evaluation import score
import random

class ReversiAI:
    def __init__(self, ai_color=-1) -> None:
        self.ai_color = ai_color

    def find_best_move(self, reversi, valid_moves=None):
        pass

    def play(self, reversi=None):
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
                    print("{} plays at ({},{}).".format("Black" if self.ai_color==1 else "White",best_move[0],best_move[1]))
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
        return reversi

class ArtificialIdiot(ReversiAI):
    def __init__(self, ai_color=-1) -> None:
        super().__init__(ai_color)
    
    def find_best_move(self, reversi, valid_moves=None):
        if valid_moves is None:
            valid_moves = reversi.find_valid_moves()
        return random.choice(list(valid_moves.keys()))

class EasyAI(ReversiAI):
    def __init__(self, ai_color=-1) -> None:
        super().__init__(ai_color)

    def find_best_move(self, reversi, valid_moves=None):
        if valid_moves is None:
            valid_moves = reversi.find_valid_moves()
        greedy_move = [[], -np.inf]
        for k, v in valid_moves.items():
            if len(v) > greedy_move[1]:
                greedy_move[0] = [k]
                greedy_move[1] = len(v)
            elif len(v) == greedy_move[1]:
                greedy_move[0].append(k)
        return random.choice(greedy_move[0])

class NormalAI(ReversiAI):
    def __init__(self, ai_color=-1, search_depth=4) -> None:
        super().__init__(ai_color)
        self.search_depth = search_depth

    def find_best_move(self, reversi, valid_moves=None):
        metrics = score()
        tree = Tree(reversi, maximizing_player=self.ai_color)
        _, move = pruning(tree, metrics, depth=self.search_depth)
        return move

class HardAI(ReversiAI):
    def __init__(self, ai_color=-1) -> None:
        super().__init__(ai_color)

class Tree:
    def __init__(self, node, maximizing_player, children=None, moves=None):
        self.node = node
        self.children = children
        self.maximizing_player = maximizing_player
        self.moves = moves

    def __str__(self):
        return f"Tree({', '.join(str(sub) for sub in self.children)})"

def pruning(tree, metrics, alpha=float("-inf"), beta=float("+inf"), depth=4):
    # if isinstance(tree, Terminal):
    #     return tree.value
    if depth == 0:
        # reach the leaf node, evaluate leaf score
        return metrics.eval(tree.node), None
    else:
        # append children to the node
        num_try = 2

        while num_try > 0:
            valid_moves = tree.node.find_valid_moves()
            if len(valid_moves) > 0:
                children = []
                moves = []
                for move in valid_moves:
                    new_node = copy.deepcopy(tree.node)
                    new_node.make_move(move[0], move[1], trace=False)
                    children.append(Tree(node=new_node,
                                         maximizing_player=-1*tree.maximizing_player))
                    moves.append(move)
                tree.children = children
                tree.moves = moves
                break
            else:
                tree.node.current_player *= -1
                num_try -= 1
        if num_try == 0:
            # game over, neither players can move
            # can not add any child to current broad
            # return the score
            return metrics.eval(tree.node), None

    val = float("-inf") if tree.maximizing_player > 0 else float("+inf")
    ret_m = None
    for i, subtree in enumerate(tree.children):
        sub_val, _ = pruning(subtree, metrics, alpha, beta, depth=depth-1)
        if tree.maximizing_player > 0:
            val = max(val, sub_val)
            alpha = max(alpha, sub_val)
        else:
            val = min(val, sub_val)
            beta = min(beta, sub_val)
        if sub_val == val:
            ret_m = tree.moves[i]
        if beta <= alpha:
            break
    return val, ret_m


if __name__ == "__main__":
    ai_color = 0
    while ai_color == 0:
        try:
            player_color = input("What color do you want? (b/w):")
            if player_color == 'b' or player_color == '':
                ai_color = -1
            elif player_color == 'w':
                ai_color = 1
        except:
            pass

    ai = None
    while ai is None:
        try:
            level = int(input("Level (0-3):"))
            if level == 0:
                ai = ArtificialIdiot(ai_color)
            elif level == 1:
                ai = EasyAI(ai_color)
            elif level == 2:
                ai = NormalAI(ai_color)
            elif level == 3:
                ai = HardAI(ai_color)
        except:
            pass
    
    ai.play()