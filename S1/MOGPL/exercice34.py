# -*- coding: utf-8 -*-
import gurobipy as gp
import numpy as np
# import pylab as plt

xi = np.array([4,17,37,55,88,96])
yi = [11,25,46,48,65,71]
# A = np.array([xi, np.ones(6)])
# w = np.linalg.lstsq(A.T, yi)[0]
# line = w[0]*xi+w[1]
# plt.plot(xi, line, "r-", xi, yi, "o")

nbcont = 6 
nbvar = 8

# Range of plants and warehouses
lignes = range(nbcont)
colonnes = range(nbvar)

# Matrice des contraintes
# e_i
a = [[1, 0, 0, 0, 0, 0,  4, 1],
     [0, 1, 0, 0, 0, 0, 17, 1],
     [0, 0, 1, 0, 0, 0, 37, 1],
     [0, 0, 0, 1, 0, 0, 55, 1],
     [0, 0, 0, 0, 1, 0, 88, 1],
     [0, 0, 0, 0, 0, 1, 96, 1]]

# e_i+ - e_i-
# a = [[1,-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,  4, 1],
#      [0, 0, 1,-1, 0, 0, 0, 0, 0, 0, 0, 0, 17, 1],
#      [0, 0, 0, 0, 1,-1, 0, 0, 0, 0, 0, 0, 37, 1],
#      [0, 0, 0, 0, 0, 0, 1,-1, 0, 0, 0, 0, 55, 1],
#      [0, 0, 0, 0, 0, 0, 0, 0, 1,-1, 0, 0, 88, 1],
#      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,-1, 96, 1]]

# ei_coeff = [1,-1]
# np.concatenate((np.array(xi).reshape(6,1),np.ones(len(xi)).reshape(6,1)),axis=1)

# Second membre
b = [11, 25, 46, 48, 65, 71]

# Coefficients de la fonction objectif
c = np.concatenate((np.ones(6), np.zeros(2))) # [1,1,1,1,1,1,0,0]
# c = [1,-1,1,-1,1,-1,1,-1,1,-1,1,-1,0,0]

m = gp.Model("mogplex")     
        
# declaration variables de decision
x = []
for i in range(nbvar-2):
    x.append(m.addVar(vtype=gp.GRB.CONTINUOUS,
                      lb=0,
                      name="e%d" % (i+1)))
for i in range(2):
    x.append(m.addVar(vtype=gp.GRB.CONTINUOUS,
                      lb=-gp.GRB.INFINITY,
                      name="w%d" % (i+1)))

# maj du modele pour integrer les nouvelles variables
m.update()

obj = gp.LinExpr()
obj = 0
for j in colonnes:
    obj += c[j] * x[j]
        
# definition de l'objectif
m.setObjective(obj,gp.GRB.MINIMIZE)

# Definition des contraintes
for i in lignes:
    m.addConstr(gp.quicksum(a[i][j]*x[j] for j in colonnes) >= b[i],
                "Contrainte%d" % i)

# Resolution
m.optimize()

print("")                
print('Solution optimale:')
for j in colonnes:
    print('x%d'%(j+1), '=', x[j].x)
print("")
print('Valeur de la fonction objectif :', m.objVal)
