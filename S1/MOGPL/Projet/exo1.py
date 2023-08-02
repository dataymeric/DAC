# -*- coding: utf-8 -*-
"""Mise en application de la linéarisation.
========

Fonctions 
----------
calculL
  Résolution de L(z).
solveExemple
  Résolution et affichage d'exemples.

Usage
----------
import exo1
help(exo1.calculL)
help(exo1.solveExemple)
"""
from linearise import linearise
from gurobipy import *


def calculL(z):
  """Résolution de L(z) de la partie 1.2

  Paramètres
  ----------
  z : vecteur L(z)

  Sortie
  ----------
  L : composantes du vecteur L(z) 
  """
  n = len(z)
  L = []

  for k in range(n):  #calcul de Lk
    m = Model("mogplex")
    m.Params.LogToConsole = 0

    # Ajout des variables
    r = m.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name="r")
    b = []
    for i in range(n):
      b.append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name=f"b{i+1}"))

    m.update()

    # Création de la fonction objective
    obj = LinExpr()
    obj = 0
    Sb = 0
    for i in range(n):
      Sb += b[i]
    obj += (k + 1) * r - Sb

    m.setObjective(obj, GRB.MAXIMIZE)

    for i in range(n):
      m.addConstr(r - b[i] <= z[i], f"Contrainte1 : {i+1}")

    m.optimize()
    L.append(m.objVal)

  return L


def solveExemple():
  """Résolution et affichage des solutions optimales de l'exemple de la 
  partie 1.
  """
  n = 2
  p = 5
  W = [2, 1]

  m, z = linearise(p, W)

  # Ajout des variables x
  x = []
  for k in range(p):
    x.append(m.addVar(vtype=GRB.BINARY, lb=0, name=f"x{k+1}"))

  # Actualisation des variables du modèle
  m.update()

  # Ajout des contraintes concernant x
  m.addConstr(5 * x[0] + 6 * x[1] + 4 * x[2] + 8 * x[3] + x[4] == z[0],
              f"Contrainte sur z1")
  m.addConstr(3 * x[0] + 8 * x[1] + 6 * x[2] + 2 * x[3] + 5 * x[4] == z[1],
              f"Contrainte sur z2")

  m.addConstr(x[0] + x[1] + x[2] + x[3] + x[4] == 3, f"Contrainte sur x")

  # Optimisation
  m.optimize()

  # Affichage de la solution
  print("------------")
  print("Solution optimale")
  for k in range(p):
    print('x%d' % (k), '=', int(x[k].x))
  print("------------")
  print("Satisfaction")
  for i in range(n):
    print(f"z{i} = {int(z[i].x)}")
