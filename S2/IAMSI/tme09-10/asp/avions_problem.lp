%%% AVIONS (PROBLEM) %%%
%%% Déclaration des objets (problem)
#const n=12.
time(0..n).
avion(a1;a2).
cargaison(c1;c2;c3).
aeroport(teg;cdg;bar).

%%% Etat initial (problem)
init(situe(a1,teg)).
init(situe(a2,teg)).
init(situe(c1,teg)).
init(situe(c2,teg)).
init(situe(c3,teg)).
init(vide(a1)).
init(vide(a2)).

%%% But (problem)
but(situe(a1,cdg)).
but(situe(a2,cdg)).
but(situe(c1,bar)).
but(situe(c2,bar)).
but(situe(c3,bar)).

%%% Beaucoup de modèles  d'après clingo

% perform(charger(c1,a2,teg),0)
% perform(charger(c3,a1,teg),1) 
% perform(voler(a1,teg,bar),2) 
% perform(decharger(c3,a1,bar),3) 
% perform(voler(a1,bar,teg),4)
% perform(charger(c2,a1,teg),5) 
% perform(voler(a1,teg,bar),6) 
% perform(decharger(c2,a1,bar),7) 
% perform(voler(a2,teg,bar),8) 
% perform(decharger(c1,a2,bar),9) 
% perform(voler(a2,bar,cdg),10) 
% perform(voler(a1,bar,cdg),11) 

