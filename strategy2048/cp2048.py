"""
Implémentation des règles du jeu 2048
Source : https://github.com/sdpython/pystrat2048/blob/master/pystrat2048/cp2048.py
Des modificiations ont été faites pour optimiser (temps) l'exécution. 
"""
import random
import numpy
import functools


# Classe optimisée grâce à la function directionaleatoire et mémoisiation de process_line

### Beaucoup plus rapide que l'utilisation de random
def directionaleatoire():
    """
    Retourne un entier aléatoire entre 0 et 3 compris
    """
    x = random.random()
    if x < 0.25:
        return 0
    elif x < 0.5:
        return 1
    elif x < 0.75:
        return 2
    else:
        return 3


class GameOverException(RuntimeError):
    """
    Exception levée en cas de Game Over
    """
    pass


class Game2048:
    """
    Logique du jeu 2048
    """

    def __init__(self, game=None):
        """
        :param game: None or matrix 4x4
        """
        if type(game) == numpy.ndarray:
            self.game = game
        else:
            self.game = numpy.zeros((4, 4), dtype=int)
        self.moves = []

    def __str__(self):
        """
        Displays the game as a string.
        """
        if len(self.moves) > 3:
            last_moves = self.moves[-3:]
        else:
            last_moves = self.moves
        return "{}\n{}".format(str(self.game), str(last_moves))

    def gameover(self):
        "Checks the game is over or not. Returns True in that case."
        # return numpy.ma.masked_not_equal(self.game, 0).count() == 0
        return 0 not in self.game

    def copy(self):
        "Makes a copy of the game."
        return Game2048(self.game.copy())

    def next_turn(self):
        "Adds a number in the game."
        if self.gameover():
            # raise GameOverException("Game Over\n" + str(self.game))
            raise GameOverException()
        else:
            while True:
                # i = random.randint(0, self.game.shape[0] - 1)
                # j = random.randint(0, self.game.shape[1] - 1)
                i = directionaleatoire()
                j = directionaleatoire()
                if self.game[i, j] == 0:
                    # n = random.randint(0, 3)
                    n = directionaleatoire()
                    self.game[i, j] = 4 if n == 0 else 2
                    self.moves.append((i, j, self.game[i, j]))
                    break


    @staticmethod
    def process_line(line):
        return process_line_memoisation(tuple(line))   # tuple pour memoisation (hashable)

    def play(self, direction):
        "Updates the game after a direction was chosen."
        if direction == 0:
            lines = [Game2048.process_line(self.game[i, :])
                     for i in range(self.game.shape[0])]
            self.game = numpy.array(lines)
        elif direction == 1:
            lines = [Game2048.process_line(self.game[:, i])
                     for i in range(self.game.shape[1])]
            self.game = numpy.array(lines).T
        elif direction == 2:
            lines = [list(reversed(Game2048.process_line(self.game[i, ::-1])))
                     for i in range(self.game.shape[0])]
            self.game = numpy.array(lines)
        elif direction == 3:
            lines = [list(reversed(Game2048.process_line(self.game[::-1, i])))
                     for i in range(self.game.shape[1])]
            self.game = numpy.array(lines).T

    def score(self):
        "Returns the maximum values."
        return numpy.max(self.game)


### Mémoisation process line : 25% de temps en moins
@functools.lru_cache(maxsize=None) 
def process_line_memoisation(line):
    """
    Moves numbers inside a vector whether this vector represents
    a row or a column.
    """
    res = []
    for n in line:
        if n == 0:
            # Zero: skipped.
            continue
        if len(res) == 0:
            # First number: add.
            res.append(n)
        else:
            prev = res[-1]
            if prev == n:
                # The number is identical: combine.
                res[-1] = 2 * n
            else:
                # Otherwise: add.
                res.append(n)
    while len(res) < len(line):
        res.append(0)
    return res