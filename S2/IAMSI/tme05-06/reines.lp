% n(8). % nombre de reines
#const n = 12.
pos(1..n). % position

% n { reine(X, Y) : pos(X), pos(Y) } n. % place les reines sur l'échiquier (aucune contrainte)

% :- not reine(1, 1). % reine en (1, 1) : 4 solutions (pour n = 8)
% :- reine(4, 4). % il ne peut pas y avoir de reine en (4, 4) : 84 (pour n = 8)

1 { reine(X, Y) : pos(Y) } 1 :- pos(X). % place les reines uniquement sur des colonnes.


:- reine(X1, Y), reine(X2, Y), X1 != X2, pos(X1 ; X2 ; Y). % deux reines ne peuvent se trouver sur une même ligne
% :- reine(X, Y1), reine(X, Y2), Y1 != Y2, pos(X ; Y1 ; Y2). % deux reines ne peuvent se trouver sur une même colonne
% interdiction des prises en diagonales
:- reine(X1, Y1), reine(X2, Y2), (X1, Y1) != (X2, Y2), X1 + Y1 == X2 + Y2, pos(X1 ; X2 ; Y1 ; Y2).
:- reine(X1, Y1), reine(X2, Y2), (X1, Y1) != (X2, Y2), X1 - Y1 == X2 - Y2, pos(X1 ; X2 ; Y1 ; Y2).

% #hide pos/1.
#show reine/2.

% avec reines = 5, 10 modèles.
% avec reines = 6, 10 modèles.
% avec reines = 8, 92 modèles.
% avec reines = 10, 724 modèles.
% avec reines = 12, 14 200 modèles.