# -*- coding: utf-8 -*-
"""Application à la selection multicritère de projets.
========

Fonctions 
----------
solve
  Résolution d'un problème.
affiche
  Affichage de la solution optimale d'un problème.
solveExemple
  Résolution et affichage d'exemples.
temps
  Calcul de l'évolution du temps de résolution du programme.

Usage
----------
import exo3
help(exo3.solve)
help(exo3.affiche)
help(exo3.solveExemple)
help(exo3.temps)
"""
import numpy as np
import matplotlib.pyplot as plt
from time import time
from linearise import linearise
from gurobipy import *


def solve(W, U, C):
  """Résolution d'un problème de partage de sélection multicritère 
  de p projets.
  
  Paramètres
  ----------
  W : array d'entiers positifs de taille (n)
      Vecteur poids. Les composantes doivent être décroissantes.
  U : array d'entiers positifs de taille (n, p)
      Matrice des utilités des projets.
  C : array d'entiers de taille (p)
      Liste des coûts des p projets.
  
  Sortie
  ----------
  x : Matrice des valeurs de x à l'optimalité.
  z : Vecteur de satisfiabilité z à l'optimalité.
  """
  n = len(W)
  p = len(C)
  b = 0.5 * sum(C)
  m, z = linearise(p, W)

  # Ajout des k variables x
  x = []
  for k in range(p):
    x.append(m.addVar(vtype=GRB.BINARY, name=f"x{k+1}"))

  # Actualisation des variables du modèle
  m.update()

  # Ajout des contraintes sur z
  for i in range(n):
    m.addConstr(
      quicksum(U[i][k] * x[k] for k in range(p)) == z[i],
      f"Contrainte sur z{i+1}")

  # Ajout des contraintes en fonction des coûts des projets
  m.addConstr(
    quicksum(C[k] * x[k] for k in range(p)) <= b, f"Contrainte sur x")

  # Optimisation
  # m.write("exo3.lp")
  m.optimize()

  # Mise en forme du résultat x
  for k in range(p):
    x[k] = int(x[k].x)

  # Mise en forme des satisfactions z
  for i in range(n):
    z[i] = int(z[i].x)

  return (x, z)


def affiche(r):
  """Affiche le résultat d'une façon élégante.
  
  Paramètres
  ----------
  r : tuple
      Valeurs optimales de x et z pour un problème.

  Sortie
  ----------
  Affichage du résultat dans la console.
  """

  x, z = r
  n = len(z)
  p = len(x)

  print("\nSélection équitable sous contrainte budgétaire")
  print("-------------------------------------")
  print("Solution optimale :")
  for j in range(p):
    print(f"x{j + 1} = {x[j]}")
  print("-------------------------------------")
  print("Vecteur d'utilité :")
  for i in range(n):
    print(f"z{i + 1} = {z[i]}")


def solveExemple():
  """Résolution et affichage des solutions optimales des exemples 
  de la partie 3.1.
  """
  U = [[19, 6, 17, 2], [2, 11, 4, 18]]
  C = [40, 50, 60, 50]

  # premier exemple
  W = [2, 1]
  print(f"\nVecteur poids = {W} :")
  affiche(solve(W, U, C))

  # second exemple
  W = [10, 1]
  print(f"\nVecteur poids = {W} :")
  affiche(solve(W, U, C))

  # satisfaction moyenne
  W = [0.5, 0.5]
  print(f"\nVecteur poids = {W} :")
  affiche(solve(W, U, C))


def temps(N, P, afficheTemps=False):
  """Etudie l’évolution du temps de résolution de la sélection multicritère
  de projets en fonction de n objectifs et p projets.
      
  Paramètres
  ----------
  N : array de taille (n_N,)
      Valeurs prises par n (nombre d'objectifs).

  P : array de taille (n_P,)
      Valeurs prises par p (nombre de prbjets).

  afficheTemps : Booléen
      Si Vrai, affiche un graphique de l'évolution du temps de résolution 
      en millisecondes en fonction du nombre de projets.
  
  Sortie
  ----------
  T : array de taille (n_N * n_P,)
      Renvoie le temps moyen de résolution (en secondes) de 10 instances pour 
      chaque couple (n, p).

  Exemple
  ----------
  >>> exo3.temps([2,5,10],[5,10,15,20])
  """
  T = []

  for n in N:
    nlist = []
    for p in P:
      print(f"Exécution en cours pour le couple (n={n}, p={p})...")
      temps = []
      for _ in range(10):
        U = np.random.randint(30, size=(n, p))
        W = np.cumsum(np.random.randint(1, 30, size=n))[::-1]
        C = np.random.randint(30, size=p)
        t = time()
        solve(W, U, C)
        temps.append(time() - t)
      nlist.append(np.mean(temps))
    T.append(nlist)

  if afficheTemps:
    fig, ax = plt.subplots(figsize=(12, 7))
    for i in range(len(T)):
      ax.plot(P, np.array(T[i]) * 1000, label=f"n={N[i]}")

    plt.xlabel("Nombre de projets $p$", fontsize=14)
    plt.ylabel("Temps de résolution (ms)", fontsize=14)
    plt.xticks(P)
    plt.legend()
    plt.show()

  return T
