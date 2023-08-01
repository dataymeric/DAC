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


1 { maison(P,C,B,F,A,N) : pos(P), couleur(C), boisson(B), fume(F), animal(A), nationalite(N) } 1.


% base de faits
:- not 1 { maison(P, rouge, B, F, A, britannique) : pos(P) ; boisson(B) ; fume(F) ; animal(A) }.

:- not 1 {maison(P, C, B, F, chien, suedois) : pos(P) ; couleur(C) ; boisson(B) ; fume(F) }.

:- not 1 { maison(P, C, the, F, A, danois) : pos(P) ; couleur(C) ; fume(F) ; animal(A) }.

:- maison(P1, verte, B, F, A, N), maison(P2, blanche, B, F, A, N), pos(P1), pos(P2),P1<P2, boisson(B), fume(F), animal(A), nationalite(N).

:- not 1 { maison(P, verte, cafe, F, A, N) : pos(P) ; fume(F) ; animal(A) ; nationalite(N) }.

:- not 1 { maison(P, C, B, pallmall, oiseau, N) : pos(P) ; couleur(C) ; boisson(B) ; nationalite(N) }.

:- not 1 { maison(P, jaune, B, dunhill, A, N) : pos(P) ; boisson(B) ; animal(A) ; nationalite(N) }.

:- not 1 { maison(3, C, lait, F, A, N) : couleur(C) ; fume(F) ; animal(A) ; nationalite(N) }.

:- not 1 { maison(1, C, B, F, A, norvegien) : couleur(C) ; boisson(B) ; fume(F) ; animal(A) }.

:- maison(P1, C, B, blend, A, N), maison(P2, C, B, F, chat, N), pos(P1), pos(P2),(P2-P1)==1, couleur(C), boisson(B), fume(F), animal(A), nationalite(N).

:- maison(P1, C, B, blend, A, N), maison(P2, C, B, F, chat, N), pos(P1), pos(P2),(P1-P2)==1, couleur(C), boisson(B), fume(F), animal(A), nationalite(N).

:- maison(P1, C, B, F, cheval, N), maison(P2, C, B, dunhill, A, N), pos(P1), pos(P2),(P2-P1)==1,  couleur(C), boisson(B), fume(F), animal(A), nationalite(N).

:- maison(P1, C, B, F, cheval, N), maison(P2, C, B, dunhill, A, N), pos(P1), pos(P2),(P1-P2)==1, couleur(C), boisson(B), fume(F), animal(A), nationalite(N).

:- not 1 { maison(P, C, biere, bluemaster, A, N) : pos(P) ; couleur(C) ; animal(A) ; nationalite(N) }.

:- not 1 { maison(P, C, B, princess, A, allemand) : pos(P) ; couleur(C) ; boisson(B) ; animal(A) }.

:- maison(P1, C, B, F, A, norvegien), maison(P2, bleue, B, F, A, N), pos(P1), pos(P2),(P2-P1)==1,  couleur(C), boisson(B), fume(F), animal(A), nationalite(N).

:- maison(P1, C, B, F, A, norvegien), maison(P2, bleue, B, F, A, N), pos(P1), pos(P2),(P1-P2)==1,  couleur(C), boisson(B), fume(F), animal(A), nationalite(N).

:- maison(P1, C, B, blend, A, N), maison(P2, C, eau, F, A, N), pos(P1), pos(P2),(P2-P1)==1, couleur(C), boisson(B), fume(F), animal(A), nationalite(N).

:- maison(P1, C, B, blend, A, N), maison(P2, C, eau, F, A, N), pos(P1), pos(P2),(P1-P2)==1,  couleur(C), boisson(B), fume(F), animal(A), nationalite(N).

#show maison/6.