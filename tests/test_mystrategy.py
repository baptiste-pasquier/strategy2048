"""
Unit tests
"""
import unittest
import numpy
from strategy2048.mystrategy import score1


class TestStrategy(unittest.TestCase):

    def test_score1(self):
        a = numpy.array([[0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0]])
        b = numpy.array([[1, 0, 0, 1],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [1, 0, 0, 1]])
        assert score1(a) == 1
        assert score1(b) == 0.75


if __name__ == '__main__':
    unittest.main()
