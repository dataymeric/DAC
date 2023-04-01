% Organisation de championnat (exercice 6)
#const ne = 3.       % Nombre d'équipes.
#const ns = 3.       % Nombre de semaines.
#const nj = 2 * ns.  % Nombre de jours.

equipe(1..ne).
jour(1..nj).

% Génération des matchs possibles
1 { match(Jour, Domicile, Exterieur) : jour(Jour) } 1 :- equipe(Domicile), equipe(Exterieur), Domicile != Exterieur.

% Chaque équipe ne peut jouer plus d'un match par jour.
% Chaque équipe doit rencontre l'ensemble des autres équipes une fois à domicile
% et une fois à l'extérieur, soit exactement 2 matchs par équipe adverse.
:- match(Jour, X, Y), match(Jour, X, Z), Y != Z.
:- match(Jour, Y, X), match(Jour, Z, X), Y != Z.
:- match(Jour, X, Y), match(Jour, Z, X).
:- match(J1, X, Y), match(J2, X, Y), J1 != J2.

#show match/3.

% Pour ne=3, ns=3, soit 6 jours, il y a 720 answer sets.

% Par exemple : 
% match(1,2,1) match(2,3,1) match(3,1,2) match(5,3,2) match(6,1,3) match(4,2,3)

% - Le premier jour, le match a lieu chez l'équipe 2 et joue contre l'équipe 1 ;
% - Le deuxième jour, le match a lieu chez l'équipe 3 et joue contre l'équipe 1 ;
% etc.