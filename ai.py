import numpy as np
from environment import *

class ReversiAI:
    def __init__(self, ai_color=-1) -> None:
        self.ai_color = ai_color

    def find_best_move(self):
        pass

    def play(self):
        pass

class EasyAI(ReversiAI):
    def __init__(self, ai_color=-1) -> None:
        super().__init__(ai_color)

class NormalAI(ReversiAI):
    def __init__(self, ai_color=-1) -> None:
        super().__init__(ai_color)

class HardAI(ReversiAI):
    def __init__(self, ai_color=-1) -> None:
        super().__init__(ai_color)
