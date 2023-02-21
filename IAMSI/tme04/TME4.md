# IAMSI - TME4
## Prise en main de `glucose` et DIMACS

La théorie $\Sigma$ de l'exercice 3 du TD4.

```
c TD4 - Theorie 1
p cnf 6 7
1 2 3 0
1 2 -3 0
1 -2 3 4 0
1 -2 -4 5 0
-1 2 4 5 0
-1 2 4 -5 0
-1 -2 6
```

```
c This is glucose 4.2.1 --  based on MiniSAT (Many thanks to MiniSAT team)
c
c ========================================[ Problem Statistics ]===========================================
c |                                                                                                       |
c |  Number of variables:             6                                                                   |
c |  Number of clauses:               7                                                                   |
c |  Parse time:                   0.00 s                                                                 |
c |                                                                                                       |
c | Preprocesing is fully done
c |  Eliminated clauses:           0.00 Mb                                                                |
c |  Simplification time:          0.00 s                                                                 |
c |                                                                                                       |
c ========================================[ MAGIC CONSTANTS ]==============================================
c | Constants are supposed to work well together :-)                                                      |
c | however, if you find better choices, please let us known...                                           |
c |-------------------------------------------------------------------------------------------------------|
c | Adapt dynamically the solver after 100000 conflicts (restarts, reduction strategies...)               |
c |-------------------------------------------------------------------------------------------------------|
c |                                |                                |                                     |
c | - Restarts:                    | - Reduce Clause DB:            | - Minimize Asserting:               |
c |   * LBD Queue    :     50      |   * First     :   2000         |    * size <  30                     |
c |   * Trail  Queue :   5000      |   * Inc       :    300         |    * lbd  <   6                     |
c |   * K            :   0.80      |   * Special   :   1000         |                                     |
c |   * R            :   1.40      |   * Protected :  (lbd)< 30     |                                     |
c |                                |                                |                                     |
c ==================================[ Search Statistics (every  10000 conflicts) ]=========================
c |                                                                                                       |
c |          RESTARTS           |          ORIGINAL         |              LEARNT              | Progress |
c |       NB   Blocked  Avg Cfc |    Vars  Clauses Literals |   Red   Learnts    LBD2  Removed |          |
c =========================================================================================================
c last restart ## conflicts  :  0 0 
c =========================================================================================================
c restarts              : 1 (0 conflicts in avg)
c blocked restarts      : 0 (multiple: 0) 
c last block at restart : 0
c nb ReduceDB           : 0
c nb removed Clauses    : 0
c average learnt size   : 0
c nb learnts DL2        : 0
c nb learnts size 2     : 0
c nb learnts size 1     : 0
c conflicts             : 0              (0 /sec)
c decisions             : 1              (0.00 % random) (541 /sec)
c propagations          : 0              (0 /sec)
c nb reduced Clauses    : 0
c LCM                   : 0 / 0 
c CPU time              : 0.001847 s

s SATISFIABLE
v -1 2 -3 4 5 6 0
```

La théorie de l'exercice 4 du TD4 :

```
c ========================================[ Problem Statistics ]===========================================
c |                                                                                                       |
c |  Number of variables:             8                                                                   |
c |  Number of clauses:               6                                                                   |
c |  Parse time:                   0.00 s                                                                 |
c |                                                                                                       |
c | Preprocesing is fully done
c |  Eliminated clauses:           0.00 Mb                                                                |
c |  Simplification time:          0.00 s                                                                 |
c |                                                                                                       |
c ========================================[ MAGIC CONSTANTS ]==============================================
c | Constants are supposed to work well together :-)                                                      |
c | however, if you find better choices, please let us known...                                           |
c |-------------------------------------------------------------------------------------------------------|
c | Adapt dynamically the solver after 100000 conflicts (restarts, reduction strategies...)               |
c |-------------------------------------------------------------------------------------------------------|
c |                                |                                |                                     |
c | - Restarts:                    | - Reduce Clause DB:            | - Minimize Asserting:               |
c |   * LBD Queue    :     50      |   * First     :   2000         |    * size <  30                     |
c |   * Trail  Queue :   5000      |   * Inc       :    300         |    * lbd  <   6                     |
c |   * K            :   0.80      |   * Special   :   1000         |                                     |
c |   * R            :   1.40      |   * Protected :  (lbd)< 30     |                                     |
c |                                |                                |                                     |
c ==================================[ Search Statistics (every  10000 conflicts) ]=========================
c |                                                                                                       |
c |          RESTARTS           |          ORIGINAL         |              LEARNT              | Progress |
c |       NB   Blocked  Avg Cfc |    Vars  Clauses Literals |   Red   Learnts    LBD2  Removed |          |
c =========================================================================================================
c last restart ## conflicts  :  0 0 
c =========================================================================================================
c restarts              : 1 (0 conflicts in avg)
c blocked restarts      : 0 (multiple: 0) 
c last block at restart : 0
c nb ReduceDB           : 0
c nb removed Clauses    : 0
c average learnt size   : 0
c nb learnts DL2        : 0
c nb learnts size 2     : 0
c nb learnts size 1     : 0
c conflicts             : 0              (0 /sec)
c decisions             : 1              (0.00 % random) (685 /sec)
c propagations          : 0              (0 /sec)
c nb reduced Clauses    : 0
c LCM                   : 0 / 0 
c CPU time              : 0.001459 s

s SATISFIABLE
v 1 -2 -3 4 -5 -6 7 -8 0
```

