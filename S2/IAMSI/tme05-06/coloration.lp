% Coloration de graphe (exercice 4)

% Note : le graphe G est instancié par l'intermédiaire d'un fichier supplémentaire
% `graphe.lp` (par exemple), où sommet(1..d) représente les sommets et relie(X, Y) 
% représente les arêtes entre deux sommets.

#const n=4.    % nombre de couleurs
nombre(1..n).  % couleur associé à un sommet (fonction f)

% À chaque sommet, on associe une couleur et un nombre (unique).
1 {couleur(Sommet, Couleur) : nombre(Couleur)} 1 :- sommet(Sommet).

% Contrainte : on ne peut affecter la même couleur à deux sommets X et Y 
% s'ils sont reliés entre eux. 
% Note : en ajoutant X != Y, on se permet d'avoir des graphes réfléxifs.
:- couleur(X, Couleur), couleur(Y, Couleur), relie(X, Y), nombre(Couleur), X != Y.   

% Trouver le nombre de couleurs n tel qu'il soit minimal
% #minimize{Couleur : nombre(Couleur)}.

#show couleur/2.

% Avec un graphe de Colomb à 10 sommets, il y a 2280 answer sets pour n=4.