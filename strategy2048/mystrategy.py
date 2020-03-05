import numpy
from .cp2048 import Game2048, GameOverException
from .evaluate import evaluate_strategy
import matplotlib.pyplot as plt
import random
import multiprocessing
import time

# ---------------------------------------------------------------------------- #
#                                    Outils                                    #
# ---------------------------------------------------------------------------- #


def moyenne(liste):
    return numpy.sum(liste) / len(liste)


def maxindice(liste):
    """
    Indice du premier maximum de la liste
    """
    indice, max = 0, 0
    for i in range(0, len(liste)):
        if liste[i] > max:
            indice, max = i, liste[i]
    return indice


# Outil d'affichage

def affiche_distribution(liste):
    liste = sorted(liste)
    liste = numpy.array(liste)
    D = {}
    for elem in liste:
        if elem in D:
            D[elem] += 1
        else:
            D[elem] = 1
    plt.bar(range(len(D)), list(D.values()), align='center')
    plt.xticks(range(len(D)), list(D.keys()))
    print("Moyenne =", moyenne(liste))
    print("proportion >= 2048 =", (liste >= 2048).sum() / len(liste))



# ---------------------------------------------------------------------------- #
#                  Stratégie : maximiser le nombre de fusions                  #
# ---------------------------------------------------------------------------- #


def nombre_fusion(game):
    """
    Retourne le nombre de fusions possibles pour chaque mouvement.
    """
    res = [0, 0]
    for numligne in range(game.shape[0]):
        ligne = list(game[numligne, :])
        while 0 in ligne:
            ligne.remove(0)
        if len(ligne) >= 2:
            prec = ligne[0]
            for numcolonne in range(1, len(ligne)):
                suivant = ligne[numcolonne]
                if suivant == prec:
                    res[0] += 1
                    prec = -1
                else:
                    prec = suivant

    for numcolonne in range(game.shape[1]):
        colonne = list(game[:, numcolonne])
        while 0 in colonne:
            colonne.remove(0)
        if len(colonne) >= 2:
            prec = colonne[0]
            for numligne in range(1, len(colonne)):
                suivant = colonne[numligne]
                if suivant == prec:
                    res[1] += 1
                    prec = -1
                else:
                    prec = suivant
    return res


def nextmove(game, move):
    res_nombre_fusion = nombre_fusion(game)
    if res_nombre_fusion[0] >= res_nombre_fusion[1]:
        return random.choice([0, 2])
    else:
        return random.choice([1, 3])


def nextmovebest(game, move):
    profondeur = 5
    nombre = 20
    scores = 4 * [0]
    for d in range(0, 4):
        for i in range(0, nombre):
            g = Game2048(game)
            g.play(d)
            for niveau in range(0, profondeur):
                try:
                    g.next_turn()
                except (GameOverException, RuntimeError):
                    break
                a = nextmove(g.game, [])
                g.play(a)
            scores[d] += g.score()
    return maxindice(scores)



# ---------------------------------------------------------------------------- #
#                                Multiprocessing                               #
# ---------------------------------------------------------------------------- #


# def evaluate_strategy_0(i):
#     return list(evaluate_strategy(nextmovebest, 1))[0]


# import multiprocessing

# if __name__ == '__main__':
#     temps = time.time()
#     pool = multiprocessing.Pool(processes=4)
#     result_list = pool.map(evaluate_strategy_0, numpy.arange(4))   # Nombre de test pour la moyenne
#     # result_list = [f(x) for x in range(0,1000)]
#     print(time.time()-temps)
#     print(result_list)
#     print(moyenne(result_list))


# # --------------------------------- Profiling -------------------------------- #

# def main():
#     list(evaluate_strategy(nextmovebest, 1))
# #

# cProfile.run('main()')

# with PyCallGraph(output=GraphvizOutput()):
#     main()



# ---------------------------------------------------------------------------- #
#                         Stratégie : plusieurs scores                         #
# ---------------------------------------------------------------------------- #


def score1(game):
    """
    Input : jeu 2048
    Output : proportion de cases vides
    """
    return (game == 0).sum() / 16


def score2(game):
    """
    Input : jeu 2048
    Output : grand nombre lorsque le jeu est proche du filtre
    """
    filtre = numpy.array([[1, 0, 0, 1],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [1, 0, 0, 1]])
    return numpy.sum(game * filtre) / game.max()


def score(game, coeff1, coeff2):
    """
    Input : jeu 2048
    Output : combinaison des deux scores
    """
    return score1(game) * coeff1 + score2(game) * coeff2


def nextmovescore(game, moves, coeff1=64, coeff2=4):
    """
    Output : direction à effectuer pour maximiser le score sur un mouvement
    """
    scores = 4 * [0]
    for d in range(0, 4):
        g = Game2048(game)
        g.play(d)
        scores[d] = score(g.game, coeff1, coeff2)
    return maxindice(scores)


