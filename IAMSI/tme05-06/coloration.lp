% Coloration de graphe (exercice 4)
#const n=4.
nombre(1..n).

% à chaque sommet, on associe une couleur et un nombre (unique).
1 {couleur(X, C) : nombre(C)} 1 :- sommet(X).

% Contrainte : on ne peut affecter la même couleur à deux sommets X et Y 
% s'ils sont reliés entre eux. 
% Note : en ajoutant X != Y, on se permet d'avoir des graphes réfléxifs.
:- couleur(X, C), couleur(Y, C), relie(X, Y), nombre(C), X != Y.   

% trouver n tel qu'il soit minimal
% #minimize{C : nombre(C)}.

% le graphe G est instancié par l'intermédiaire d'un fichier supplémentaire
% `graphe.lp` (par exemple), où sommet(1..n) et relie(X, Y) représente les 
% arêtes entre deux sommets.
#show couleur/2.
