
% Constantes %
% Last time = 5 %
time(0..8).
#const lasttime = 5.

% Nombre de blocs = 6 %
block(1..6).

location(B) :- block(B).
location(table).

% Génération: avec 1 poignet %
{move(BB, LL, T):block(BB),location(LL)}  1 :- time(T), T < lasttime.

% Définition %

% Effet du mouvement d'un bloc %
on(B, L, T+1) :- block(B), time(T), location(L), move(B, L, T), T < lasttime.

% Inertie %
on(B, L, T+1) :- block(B), time(T), location(L), on(B, L, T), not -on(B, L, T+1), T < lasttime.

% Position unique de chaque bloc %
-on(B, L1, T+1) :- block(B), time(T), location(L), location(L1), on(B, L, T+1), L != L1.

% Contraintes %
% Deux blocs ne peuvent pas se trouver au-dessus d'un méme bloc %
:- 2 {on(BB, B, T) : block(BB)}, block(B), block(BB), time(T).

% Un bloc ne peut étre mu si quelque chose se trouve au-dessus %
:- move(B, L, T), on(B1, B, T),block(B), block(B1), location(L), time(T).

% Un bloc ne peut étre mu sur un bloc occupé é contrainte ajoutée %
:- move(B, B2, T), on(B1, B2, T),block(B), block(B1), block(B2), time(T).

% Un bloc ne peut pas étre mu sur un bloc qui est en mouvement %
:- move(B, B1, T), move(B1, L, T), block(B), block(B1), location(L), time(T).

% Etat initial %
on(1, 2, 0).
on(2, table, 0).
on(3, 4, 0).
on(4, table, 0).
on(5, 6, 0).
on(6, table, 0).

% But %
:- not on(3, 2, lasttime).
:- not on(2, 1, lasttime).
:- not on(1, table, lasttime).
:- not on(6, 5, lasttime).
:- not on(5, 4, lasttime).
:- not on(4, table, lasttime).

% Affichage %
#show move/3.
%#show on/3.%