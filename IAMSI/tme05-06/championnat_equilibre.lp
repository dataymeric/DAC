% Organisation de championnat "équilibré" (exercice 7)
#const ne = 3.             % Nombre d'équipes.
#const ns = 3.             % Nombre de semaines.
#const nj = 2 * ns.        % Nombre de jours.
#const nm = 2 * (ne - 1).  % Nombre de matchs joués pour chaque équipe.
#const pext = 50 / 100.    % Pourcentage de matchs joués à l'extérieur.
#const pdom = 40 / 100.    % Pourcentage de matchs joués à domicile.

equipe(1..ne).
semaine(1..ns).
jour(mercredi;dimanche).

% Génération des matchs possibles
1 { match(Semaine, Jour, Domicile, Exterieur) : semaine(Semaine), jour(Jour) } 1 :- equipe(Domicile), equipe(Exterieur), Domicile != Exterieur.

% Chaque équipe ne peut jouer plus d'un match par jour.
% Chaque équipe doit rencontre l'ensemble des autres équipes une fois à domicile
% et une fois à l'extérieur, soit exactement 2 matchs par équipe adverse.
:- match(S, J, X, Y), match(S, J, X, Z), Y != Z.
:- match(S, J, X, Y), match(S, J, Z, X).
:- match(S, J, Y, X), match(S, J, Z, X), Y != Z.
:- match(S, J1, X, Y), match(S, J2, X, Y), J1 != J2.

% Chaque équipe joue au moins pext % de ses matchs à l'extérieur les dimanches.
n {match(S, dimanche, Y, X) : semaine(S), equipe(X), equipe(Y) } :- n = pext * nm.

% Chaque équipe joue au moins pdom % de ses match à domicile les dimanches.
n {match(S, dimanche, X, Y) : semaine(S), equipe(X), equipe(Y) } :- n = pdom * nm.

% Aucune équipe ne joue plus de deux matchs consécutifs à l'extérieur.
:- match(S, mercredi, Y, X), match(S, dimanche, Z, X).

% Aucune équipe ne joue plus de deux match consécutifs à domicile.
:- match(S, mercredi, X, Y), match(S, dimanche, X, Y).

#show match/4.

% 384 answer sets pour ne=3, ns=3.

% Par exemple :
% match(1,dimanche,2,1) match(2,mercredi,3,1) match(3,mercredi,1,2) match(1,mercredi,3,2) match(3,dimanche,1,3) match(2,dimanche,2,3)