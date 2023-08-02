# -*- coding: utf-8 -*-
"""Application à la recherche d’un chemin robuste dans un graphe.
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
  Calcule l'impact de la pondération sur la robustesse.
plusCourtsChemins
  Calcule les plus courts chemin du graphe exemple.
  
Usage
----------
import exo4
help(exo4.solve)
help(exo4.affiche)
help(exo4.solveExemple)
help(exo4.temps)
help(exo4.plusCourtsChemins)
"""
import numpy as np
import matplotlib.pyplot as plt
from linearise import linearise
from gurobipy import *

G = np.array([[[-1, -1], [5, 3], [10, 4], [2, 6], [-1, -1], [-1, -1], [-1, -1]],
              [[-1, -1], [-1, -1], [4, 2], [1, 3], [4, 6], [-1, -1], [-1, -1]],
              [[-1, -1], [-1, -1], [-1, -1], [-1, -1], [3, 1], [1, 2], [-1, -1]],
              [[-1, -1], [-1, -1], [1, 4], [-1, -1], [-1, -1], [3, 5], [-1, -1]],
              [[-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [1, 1]],
              [[-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [1, 1]],
              [[-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1], [-1, -1]]])
# graphe exemple avec -1 pour l'infinité


def solve(T, W):
  """Résolution d'un problème de chemin robuste dans un graphe à plusieurs scénarios.

  Paramètres
  ----------
  T : matrice d'entiers de taille (p,p,n) (numpy.array conseillé)
      La matrice d'adjacence du graphe, en notant p le nombre de sommet 
      et n le nombre de scénarios.
  W : array d'entiers positifs de taille (n)
      Vecteur poids. Les composantes doivent être décroissantes.

  Sortie
  ----------
  x : Matrice des valeurs de x à l'optimalité.
  z : Vecteur de satisfiabilité z à l'optimalité.
  """
  T = np.array(
    T)  # au cas où l'utilisateur passe une liste au lieu d'un numpy.array
  p = len(T)
  n = len(T[0][0])

  m, z = linearise(p, W)

  # infty = T[T!=-1].sum() # On calcul l'infinité
  # T[T == -1] = infty # On remplace les -1

  # Ajout des p*p variables x
  x = []
  for i in range(p):
    x.append([])
    for j in range(p):
      x[-1].append(m.addVar(vtype=GRB.BINARY, lb=0, name=f"x{i+1},{j+1}"))

  # Actualisation des variables du modèle
  m.update()

  # Ajout des contraintes sur z
  for s in range(n):
    m.addConstr(
      quicksum(T[i][j][s] * x[i][j] for i in range(p)
               for j in range(p)) == -z[s], f"Contrainte sur z{s+1}")

  # Ajout de la contrainte sur le sommet 1
  m.addConstr(
    quicksum(x[0][j] for j in range(1, p)) == 1, f"Contrainte sur x1")
  # Ajout de la contrainte sur le sommet p
  m.addConstr(
    quicksum(x[i][p - 1] for i in range(0, p - 1)) == 1, f"Contrainte sur xp")
  # Ajout de la contrainte sur les autres sommets
  for i in range(1, p - 1):
    m.addConstr(
      quicksum(x[i][j] for j in range(p)) == quicksum(x[j][i]
                                                      for j in range(p)),
      f"Contrainte sur x{i+1}")

  # Optimisation
  # m.write("mymodel.mps")
  m.optimize()

  # Mise en forme du résultat x
  for i in range(p):
    for j in range(p):
      x[i][j] = int(x[i][j].x)

  # Mise en forme des temps t
  for i in range(n):
    z[i] = -int(z[i].x)

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

  print("Chemin pris :")
  i = 0
  while i != p - 1:
    print(chr(i + 97), end='')
    print(' => ', end='')
    i = np.argmax(x[i])
  print(chr(96+p))
  print("-------------")
  print("Vecteur de temps :")
  for i in range(n):
    print(f"t{i+1}={z[i]}")


def solveExemple():
  """Affiche le résultat optimal du graphe exemple.
  """
  T = G.copy()

  # On calcul l'infinité
  infty = T[T != -1].sum()
  # On remplace les -1
  T[T == -1] = infty

  # Premier exemple
  W = [2, 1]
  print(f"\nAvec les poids {W} :")
  affiche(solve(T, W))


def temps(N, afficheTemps=False):
  """Calcul les temps et peut les afficher.
  
  Paramètres
  ----------
  N : entier
    Nombre de matrices à générer (instances)

  Sortie
  ----------
  t : matrice (6,N,2) d'entiers
    t(i,j,s)=temps mis pour alpha=i+1 de la matrice j dans le scénario s

  Action
  ----------
  Si afficheTemps vrai, affiche les temps par alpha dans le plan (t1,t2)
  """
  p = len(G)
  n = len(G[0, 0])
  #creation des matrices T dans M
  M = []
  for k in range(N):
    M.append(np.random.randint(1, 40, size=(p, p, n)))
    #on calcul l'inifité
    infty = M[-1][G != -1].sum()
    #on remplace les -1
    M[-1][G == -1] = infty

  # Calcul des temps de résolution
  temps = []
  for alpha in range(1, 6):
    temps.append([])

    # Calcul des poids
    W = []
    for i in range(1, n + 1):
      W.append(((n - i + 1) / n)**alpha - ((n - i) / n)**alpha)

    # Résolution
    for T in M:
      t = solve(T, W)[1]
      temps[-1].append(t)

  # Si afficheTemps, représente les temps dans (t1,t2)
  if afficheTemps:
    tmin = np.min(temps)
    tmax = np.max(temps)
    for alpha in range(1, 6):
      plt.figure(alpha)
      plt.title(f"Nuage de temps pour alpha={alpha}")
      plt.xlabel("t1")
      plt.ylabel("t2")

      for t in temps[alpha - 1]:
        plt.scatter(t[0], t[1])

      plt.plot([tmin, tmax], [tmin, tmax], '--')

      #plt.savefig(f'{alpha}.png')
      plt.show()

  return temps


def plusCourtsChemins():
  """ Affiche les plus courts chemins des deux scénarios du graphe exemple.
  """
  p = len(G)
  for s in range(len(G[0,0])):
    T = G[:, :, s]

    infty = T[T != -1].sum() + 1
    # On remplace les -1
    T[T == -1] = infty

    m = Model("mogplex")
    m.Params.LogToConsole = 0  # désactive toutes les infos "inutiles" en console

    # Ajout des p*p variables x
    x = []
    for i in range(p):
      x.append([])
      for j in range(p):
        x[-1].append(m.addVar(vtype=GRB.BINARY, lb=0, name=f"x{i+1},{j+1}"))

    m.update()

    # Ajout de la contrainte sur le sommet 1
    m.addConstr(
      quicksum(x[0][j] for j in range(1, p)) == 1, f"Contrainte sur x1")
    # Ajout de la contrainte sur le sommet p
    m.addConstr(
      quicksum(x[i][p - 1] for i in range(0, p - 1)) == 1,
      f"Contrainte sur xp")
    # Ajout de la contrainte sur les autres sommets
    for i in range(1, p - 1):
      m.addConstr(
        quicksum(x[i][j] for j in range(p)) == quicksum(x[j][i]
                                                        for j in range(p)),
        f"Contrainte sur x{i+1}")

    #Ajout de l'objectif
    obj = LinExpr()
    obj = 0
    for i in range(p):
      for j in range(p):
        obj += x[i][j] * T[i][j]
    m.setObjective(obj, GRB.MINIMIZE)

    m.optimize()

    print(f"\nScénario {s+1}")
    affiche([[[int(x[i][j].x) for j in range(p)] for i in range(p)], [m.objVal]])

