# coding: utf-8

__version__ = "0.1"
__author__ = "Mathilde Binet, Asma Dassi, Axel Chedri, Vincent Nguyen, Baptiste Pasquier"

from .cp2048 import Game2048  # noqa
from .evaluate import evaluate_strategy  # noqa
from .mystrategy import nextmovescorebest
from .random_strategy import random_strategy
