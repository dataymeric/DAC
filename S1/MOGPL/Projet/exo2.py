# -*- coding: utf-8 -*-
"""Application au partage équitable de biens indivisibles.
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
import exo2
help(exo2.solve)
help(exo2.affiche)
help(exo2.solveExemple)
help(exo2.temps)
"""
import numpy as np
from time import time
from linearise import linearise
from gurobipy import *


def solve(W, U):
  """Résolution d'un problème de partage équitable de biens indivisibles.
  
  Paramètres
  ----------
  W : array d'entiers positifs taille (n)
      Vecteur poids. Les composantes doivent être décroissantes.
  U : array d'entiers positifs taille (n, p)
      Matrice des utilités des objets.
  
  Sortie
  ----------
  x : Matrice des valeurs de x à l'optimalité.
  z : Vecteur de satisfiabilité z à l'optimalité.
  """
  n = len(W)
  p = len(U[0])
  m, z = linearise(p, W)

  # Ajout des n*p variables x
  x = []
  for i in range(n):
    x.append([])
    for j in range(p):
      x[-1].append(m.addVar(vtype=GRB.BINARY, lb=0, name=f"x{i+1},{j+1}"))

  # Actualisation des variables du modèle
  m.update()

  # Ajout des contraintes sur z
  for i in range(n):
    m.addConstr(
      quicksum(U[i][j] * x[i][j] for j in range(p)) == z[i],
      f"Contrainte sur z{i+1}")

  # Ajout des contraintes sur x
  for j in range(p):
    m.addConstr(
      quicksum(x[i][j] for i in range(n)) <= 1, f"Contrainte sur x{j+1}")

  # Optimisation
  # m.write("exo2.lp")
  m.optimize()

  # Mise en forme du résultat x
  for i in range(n):
    for j in range(p):
      x[i][j] = int(x[i][j].x)

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
  x, z = np.array(r, dtype="object")
  n = len(x)
  p = len(x[0])

  print(f"Partage équitable de {p} biens indivisibles entre {n} agents")
  print("-------------")
  for i in range(n):
    objets = np.nonzero(x[i])[0]
    if len(objets) == 0:
      print(f"L'agent {i+1} ne prend pas d'objet.")
    if len(objets) == 1:
      print(f"L'agent {i+1} prend l'objet {objets[0]+1}.")
    if len(objets) > 1:
      print(f"L'agent {i+1} prend les objets", end=" ")
      print(*np.nonzero(x[i])[0] + 1, sep=", ", end=".\n")
    print(f"Sa satisfaction est de {z[i]}.")
    print("-------------")


def solveExemple():
  """Résolution et affichage des solutions optimales des exemples 
  de la partie 2.1.
  """

  U = [[325, 225, 210, 115, 75, 50]] * 3

  # Premier exemple
  W = [3, 2, 1]
  print(f"\nAvec les poids {W} :")
  affiche(solve(W, U))

  # Second exemple
  W = [10, 3, 1]
  print(f"\nAvec les poids {W} :")
  affiche(solve(W, U))

  # Satisfaction moyenne
  W = [1 / 3, 1 / 3, 1 / 3]
  print(f"\nAvec les poids {W} :")
  affiche(solve(W, U))


def temps(N):
  """Etudie l’évolution du temps de résolution du partage équitable de bien indivisibles
  en fonction de n agents et p objets.
      
  Paramètres
  ----------
  N : array de taille (s)
      Valeurs prises par n (nombre d'agents).

  Sortie
  ----------
  T : array de taille (s)
      vecteur des |N| temps moyens de résolution en seconde.

  Exemple
  ----------
  >>> temps([5,10])
  """
  T = []
  for n in N:
    print(f"n={n}, p={5*n}")
    p = 5 * n
    temps = []
    for _ in range(10):
      U = np.random.randint(30, size=(n, p))
      W = np.cumsum(np.random.randint(1, 30, size=n))[::-1]
      t = time()
      solve(W, U)
      temps.append(time() - t)
    T.append(np.mean(temps))
  return T
