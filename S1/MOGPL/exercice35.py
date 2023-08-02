# -*- coding: utf-8 -*-
import gurobipy as gp

# Matrice des contraintes
a = [[1,2,3],
     [3,1,1]]

# Second membre
b = [8, 5]

# Coefficients de la fonction objectif
c = [7, 3, 4]

nbcont = len(b)
nbvar = len(a[0])

# Range of plants and warehouses
lignes = range(nbcont)
colonnes = range(nbvar)

m = gp.Model("mogplex")     

# declaration variables de decision
x = []
for i in colonnes:
    x.append(m.addVar(vtype=gp.GRB.INTEGER, lb=0, name="x%d" % (i+1)))

# maj du modele pour integrer les nouvelles variables
m.update()

obj = gp.LinExpr()
obj = 0
for j in colonnes:
    obj += c[j] * x[j]
        
# definition de l'objectif
m.setObjective(obj,gp.GRB.MINIMIZE) # minimisation

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