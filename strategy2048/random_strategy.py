"""
Implements a random strategy for the game 2048.
Source : https://github.com/sdpython/pystrat2048/blob/master/pystrat2048/random_strategy.py
"""
import random


def random_strategy(game, state=None, moves=None):
    """
    Returns a random direction.

    :param game: matrix usually 4x4 but could anything else
    :param state: keeps here anything you need, it will be
        here at the next call to the function
    :param moves: list of previous moves (unused)
    :return: a direction in `{0, 1, 2, 3}`
    """
    return random.randint(0, 3)


def random_strategy_all_but_one(game, state=None, moves=None):
    """
    Returns a random direction among three.

    :param game: matrix usually 4x4 but could anything else
    :param state: keeps here anything you need, it will be
        here at the next call to the function
    :param moves: list of previous moves (unused)
    :return: a direction in `{0, 1, 2}`
    """
    return random.randint(0, 2)
