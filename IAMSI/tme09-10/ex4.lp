% Représentation des objets
#const last_time=1.
time(0..last_time).
cargaison(c1;c2;c3).
avion(a1;a2).
aeroport(teg;cdg;bar).

% Représentation des fluents
holds(vide(a1),0).
holds(vide(a2),0).
holds(situe(c1,teg),0).
holds(situe(c2,teg),0).
holds(situe(c3,teg),0).
holds(situe(a1,teg),0).
holds(situe(a2,teg),0).

% Représentation du but
:- not holds(dans(c1,a1),last_time).
% :- not holds(situe(c2,bar),last_time).
% :- not holds(situe(c3,bar),last_time).
% :- not holds(situe(a1,bar),last_time).
% :- not holds(situe(a2,bar),last_time).

% Programmation des actions
%% action(X, T)
% #define action/2.

%%%%%% charger(X,Y)
%%% Représentation des precond

% il n'est pas permis de charger un avion si l'avion n'est pas vide
% :- action(charger(Avion,Cargaison,Aeroport),T), not holds(vide(Avion),T), avion(Avion), cargaison(Cargaison), aeroport(Aeroport), time(T), T < last_time.

% il n'est pas permis de charger un avion si la cargaison se situe à un aéroport différent d'où est stationné l'avion, càd, je ne peux charger un avion que si la Cargaison et l'Avion se situe au même Aeroport
% :- action(charger(Avion,Cargaison,Aeroport),T), holds(situe(Cargaison,Aeroport),T), holds(situe(Avion,Aeroport),T), avion(Avion), cargaison(Cargaison), aeroport(Aeroport), time(T), T < last_time.

% il n'est pas permis de charger un avion 
:-  action(charger(Avion,Cargaison,Aeroport),T),
    not holds(vide(Avion),T),                     % si l'avion n'est pas vide
    not holds(situe(Cargaison,Aeroport),T),       % si la cargaison ne se situe pas à l'aéroport
    not holds(situe(Avion,Aeroport),T),           % si l'avion ne se situe pas à l'aéroport
    avion(Avion), 
    cargaison(Cargaison),
    aeroport(Aeroport),
    time(T),
    T < last_time.

%%% Représentation des add
% si on charge un avion, alors la cargaison est dans l'avion
holds(dans(Avion, Cargaison), T+1) :- 
    action(charger(Avion, Cargaison, Aeroport), T),
    avion(Avion),
    cargaison(Cargaison),
    aeroport(Aeroport),
    time(T),
    T < last_time.

%%% Représentation des del, `-` représente la "vraie" négation

% si on charge un avion, alors un avion n'est plus vide.
-holds(vide(Avion),T+1) :- 
    action(charger(Avion, Cargaison, Aeroport), T),
    avion(Avion),
    cargaison(Cargaison), 
    eroport(Aeroport), 
    ime(T),
    T < last_time.

%%% Inertie
% si c'est vrai à T et que ce n'est pas faux à T+1, alors c'est vrai à T+1
holds(vide(Avion), T+1) :- 
    holds(vide(Avion), T), 
    -holds(vide(Avion), T+1), 
    avion(Avion), 
    time(T), 
    T < last_time. 

holds(situe(Avion, Aeroport), T+1) :- 
    holds(situe(Avion, Aeroport), T), 
    -holds(situe(Avion, Aeroport), T+1), 
    avion(Avion), 
    aeroport(Aeroport),
    time(T), 
    T < last_time. 

holds(situe(Cargaison, Aeroport), T+1) :- 
    holds(situe(Cargaison, Aeroport), T), 
    -holds(situe(Cargaison, Aeroport), T+1), 
    cargaison(Cargaison), 
    aeroport(Aeroport),
    time(T), 
    T < last_time. 

holds(dans(Cargaison, Avion), T+1) :- 
    holds(dans(Cargaison, Avion), T), 
    -holds(dans(Cargaison, Avion), T+1), 
    cargaison(Cargaison), 
    avion(Avion),
    time(T),
    T < last_time. 

1 { action(charger(Avion, Cargaison, Aeroport), T) : avion(Avion), cargaison(Cargaison), aeroport(Aeroport)} 1 :- time(T). % à chaque pas de temps je choisis une action














% % si on décharge un avion, alors l'avion est vide.
% -holds(dans(Avion, Cargaison), T) :- action(decharger(Avion, Cargaison, Aeroport), T), avion(Avion), cargaison(Cargaison), aeroport(Aeroport), time(T), T < last_time.
% % si on vole d'un aéroport X vers un aéroport Y, alors on ne peut plus être situé à l'aéroport X
% -holds(situe(Avion, AeroportX), T) :- action(voler(Avion, AeroportX, AeroportY), T), avion(Avion), aeroport(AeroportX), aeroport(AeroportY), time(T), T < last_time.

% holds(vide(Avion), T+1) :- action(decharger(Avion, Cargaison, Aeroport), T), avion(Avion), cargaison(Cargaison), aeroport(Aeroport), time(T), T < last_time.
% holds(situe(Avion, AeroportY), T+1) :- action(voler(Avion, AeroportX, AeroportY), T), avion(Avion), aeroport(AeroportX), aeroport(AeroportY), time(T), T < last_time.
% holds(situe(Cargaison, Aeroport), T+1) :- action(voler(Avion, Cargaison, Aeroport), T), avion(Avion), cargaison(Cargaison), aeroport(Aeroport), time(T), T < last_time.