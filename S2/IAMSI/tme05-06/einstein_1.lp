% Casse-tête logique (exercice 5)
% la maison 1 est la plus à gauche, 5 la plus à droite et 3 celle au centre.
pos(1..5).
% couleur des maisons
couleur(blanche;bleue;jaune;rouge;verte).
% ce que boit le résident
boisson(biere;cafe;eau;lait;the;).
% ce que fume le résident
fume(blend;bluemaster;dunhill;pallmall;princess).
% l'animal possédé par le résident
animal(chat;cheval;chien;oiseau;poisson).
% la nationalité du résident
nationalite(allemand;britannique;danois;norvegien;suedois).


1 { maison(P,C,B,F,A,N) : pos(P), couleurMaison(P, C), boissonMaison(P, B), fumeMaison(P, F), animalMaison(P, A), nationaliteMaison(P, N) } 1.

1 { couleurMaison(P, C) : pos(P), couleur(C) } 1.
1 { boissonMaison(P, B) : pos(P), boisson(B) } 1.
1 { fumeMaison(P, F) : pos(P), fume(F) } 1.
1 { animalMaison(P, A) : pos(P), animal(A) } 1.
1 { nationalite(P, N) : pos(P), nationalite(N) } 1.

couleurMaison(P, rouge) :- nationaliteMaison(P, britannique), pos(P).
nationaliteMaison(P, britannique) :- couleurMaison(P, rouge), pos(P).

animalMaison(P, chien) :- nationaliteMaison(P, suedois), pos(P).
nationaliteMaison(P, suedois) :- animalMaison(P, chien), pos(P).

boissonMaison(P, the) :- nationaliteMaison(P, danois), pos(P).
nationaliteMaison(P, danois) :- boissonMaison(P, the), pos(P).

couleurMaison(P1, verte) :- couleurMaison(P2, blanche), pos(P1), pos(P2), P1 < P2.

couleurMaison(P, verte) :- boissonMaison(P, cafe), pos(P).
boissonMaison(P, cafe) :- couleurMaison(P, verte), pos(P).

fumeMaison(P, pallmall) :- animal(P, oiseau), pos(P).
animal(P, oiseau) :- fumeMaison(P, pallmall), pos(P).

couleurMaison(P, jaune) :- fumeMaison(P, dunhill), pos(P).
fumeMaison(P, dunhill) :- couleurMaison(P, jaune), pos(P).


boissonMaison(3, lait).

nationaliteMaison(1, norvegien).

fumeMaison(P1, blend) :- animalMaison(P2, chat), pos(P1), pos(P2), P2-P1==1.

animalMaison(P1, cheval) :- fumeMaison(P2, dunhill), pos(P1), pos(P2), P2-P1==1.

fumeMaison(P,bluemaster) :- boissonMaison(P, biere), pos(P).
boissonMaison(P, biere) :- fumeMaison(P,bluemaster), pos(P).

nationalite(P,allemand) :- fumeMaison(P, princess), pos(P).
fumeMaison(P, princess) :- nationalite(P,allemand), f, pos(P).


nationaliteMaison(P1, norvegien) :- couleurMaison(P2, bleue), pos(P1), pos(P2), P2-P1==1.

fumeMaison(P1, blend) :- boissonMaison(P2, eau), pos(P1), pos(P2), P2-P1==1.


#show maison/6.