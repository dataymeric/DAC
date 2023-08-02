# Optimisation équitable
[@barthosdac](https://github.com/barthosdac) et [@dataymeric](https://github.com/dataymeric)</span>

Le programme sert à la résolution de problèmes d'optimisation équitable à l'aide de la programmation linéaire et du solveur Gurobi. 

## Composition

Le programme se compose de 5 modules :
- `linearise.py` : linéarisation des problèmes afin de les modéliser sous la forme d'un programme linéaire, utilisé par et pour les autres modules.
- `exo1.py` : applique les concepts de la linéarisation.
- `exo2.py` : résolution des problèmes de partage équitable de biens indivisibles entre plusieurs personnes.
- `exo3.py` : résolution des problèmes de sélection multicritère de projets.
- `exo4.py` : recherche d'un chemin robuste dans un graphe.

Le fichier `main.py` contient le code qui a servi à calculer les divers résultats obtenus dans le rapport à l'aide de ces modules.

## Usage
Chaque module possède un ou plusieurs exemples accessibles depuis la méthode `solveExemple()`.

Par exemple :
```python
import exo1, exo2, exo3, exo4

exo1.solveExemple()
exo2.solveExemple()
exo3.solveExemple()
exo4.solveExemple()
```
Cette fonction calcule et affiche les divers solutions optimales des exemples énoncés dans chaque partie du projet. 

De plus, le code a été agrémenté de documentation, qui, à l'aide de la commande `help(module.fonction)`, rappelle ce que fait une fonction, quels sont ses paramètres d'entrée et quelles sont les sorties. 

Le module `exo1` sert essentiellement à prendre en main Gurobi et mettre en application les concepts vus dans la première partie du projet, tels que la mise sous forme duale afin de résoudre $L(z)$ ou encore pour résoudre un problème d'optimisation équitable simple comme énoncé dans l'exemple de la partie 1.

Les 3 modules principaux (`exo2`, `exo3`, `exo4`) se composent et fonctionnent de manière analogue, à l'aide des fonctions suivantes :
- `solve` : fonction permettant de résoudre le problème linéarisé à l'aide du solveur Gurobi. 
- `affiche` : fonction permettant d'afficher les solutions optimales du problème.
- `temps` : fonction calculant l'évolution du temps de résolution du programme.
- `solveExemple` 

La principale différence se fait au niveau des différentes entrées.

## Linéarisation
Cette section concerne le module `linearise.py`.

```python
m, z = linearise(p, W)
```

Ce module est le coeur du projet. Il permet de linéariser une fonction de type $f(x)=\sum_i w_iz_{(i)}(x)$, où $z_{(i)}(x)$. Il prend en entrée $p$ (nombre d'objets dans le cas d'un problème multi-agents, nombre de projets dans le cas d'un problème multicritère, etc.) et $W$, un vecteur de poids positifs et décroissants.

En sortie, nous avons deux objets issus du solveur Gurobi, qui servent de point d'entrée aux autres modules.
- `m` : le modèle (linéarisé).
- `z` : les variables d'évaluation.

Il ne reste plus qu'à créer les variables de décision `x` et ajouter les contraintes supplémentaires sur les `x` et `z`en fonction du type d'optimisation (multi-agents, multicritère).

En enlevant le commentaire à la ligne 55 `m.setParam("TimeLimit", 300)`, il est possible d'ajouter un délai d'attente à notre modèle de 300 secondes, afin d'éviter d'avoir des grands temps de résolution.

## Partage équitable de biens indivisibles
Cette section concerne le module `exo2`.

```python
solve(W, U)
```
$W$ représente un vecteur de poids positifs et décroissants ($w_i \ge w_{i+1}, i=1,\dots,n-1$). Si ce n'est pas le cas, le programme s'arrête avec une valeur `ValueError`.

$U$ est la matrice des utilités $u_{ij}$ de l'objet $j$ pour l'agent $i$ . Elle doit être de taille $n \times p$ ($n$ agents, $p$ objets), au risque de soulever une valeur `IndexError`.

### Exemple
```python
W = [3, 2, 1]
U = [[325, 225, 210, 115, 75, 50],
     [325, 225, 210, 115, 75, 50],
     [325, 225, 210, 115, 75, 50]]
res = exo2.solve(W,U)
```
___
```python
affiche(r)
```
Permet d'afficher le résultat précédemment calculé.
### Exemple
```python
>>> exo2.affiche(res)
```
```
Partage équitable de 6 biens indivisibles entre 3 agents
-------------
L'agent 1 prend les objets 3, 5, 6.
Sa satisfaction est de 335.
-------------
L'agent 2 prend l'objet 1.
Sa satisfaction est de 325.
-------------
L'agent 3 prend les objets 2, 4.
Sa satisfaction est de 340.
-------------
```
____
```python
temps(N)
``` 
Calcule le temps (en secondes) d'évolution du programme en fonction d'une liste de $n$ agents dans `N` et de $p=5n$ objets. Attention, il est conseillé d'utiliser ce programme avec $n > 10$.

### Exemple
```python
N = range(2,6)
evo = exo2.temps(N)
print(evo)
```
```
[0.006165933609008789, 0.0853731632232666, 0.23780517578125, 0.67942316532135]
```
____

## Sélection multicritère de projets
Cette section concerne le module `exo3`.

```python
solve(W, U, C)
```
$W$ représente un vecteur de poids positifs et décroissants ($w_i \ge w_{i+1}, i=1,\dots,n-1$). Si ce n'est pas le cas, le programme s'arrête avec une valeur `ValueError`.

$U$ est la matrice des utilités $u_{ik}$ du projet $k$ pour satisfaire l'objectif $i$ . Elle doit être de taille $n \times p$ ($n$ objectifs, $p$ projets), au risque de soulever une valeur `IndexError`.

$C$ est le vecteur des coûts $c_k$ des projets, de taille $p$.

### Exemple
```python
W = [2, 1]
U = [[19, 6, 17, 2], [2, 11, 4, 18]]
C = [40, 50, 60, 50]
res = exo3.solve(W,U,C)
```
___
```python
affiche(r)
```
Permet d'afficher le résultat précédemment calculé.
### Exemple
```python
exo3.affiche(res)
```

```
Sélection équitable sous contrainte budgétaire
-------------------------------------
Solution optimale :
x1 = 1
x2 = 0
x3 = 0
x4 = 1
-------------------------------------
Vecteur d'utilité :
z1 = 21
z2 = 20
```
____
```python
temps(N,P,afficheTemps=False)
``` 
Calcule le temps d'évolution du programme en fonction d'une liste de $n$ objectifs dans `N` et d'une liste de $p$ projets dans `P`. Si `afficheTemps` est passé à `True` en paramètre, une sortie graphique des temps d'évolution est réalisée.

### Exemples
```python
evo = exo3.temps([2,5,10], [5,10,15,20])
print(evo)
```
```
[[0.006398487091064453, 0.011908221244812011, 0.018743014335632323, 0.017652201652526855],
 [0.0169236421585083, 0.01993708610534668, 0.030869603157043457, 0.04239866733551025],
 [0.029593539237976075, 0.05645716190338135, 0.08109097480773926, 0.08324108123779297]]
```
```python
exo3.temps([2,5,10], [5,10,15,20], afficheTemps=True)
```
![Sortie de exo3.temps(N,P,afficheTemps=True)](https://cdn.discordapp.com/attachments/1041730982086201394/1048238958217285632/Figure_2022-12-01_205132.png)

## Recherche d'un chemin robuste dans un graphe
Cette section concerne le module `exo4`.

```python
solve(T,W)
```
$W$ représente vecteur de poids positifs et décroissants ($w_i \ge w_{i+1}, i=1,\dots,n-1$). Si ce n'est pas le cas, le programme s'arrête avec une valeur `ValueError`.

$T$ est la matrice d'adjacence du graphe avec $p$ sommets et $n$ scénarios. Pour simuler l'infini, on prendra une valeur comme définie dans le rapport ($\forall s, infty>\sum_{(i,j)\in E} t_{ij}^s$). Il est recommandé d'utiliser `numpy.array` pour stocker la matrice.

### Exemple
```python
T = np.array([
  [[50,50],   [5,3],  [10,4],   [2,6], [50,50], [50,50], [50,50]],
  [[50,50], [50,50],   [4,2],   [1,3],   [4,6], [50,50], [50,50]],
  [[50,50], [50,50], [50,50], [50,50],   [3,1],   [1,2], [50,50]],
  [[50,50], [50,50],   [1,4], [50,50], [50,50],   [3,5], [50,50]],
  [[50,50], [50,50], [50,50], [50,50], [50,50], [50,50],   [1,1]],
  [[50,50], [50,50], [50,50], [50,50], [50,50], [50,50],   [1,1]],
  [[50,50], [50,50], [50,50], [50,50], [50,50], [50,50], [50,50]]])
W = [2, 1]
res = exo4.solve(T,W)
```
___
```python
affiche(r)
```
Permet d'afficher le résultat précédemment calculé.

### Exemple
```python
exo4.affiche(res)
```
```
Chemin pris :
a => b => e => g

Vecteur de temps :
t1=10
t2=10
```
____
```python
temps(N,afficheTemps=False)
``` 
Calcule l'impact de la pondération $w$ sur la robustesse du programme en fonction d'un nombre d'instances $N$. Si `afficheTemps` est passé à `True` en paramètre, une sortie graphique en nuage de points est réalisée en fonction de $\alpha=1,2,3,4,5$.

### Exemple
```python
evo = exo4.temps(20, afficheTemps=True)
```

----
```python
exo4.plusCourtsChemins()
``` 
Calcule puis affiche le plus court chemin de chacun des deux scénarios du graphe exemple (partie 4.1). Doit afficher le résultat suivant :

```
Scénario 1
Chemin pris :
a => d => c => f => g
-------------
Vecteur de temps :
t1=5

Scénario 2
Chemin pris :
a => c => e => g
-------------
Vecteur de temps :
t1=6
```