def nextmovescorebest(game, state=None, moves=None):
    """
    Output : direction à effectuer pour maximiser le score en prenant en
    compte une certaine profondeur dans l'arbre des possibilités.
    """
    coeff1 = 64
    coeff2 = 4
    profondeur = 2    # profondeur dans l'arbre
    nombre = 20        # nombre de chemin à parcourir dans l'arbre

    scores = 4 * [0]
    for d in range(0, 4):
        for i in range(0, nombre):
            g = Game2048(game)
            g.play(d)
            for niveau in range(0, profondeur):
                try:
                    g.next_turn()
                except (GameOverException, RuntimeError):
                    break
                a = nextmovescore(g.game, [], coeff1, coeff2)
                g.play(a)
            scores[d] += score(g.game, coeff1, coeff2)
    return maxindice(scores)


# Test
# temps = time.time()
# affiche_distribution(list(evaluate_strategy(nextmovescorebest, 1000)))
# print(time.time() - temps)


# ------------------------------ Multiprocessing ----------------------------- #

def evaluate_strategy_1(i):
    return list(evaluate_strategy(nextmovescorebest, 1))[0]


if __name__ == '__main__':
    temps = time.time()
    pool = multiprocessing.Pool(processes=4)
    result_list = pool.map(evaluate_strategy_1, numpy.arange(50))   # Nombre de test pour la moyenne
    # result_list = [evaluate_strategy_1(x) for x in range(0, 10)]
    print(time.time() - temps)
    print(result_list)
    print("Moyenne =", moyenne((result_list)))
    print("proportion >= 2048 =", ((numpy.array(result_list) >= 2048).sum() / len((result_list))))



# ---------------------------------------------------------------------------- #
#                      Détermination des meilleurs coeffs                      #
# ---------------------------------------------------------------------------- #


# def fcoeff(coeffs):
#     return [coeffs[0], coeffs[1], moyenne(list(evaluate_strategy(nextmovescorebest, 1, coeffs[0], coeffs[1])))]

# listcoeff1 = [64]
# listcoeff2 = [0, 2, 4, 8, 16]
# listcoeff = []
# for coeff1 in listcoeff1:
#     for coeff2 in listcoeff2:
#             listcoeff.append((coeff1, coeff2))


# if __name__ == '__main__':
#     temps = time.time()
#     pool = multiprocessing.Pool(processes=4)
#     result_list = pool.map(fcoeff, listcoeff)
#     print(time.time()-temps)
#     print(result_list)


# # --------------------------------- Profiling -------------------------------- #

# def main():
#      list(evaluate_strategy(nextmovescorebest, 100))


# cProfile.run('main()')

# with PyCallGraph(output=GraphvizOutput()):
#     main()



# ---------------------------------------------------------------------------- #
#           Stratégie : Tester un certain nombre de jeux aléatoires            #
# ---------------------------------------------------------------------------- #


# def simulationaléatoire(param):
#     """
#     A partir d'un jeux, joue aléatoirement jusqu'à échec
#     Retourne la somme des scores
#     """
#     game, n, direction = param
#     resul = 0
#     g = Game2048(game)
#     g.play(direction)
#     for i in range(0, n):
#         gi = g.copy()
#         while True:
#             try:
#                 gi.next_turn()
#             except (GameOverException, RuntimeError):
#                 break
#             d = directionaleatoire()
#             gi.play(d)
#         resul += gi.score()
#     return resul


# def nextmoverandom(game, moves):
#     """
#     Utilisation de simulation aléatoire pour les 4 directions possibles
#     Retourne la direction ayant le meilleur score
#     """
#     n = 16
#     scores = [simulationaléatoire((game, n, 0)), simulationaléatoire((game, n, 1)), simulationaléatoire((game, n, 2)), simulationaléatoire((game, n, 3))]
#     return maxindice(scores)


# ------------------------------ Multiprocessing ----------------------------- #

# from multiprocessing import Pool
# def nextmoverandom(game, moves):
#     """
#     Utilisation de simulation aléatoire pour les 4 directions possibles
#     Retourne la direction ayant le meilleur score
#     """
#     n = 16
#     with Pool(4) as p:
#         scores = p.map(simulationaléatoire, [(game, n, 0), (game, n, 1), (game, n, 2), (game, n, 3)])
#     return maxindice(scores)


# g = Game2048()
# while True:
#     g.next_turn()
#     print(g.game)
#     g.play(nextmoverandom(g.game, g.moves))
#     print(g.game)

# import time
# a = time.time()
# affiche_distribution(list(evaluate_strategy(nextmoverandom, 2)))
# print("Temps :",time.time() - a)


# --------------------------------- Profiling -------------------------------- #

# if __name__ == '__main__':
#     a = time.time()
#     print(list(evaluate_strategy(nextmoverandom, 5)))
#     print(time.time()-a)


# cProfile.run('main()')


# with PyCallGraph(output=GraphvizOutput()):
#     main()
