# Copyright 2013, Gurobi Optimization, Inc.

# from gurobipy import *
import gurobipy as gp

nbcont=4 
nbvar=2

# Range of plants and warehouses
lignes = range(nbcont)
colonnes = range(nbvar)

# Matrice des contraintes
a = [[1,0],
     [0,1],
     [1,2],
     [2,1]]

# Second membre
b = [8, 6, 15, 18]

# Coefficients de la fonction objectif
c = [4, 3]

m = gp.Model("mogplex")     
        
# declaration variables de decision
x = []
for i in colonnes:
    x.append(m.addVar(vtype=gp.GRB.CONTINUOUS, lb=0, name="x%d" % (i+1)))

# maj du modele pour integrer les nouvelles variables
m.update()

obj = gp.LinExpr();
obj = 0
for j in colonnes:
    obj += c[j] * x[j]
        
# definition de l'objectif
m.setObjective(obj,gp.GRB.MAXIMIZE) # maximisation

# Definition des contraintes
for i in lignes:
    m.addConstr(gp.quicksum(a[i][j]*x[j] for j in colonnes) <= b[i],
                "Contrainte%d" % i)

# Resolution
m.optimize()

print("")                
print('Solution optimale:')
for j in colonnes:
    print('x%d'%(j+1), '=', x[j].x)
print("")
print('Valeur de la fonction objectif :', m.objVal)

   
