import numpy
import matplotlib.pyplot as plt
import time

from strategy2048 import Game2048, random_strategy, evaluate_strategy, nextmovescorebest


##############################
# Stratégie aléatoire


temps1 = time.time()
gen1 = evaluate_strategy(random_strategy, 100)
res1 = list(gen1)
res1.sort()
print("Stratégie aléatoire : " + str(res1))
print("Durée : " + str((time.time() - temps1)))
print("proportion >= 2048 =", ((numpy.array(res1) >= 2048).sum() / len((res1))))
print()

##############################
# Notre stratégie

temps2 = time.time()
gen2 = evaluate_strategy(nextmovescorebest, 100)
res2 = list(gen2)
res2.sort()
print("Notre stratégie : " + str(res2))
print("Durée : " + str((time.time() - temps2)))
print("proportion >= 2048 =", ((numpy.array(res2) >= 2048).sum() / len((res2))))


#########################################
# Finaly plots the gains obtained by the two strategies.

fig, ax = plt.subplots(1, 1, figsize=(8, 4))
ax.bar(numpy.arange(len(res1)), res1, color="b",
       label="aléatoire", width=0.4)
ax.bar(numpy.arange(len(res2)) + 0.4, res2, color="orange",
       label="notre stratégie", width=0.4)
ax.set_title("Compares two strategies for 2048.")
ax.legend()

plt.show()