L'exercice 2 du TD4 : 

```
c ========================================[ Problem Statistics ]===========================================
c |                                                                                                       |
c |  Number of variables:             5                                                                   |
c |  Number of clauses:               5                                                                   |
c |  Parse time:                   0.00 s                                                                 |
c |                                                                                                       |
c | Preprocesing is fully done
c |  Simplification time:          0.00 s                                                                 |
c |                                                                                                       |
c =========================================================================================================
Solved by simplification
c restarts              : 0 (0 conflicts in avg)
c blocked restarts      : 0 (multiple: 0) 
c last block at restart : 0
c nb ReduceDB           : 0
c nb removed Clauses    : 0
c average learnt size   : 0
c nb learnts DL2        : 0
c nb learnts size 2     : 0
c nb learnts size 1     : 0
c conflicts             : 0              (-nan /sec)
c decisions             : 0              (-nan % random) (-nan /sec)
c propagations          : 4              (inf /sec)
c nb reduced Clauses    : 0
c LCM                   : 0 / 0 
c CPU time              : 0 s

s UNSATISFIABLE
```

## Problème : organisation d'un championnat

Il y a $n_e$ équipes participantes. Les matchs se déroulent le mercredi ou le dimanche. Un championnat dure maximum $n_s$ semaines (2 matchs par semaine) soit $n_j = 2 \times n_s$ jours.

Une équipe joue un match par jour. Une équipe doit rencontre toutes les autres équipes une fois à domicile et une fois à l'extérieur.

**But** : produire un planning des matchs.

### Modélisation
Equipe : liste taille $n_e-1$
Jours : liste taille $n_j-1$, où les jours pairs = mercredi et les jours impairs = dimanche
$m_{j,x,y}$ : match entre $x$ (qui joue à domicile) et $y$ le jour $j$. On l'encode par $v_k$ avec $k=j \times n_e^2 + x \times n_e + y + 1$.


$C^{n_e}_2 \times 2 + n_j$
$C^{n_e}_2 \times n_j$


Nombre de variables propositionnelles utilisées :
- Si on considère en amont qu'une équipe ne peut pas jouer contre elle-même, il y a : $n_j \times n_e \times (n_e - 1)$ variables propositionnelles ;
- Sinon, il y a $n_j \times n_e^2$ variables propositionnelles.

```python
def codage(ne, nj, j, x, y):
    """int ** 5 -> int
    Encode une variable m_{j,x,y} par v_k.
    """
    return j * ne * ne + x * ne + y + 1

def decodage(k, ne):
    """int**2 -> int
    Décode la variable v_k en variable m_{j,x,y}.
    """
    y = (k - 1) % ne
    x = ((k - 1 - y) // ne) % ne
    j = (k - 1 - y - x * ne) // (ne * ne)
    return j, x, y
```

### Génération d'un planning de matchs
#### Contraintes de cardinalité

La contrainte "au moins une de ces variables est vraie", c'est-à-dire $\sum_{i \in \{1,\dots,n\}} v_i \ge 1$, s'encode ainsi: $v_1 \lor v_2 \lor \dots \lor v_n$

```python
def truc(variables):
    variables.append(0)
    return " ".join(map(str, variables))
```

La contrainte "au plus une de ces variables est vraie", c'est-à-dire $\sum_{i \in \{1,\dots,n\}} v_i \le 1$, s'encode par paires ou par encodage *bitwise*.
- par paires ($O(n^2)$ clauses) : $$\bigwedge_{1 \le i < n}^{i < j \le n}(\lnot x_i \lor \lnot x_j)$$
- par encodage *bitwise* ($O(nlogn)$ clauses, $O(n)$ variables supplémentaires)

```python
def truc2(variables):
    pass
```

#### Traduction du problème

Pour chaque jour, pour chaque équipe, une équipe joue au plus un match. On va donc utiliser la contrainte $\sum_{i \in \{1,\dots,n\}} v_i \le 1$ pour chaque jour, chaque équipe.
n*n-1/2 * n_e * n_j

pour une équipe donnée pour un jour donnée au plus 1