import numpy
import matplotlib.pyplot as plt
import time
from strategy2048 import Game2048, random_strategy, evaluate_strategy, nextmovescorebest


nb_test = 20


##############################
# Stratégie aléatoire

temps1 = time.time()
gen1 = evaluate_strategy(random_strategy, nb_test)
res1 = list(gen1)
res1.sort()
print("Stratégie aléatoire : " + str(res1))
print("Durée : " + str((time.time() - temps1)))
print("Moyenne =", numpy.mean(res1))
print("Proportion >= 2048 =", ((numpy.array(res1) >= 2048).sum() / len((res1))))
print()


##############################
# Notre stratégie

temps2 = time.time()
gen2 = evaluate_strategy(nextmovescorebest, nb_test)
res2 = list(gen2)
res2.sort()
print("Mystrategy : " + str(res2))
print("Durée : " + str((time.time() - temps2)))
print("Moyenne =", numpy.mean(res2))
print("Proportion >= 2048 =", ((numpy.array(res2) >= 2048).sum() / len((res2))))


#########################################
# Graphiques résultats

# fig, ax = plt.subplots(1, 1, figsize=(8, 4))
# ax.bar(numpy.arange(len(res1)), res1, color="b",
#        label="Stratégie aléatoire", width=0.4)
# ax.bar(numpy.arange(len(res2)) + 0.4, res2, color="orange",
#        label="mystrategy", width=0.4)
# ax.set_title("Compares two strategies for 2048.")
# ax.legend()
# plt.show()


def affiche_distribution(liste, nom):
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
    plt.xlabel("Score final")
    plt.title(nom)
    plt.show()


affiche_distribution(res1, "Distribution stratégie aléatoire")
affiche_distribution(res2, "Distribution mystrategy")
