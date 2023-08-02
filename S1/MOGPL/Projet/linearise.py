# -*- coding: utf-8 -*-
"""Linéarisation d'une fonction f(x) de la forme w*z(x).
========

Fonctions 
----------
linearise
  Linéarise la fonction.

Usage
----------
import linearise
help(linearise.linearise)
"""
import numpy as np
from gurobipy import *

def linearise(p, W):
  """Linéarisation du problème comme démontré dans la partie 1.
  
  Paramètres
  ----------
  p : int
      Nombre d'objets.
  W : array d'entiers positifs de taille (n)
      Vecteur poids. Les composantes doivent être décroissantes.
  
  Sortie
  ----------
  m : gurobi object
      Modèle linéarisé.
  z : gurobi object
      Variables d'évaluation.
  
  Il faut ensuite créer les variables de décision x et ajouter les
  contraintes supplémentaires sur les x et z en fonction du type 
  d'optimisation (multi-agents, multicritère).

  Exceptions
  ----------
  ValueError
    Si les composantes du vecteur poids ne sont pas décroissantes.
  """
  if (sorted(np.array(W), reverse=True) != np.array(W)).any():
    raise ValueError("Les composantes du vecteur poids 'W' doivent être décroissantes.")
    
  n=len(W)
  # Définition des w'
  Wprime = []
  for k in range(n - 1):
    Wprime.append(W[k] - W[k + 1])
  Wprime.append(W[-1])

  m = Model("mogplex")
  # m.setParam("TimeLimit", 300) # time-out à 300 secondes
  m.Params.LogToConsole = 0  # désactive toutes les infos "inutiles" en console

  # Ajout des vars z
  z = []
  for i in range(n):
    z.append(m.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name=f"z{i+1}"))

  # Ajout des vars b
  b = []
  for k in range(n):
    b.append([])
    for i in range(n):
      b[-1].append(m.addVar(vtype=GRB.CONTINUOUS, lb=0, name=f"b{k+1},{i+1}"))

  # Ajout des vars r
  r = []
  for k in range(n):
    r.append(m.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name=f"r{k+1}"))

  m.update()

  # Création de la fonction objective
  obj = LinExpr()
  obj = 0
  for k in range(n):
    Sb = LinExpr()
    Sb = 0
    for i in range(n):
      Sb += b[i][k]
    obj += Wprime[k] * ((k+1) * r[k] - Sb)

  # Définition de l'objectif
  m.setObjective(obj, GRB.MAXIMIZE)

  # Définition des contraintes de bik
  for k in range(n):
    for i in range(n):
      m.addConstr(r[k] - b[i][k] <= z[i], f"Contrainte1 : {k},{i}")

  return m, z
