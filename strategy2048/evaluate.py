"""
Implements a function to test a strategy for the 2048.
Source : https://github.com/sdpython/pystrat2048/blob/master/pystrat2048/evaluate.py
"""
from .cp2048 import Game2048, GameOverException


def evaluate_strategy(fct_strategy, ntries=10):
    """
    Applies method *best_move* until gameover
    starting from the current position. Repeats *ntries* times
    and the maximum number in every try.
    @param      fct_strategy    a function which returns the best move
                                (see below)
    @return                     enumerator on scores
    One example to show how to test a strategy:
    .. runpython::
        :showcode:
        import random
        from ensae_teaching_cs.td_1a.cp2048 import evaluate_strategy
        def random_strategy(game, moves):
            return random.randint(0, 3)
        scores = list(evaluate_strategy(random_strategy))
        print(scores)
    """
    for i in range(0, ntries):
        g = Game2048()
        while True:
            try:
                g.next_turn()
            except (GameOverException, RuntimeError):
                break
            d = fct_strategy(g.game, g.moves)
            g.play(d)
        yield g.score()