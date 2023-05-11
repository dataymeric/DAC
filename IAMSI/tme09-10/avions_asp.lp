%%% Représentation des objets
#const last_time=12.
time(0..last_time).
cargaison(c1;c2;c3).
avion(a1;a2).
aeroport(teg;cdg;bar).

%%% Programmation des actions
%%% charger
{ charger(X,Y,Z,T) : cargaison(X), avion(Y), aeroport(Z) } 1 :- time(T), T < last_time.

% précond : il n'est pas permis de charger un avion 
:-  charger(X,Y,Z,T),
    not vide(Y,T),       % si l'avion n'est pas vide
    not situe(X,Z,T),    % si la cargaison ne se situe pas à l'aéroport
    not situe(Y,Z,T).    % si l'avion ne se situe pas à l'aéroport

% add : si on charge un avion, alors la cargaison est dans l'avion.
dans(X,Y,T+1) :- charger(X,Y,Z,T).

% del : si on charge un avion, alors un avion n'est plus vide et la cargaison ne se situe plus à l'aéroport.
% note : (Représentation des del, `-` représente la "vraie" négation)
-vide(Y,T+1) :- charger(X,Y,Z,T).
-situe(X,Z,T+1) :- charger(X,Y,Z,T).

%% voler
{ voler(X,Y,Z,T) : avion(X), aeroport(Y), aeroport(Z) } 1 :- time(T), T < last_time.

% precond : il  n'est pas permis de voler si l'avion ne se situe pas à l'aéroport de départ
:- voler(X,Y,Z,T), not situe(X,Y,T).

% add : si on vole d'un point Y à Z, alors l'avion se situe à Z à T+1.
situe(X,Z,T+1) :- voler(X,Y,Z,T).

% del : si on vole d'un point Y à Z, alors on ne se situe plus à Y à T+1.
-situe(X,Y,T+1) :- voler(X,Y,Z,T).

%% decharger
{ decharger(X,Y,Z,T) : cargaison(X), avion(Y), aeroport(Z) } 1 :- time(T), T < last_time.

% precond : il n'est pas permis de décharger un avion si la cargaison n'est pas dans l'avion et que l'avion ne se situe pas à l'aéroport.
:- decharger(X,Y,Z,T), not dans(X,Y,T), not situe(Y,Z,T).

% add : si on décharge un avion, la cargaison se situe à l'aéroport d'arrivée et l'avion est vide.
situe(X,Z,T+1) :- decharger(X,Y,Z,T).
vide(Y,T+1) :- decharger(X,Y,Z,T).

% del : si on décharge un avion, alors l'avion est vide, ie la cargaison n'est plus dans l'avion.
-dans(X,Y,T+1) :- decharger(X,Y,Z,T).

% Inertie :  si c'est vrai à T et que ce n'est pas faux à T+1, alors c'est vrai à T+1
vide(X,T+1) :- vide(X,T), not -vide(X,T+1), T < last_time.

dans(X,Y,T+1) :- dans(X,Y,T), not -dans(X,Y,T+1), T < last_time.

situe(X,Y,T+1) :- situe(X,Y,T), not -situe(X,Y,T+1), T < last_time.

%%% Etat initial
vide(a1,0).
vide(a2,0).
situe(c1,teg,0).
situe(c2,teg,0).
situe(c3,teg,0).
situe(a1,teg,0).
situe(a2,teg,0).

%%% Représentation du but
:- not situe(c1,bar,last_time).
:- not situe(c2,bar,last_time).
:- not situe(c3,bar,last_time).
:- not situe(a1,cdg,last_time).
:- not situe(a2,cdg,last_time).

#show charger/4.
#show voler/4.
#show decharger/4.