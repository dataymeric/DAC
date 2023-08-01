% Casse-tête logique (exercice 5)

% Domaines
maisons(1..5). % (1 tout à gauche, 5 tout à droite)
couleurs(rouge;verte;blanche;jaune;bleue).
nationalites(britannique;suedois;danois;norvegien;allemand).
animaux(chien;chats;chevaux;poissons;oiseaux).
boissons(cafe;the;lait;biere;eau).
cigarettes(pall_mall;dunhill;blend;bluemaster;princess).

% Génération
% Note : il y a une équivalence dans les contraintes.
% Couleur de la maison.
1 { couleur(Maison, Couleur) : couleurs(Couleur) } 1 :- maisons(Maison).
1 { couleur(Maison, Couleur) : maisons(Maison) } 1 :- couleurs(Couleur).
% Nationalité du propriétaire.
1 { nationalite(Maison, Nationalite) : nationalites(Nationalite) } 1 :- maisons(Maison).
1 { nationalite(Maison, Nationalite) : maisons(Maison) } 1 :- nationalites(Nationalite).
% Animal possédé par le propriétaire.
1 { animal(Maison, Animal) : animaux(Animal) } 1 :- maisons(Maison).
1 { animal(Maison, Animal) : maisons(Maison) } 1 :- animaux(Animal).
% Boisson préférée du propriétaire.
1 { boisson(Maison, Boisson) : boissons(Boisson) } 1 :- maisons(Maison).
1 { boisson(Maison, Boisson) : maisons(Maison) } 1 :- boissons(Boisson).
% Cigarettes préférées du propriétaire.
1 { fume(Maison, Cigarette) : cigarettes(Cigarette) } 1 :- maisons(Maison).
1 { fume(Maison, Cigarette) : maisons(Maison) } 1 :- cigarettes(Cigarette).

% Contrainte du voisin (càd, il est à gauche ou à droite).
a_cote(P1, P2) :- maisons(P1), maisons(P2), |P1-P2| == 1.

% 1. Le Britannique vit dans la maison rouge.
:- couleur(P1, rouge), nationalite(P2, britannique), P1 != P2.

% 2. Le Suédois garde un chien.
:- nationalite(P1, suedois), animal(P2, chien), P1 != P2.

% 3. Le Danois boit du thé.
:- nationalite(P1, danois), boisson(P2, the), P1 != P2.

% 4. La maison verte est à gauche de la maison blanche.
:- couleur(P1, verte), couleur(P2, blanche), P1 + 1 != P2.

% 5. Le propriétaire de la maison verte boit du café.
:- couleur(P1, verte), boisson(P2, cafe), P1 != P2.

% 6. La personne qui fume des Pall Mall possède des oiseaux.
:- fume(P1, pall_mall), animal(P2, oiseaux), P1 != P2.

% 7. Le propriétaire de la maison jaune fume des Dunhill.
:- fume(P1, dunhill), couleur(P2, jaune), P1 != P2.

% 8. La personne qui vit dans la maison qui se trouve exactement au centre boit du lait.
:- not boisson(3, lait).

% 9. Le Norvégien vit dans la première maison.
:- not nationalite(1, norvegien).

% 10. La personne qui fume des Blend vit à côté de celle qui possède des chats.
:- fume(P1, blend), animal(P2, chats), not a_cote(P1, P2).

% 11. La personne qui possède des chevaux vit à côté du fumeur de Dunhill.
:- fume(P1, dunhill), animal(P2, chevaux), not a_cote(P1, P2).

% 12. La personne qui fume des Bluemaster boit de la bière.
:- fume(P1, bluemaster), boisson(P2, biere), P1 != P2.

% 13. L’Allemand fume des Princess.
:- nationalite(P1, allemand), fume(P2, princess), P1 != P2.

% 14. Le Norvégien vit à côté de la maison bleue.
:- nationalite(P1, norvegien), couleur(P2, bleue), not a_cote(P1, P2).

% 15. La personne qui fume des Blend a un voisin qui boit de l’eau.
:- fume(P1, blend), boisson(P2, eau), not a_cote(P1, P2).

% La question est alors : qui possède des poissons ?
a_poissons(Nationalite) :- 
    nationalite(Maison, Nationalite), 
    animal(Maison, poissons). 

% Reconstruction
maison(Maison, Couleur, Nationalite, Animal, Boisson, Cigarette) :-
    maisons(Maison), 
    couleur(Maison, Couleur), 
    nationalite(Maison, Nationalite), 
    animal(Maison, Animal), 
    boisson(Maison, Boisson), 
    fume(Maison, Cigarette).

#show maison/6. 
#show a_poissons/1.

% Il n'existe qu'un unique answer set. La réponse à l'énigme est donc :

% -- Ordonnancement des maisons :
% maison(1, jaune, norvegien, chats, eau, dunhill)
% maison(2, bleue, danois, chevaux, the, blend)
% maison(3, rouge, britannique, oiseaux, lait, pall_mall)
% maison(4, verte, allemand, poissons, cafe, princess)
% maison(5, blanche, suedois, chien, biere, bluemaster)

% -- Réponse à la question :
% a_poissons(allemand)

% L'Allemand est donc celui qui possède les poissons !