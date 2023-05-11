% Représentation des objets
#const last_time=12.
time(0..last_time).
cargaison(c1;c2;c3).
avion(a1;a2).
aeroport(teg;cdg;bar).

% Représentation des fluents
vide(Avion, T) :- avion(Avion), time(T).
dans(Cargaison, Avion, T) :- cargaison(Cargaison), avion(Avion), time(T).
situe(Avion, Aeroport, T) :- avion(Avion), aeroport(Aeroport), time(T).
situe(Cargaison, Aeroport,T) :- cargaison(Cargaison), aeroport(Aeroport), time(T).

% Etat initial
vide(a1,0).
vide(a2,0).
situe(c1,teg,0).
situe(c2,teg,0).
situe(c3,teg,0).
situe(a1,teg,0).
situe(a2,teg,0).

% Représentation du but
:- not dans(c1,a1,last_time).
% :- not situe(c2,bar),last_time).
% :- not situe(c3,bar),last_time).
% :- not situe(a1,bar),last_time).
% :- not situe(a2,bar),last_time).

% Programmation des actions
%% X, T)
% #define action/2.
charger(X,Y,Z, T) :- cargaison(X), avion(Y), aeroport(Z), time(T).
voler(X,Y,Z, T) :- avion(X), aeroport(Y), aeroport(Z), time(T).
decharger(X,Y,Z, T) :- cargaison(X), avion(Y), aeroport(Z), time(T).

%%%%%% charger(X,Y)
%%% Représentation des precond
% il n'est pas permis de charger un avion 
:-  charger(X,Y,Z,T),
    not vide(Y,T),              % si l'avion n'est pas vide
    not situe(X,Y,T),           % si la cargaison ne se situe pas à l'aéroport
    not situe(Y,Z,T),           % si l'avion ne se situe pas à l'aéroport
    T < last_time.

%%% Représentation des add
% si on charge un avion, alors la cargaison est dans l'avion
dans(X, Y, T+1) :- 
    charger(X, Y, Z, T),
    T < last_time.

%%% Représentation des del, `-` représente la "vraie" négation

% si on charge un avion, alors un avion n'est plus vide.
not vide(Y,T+1) :- 
    charger(X, Y, Z, T),
    T < last_time.

%%% Inertie
% si c'est vrai à T et que ce n'est pas faux à T+1, alors c'est vrai à T+1
vide(Avion, T+1) :- 
    vide(Avion, T), 
    not vide(Avion, T+1), 
    T < last_time. 

situe(Avion, Aeroport, T+1) :- 
    situe(Avion, Aeroport, T), 
    not situe(Avion, Aeroport, T+1), 
    T < last_time. 

situe(Cargaison, Aeroport, T+1) :- 
    situe(Cargaison, Aeroport, T), 
    not situe(Cargaison, Aeroport), T+1), 
    T < last_time. 

dans(Cargaison, Avion, T+1) :- 
    dans(Cargaison, Avion, T), 
    not dans(Cargaison, Avion), T+1), 
    T < last_time. 

1 { charger(X, Y, Z, T) : avion(Y), cargaison(X), aeroport(Z)} 1 :- time(T), T < last_time.











% % si on décharge un avion, alors l'avion est vide.
% -dans(Avion, Cargaison), T) :- decharger(Avion, Cargaison, Aeroport), T), avion(Avion), cargaison(Cargaison), aeroport(Aeroport), time(T), T < last_time.
% % si on vole d'un aéroport X vers un aéroport Y, alors on ne peut plus être situé à l'aéroport X
% -situe(Avion, AeroportX), T) :- voler(Avion, AeroportX, AeroportY), T), avion(Avion), aeroport(AeroportX), aeroport(AeroportY), time(T), T < last_time.

% vide(Avion), T+1) :- decharger(Avion, Cargaison, Aeroport), T), avion(Avion), cargaison(Cargaison), aeroport(Aeroport), time(T), T < last_time.
% situe(Avion, AeroportY), T+1) :- voler(Avion, AeroportX, AeroportY), T), avion(Avion), aeroport(AeroportX), aeroport(AeroportY), time(T), T < last_time.
% situe(Cargaison, Aeroport), T+1) :- voler(Avion, Cargaison, Aeroport), T), avion(Avion), cargaison(Cargaison), aeroport(Aeroport), time(T), T < last_time.