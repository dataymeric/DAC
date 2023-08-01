%%% AVIONS (DOMAIN) %%%
%%% Déclaration des prédicats (domain)
pred(situe(X,Y)) :- avion(X),aeroport(Y).
pred(situe(X,Y)) :- cargaison(X),aeroport(Y).
pred(dans(X,Y)) :- cargaison(X),avion(Y).
pred(vide(X)) :- avion(X).

%%% Déclaration de l'action charger
action(charger(X,Y,Z)) :- cargaison(X), avion(Y), aeroport(Z).

% Préconditions
pre(charger(X,Y,Z),situe(X,Z)) :- action(charger(X,Y,Z)).
pre(charger(X,Y,Z),situe(Y,Z)) :- action(charger(X,Y,Z)).
pre(charger(X,Y,Z),vide(Y)) :- action(charger(X,Y,Z)).

% Effets
del(charger(X,Y,Z),situe(X,Z)) :- action(charger(X,Y,Z)).
del(charger(X,Y,Z),vide(Y)) :- action(charger(X,Y,Z)).
add(charger(X,Y,Z),dans(X,Y)) :- action(charger(X,Y,Z)).

%%% Déclaration de l'action voler
action(voler(X,Y,Z)) :- avion(X), aeroport(Y), aeroport(Z).

% Préconditions
pre(voler(X,Y,Z),situe(X,Y)) :- action(voler(X,Y,Z)).

% Effets
del(voler(X,Y,Z),situe(X,Y)) :- action(voler(X,Y,Z)).
add(voler(X,Y,Z),situe(X,Z)) :- action(voler(X,Y,Z)).

%%% Déclaration de l'action decharger
action(decharger(X,Y,Z)) :- cargaison(X), avion(Y), aeroport(Z).

% Préconditions
pre(decharger(X,Y,Z),dans(X,Y)) :- action(decharger(X,Y,Z)).
pre(decharger(X,Y,Z),situe(Y,Z)) :- action(decharger(X,Y,Z)).

% Effets
del(decharger(X,Y,Z),dans(X,Y)) :- action(decharger(X,Y,Z)).
add(decharger(X,Y,Z),situe(X,Z)) :- action(decharger(X,Y,Z)).
add(decharger(X,Y,Z),vide(Y)) :- action(decharger(X,Y,Z)).