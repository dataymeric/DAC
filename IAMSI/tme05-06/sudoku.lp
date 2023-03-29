% Résolveur de Sudoku (exerice 3)
#const taille = 3.
pos(0..taille*taille-1).
n(1..taille*taille).

% instanciation des cases
1 {case(X, Y, N) : n(N)} 1 :- pos(X), pos(Y).

% pour avoir les régions de la grille (3x3 dans un sudoku de taille 9x9)
region(X1, Y1, X2, Y2) :- pos(X1), pos(X2), pos(Y1), pos(Y2),  (X1 / taille) == (X2 / taille), (Y1 / taille) == (Y2 / taille).

% contraintes
:- case(X1, Y, N), case(X2, Y, N), X1 != X2. % il ne peut y avoir le même chiffre sur une même ligne.
:- case(X, Y1, N), case(X, Y2, N), Y1 != Y2. % il ne peut y avoir le même chiffre sur une même colonne.
% il ne peut y avoir le même chiffre dans une région
:- case(X1, Y1, N), case(X2, Y2, N), region(X1, Y1, X2, Y2), X1 != X2, Y1 != Y2.

#show case/3.

%* Il n'existe qu'une solution pour le problème donné dans grille_sudoku. 
Solution : 
case(0,1,7) case(0,3,6) case(0,5,3) case(0,7,1) case(0,8,4) case(1,0,8) case(1,4,9) case(2,1,6) case(2,2,3) case(2,3,2) case(2,4,1) case(2,6,8) case(3,4,3) case(3,7,5) case(3,8,9) case(4,0,6) case(4,3,9) case(4,6,4) case(4,8,1) case(5,0,9) case(5,1,2) case(5,3,4) case(5,5,1) case(5,8,8) case(6,1,5) case(6,3,8) case(6,8,3) case(7,0,4) case(7,2,1) case(7,3,3) case(7,4,6) case(7,5,2) case(7,6,7) case(7,7,8) case(8,0,3) case(8,2,6) case(8,3,1) case(8,6,9) case(8,8,2) case(1,1,1) case(0,0,2) case(2,0,5) case(3,0,1) case(4,1,3) case(3,1,4) case(6,0,7) case(7,1,9) case(8,1,8) case(1,2,4) case(0,2,9) case(4,2,5) case(5,2,7) case(3,2,8) case(6,2,2) case(1,3,5) case(0,4,8) case(4,4,2) case(3,3,7) case(5,4,5) case(8,4,7) case(6,4,4) case(1,5,7) case(2,5,4) case(4,5,8) case(3,5,6) case(8,5,5) case(6,5,9) case(1,7,2) case(0,6,5) case(2,7,9) case(1,6,3) case(3,6,2) case(4,7,7) case(5,7,3) case(5,6,6) case(6,6,1) case(8,7,4) case(6,7,6) case(1,8,6) case(2,8,7) case(7,8,5)
*%