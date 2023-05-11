On considère trois aéroports, Teg (Tegel, à Berlin), CDG (Charles-De-Gaulle, à Paris) et Bar (Barajas à Madrid). Il y a trois cargaisons C1, C2 et C3 qui sont toutes à Tegel à l’instant initial, ainsi que deux avions-cargos A1 et A2, eux aussi à Tegel et tous les deux vides. On veut convoyer les trois cargaisons à Barajas et laisser les deux avions à CDG, sachant que les avions-cargos ne peuvent charger qu’une seule cargaison à la fois.

On considère :
— les prédicats de type cargaison(X), avion(X), aeroport(X).
— le prédicat vide(X) qui indique que l’avion X est vide.
— les prédicats binaires situe(X, Y ) (l’objet X se trouve au lieu Y ), dans(X, Y ) (l’objet X est dans l’objet Y )
— les actions charger(X, Y, Z) (on charge la cargaison X dans l’avion Y à l’aéroport Z), voler(X, Y, Z) (l’avion X va de l’aéroport Y à l’aéroport Z) et decharger(X, Y, Z) (on décharge la cargaison X de l’avion Y à l’aéroport Z)


**Planification en ASP**

On reprend ici la programmation de la planification présentée dans l’exercice précédent, mais en ASP, en considérant successivement les sept composantes : (1) représentation des objets (2) représentation des états avec les fluents (3) expression des buts, (4) spécification des mouvements, qui se dissocie en une programmation des effets des actions sur les fluents et une programmation des conditions de déclenchement des actions (5) l’inertie (6) expression des contraintes et (7) la règle de génération.

1. Représentation des objets
Représenter en ASP les objets, à savoir les instants, les 3 cargaisons et les 2 avions. Noter que les instants sont bornés par une constante appelée last time.

Remarque : on choisit arbitrairement last time = 12.

2. Représentation des états Il s’agit maintenant de décrire ce que l’on appelle les fluents, c’est-à-dire les prédicats qui varient dans le temps.
— Quels sont les fluents dans ce problème ? Comment les représente-t-on ?
— Représenter l’état initial avec les fluents.

3. Représentation du but
Représenter le but à l’aide de contraintes d’intégrité. On rappelle que les trois cargaisons C1, C2 et C3 doivent se trouver à Barajas et les deux avions à CDG dans l’état final.

4. Programmation des actions
On représente les actions avec un prédicat binaire, action(X, T) o`u T correspond à l’instant du déclenchement du mouvement et X aux trois mouvements définis plus haut, charger(X, Y, Z), voler(X, Y, Z) et decharger(X, Y, Z).
— Programmer en ASP, pour l’action charger(X, Y, Z), ses effets sur les fluents.
— Programmer en ASP, pour l’action charger(X, Y, Z), ses conditions de déclenchement sous forme de contraintes.

5. Inertie
Donner, en ASP, les clauses qui spécifient l’inertie des trois fluents vide, dans et situe lorsque les littéraux ne sont pas affectés par l’action.

6. Spécification des contraintes
Programmer, en ASP, les contraintes, à savoir (i) que chaque avion n’a qu’une seule position à un moment donné et (ii) qu’il ne peut y avoir plus d’une cargaison à la fois dans un avion.

7. Règle de génération
Programmer en ASP une clause qui engendre les mouvements, sachant qu’il n’y en a pas plus d’un à chaque instant. Pour cela, on fera appel à une énumération contrainte, comme cela a été vu en cours.

Remarque : s’il y des opérateurs différents, on indique les différents termes de la disjonction avec des “ ;”. Ainsi, si l’on choisit une action unique parmi tous les mouvement1(A) pour tous les objets A et tous les mouvement2(B) pour tous les objets B, on écrira {action(mouvement1(A)) : objet(A); action(mouvement2(B)) : objet(A)} = 1

## Représentation ASP d’un problème STRIPS
Un problème exprimé en STRIPS contient un ensemble de prédicats (qui permettent de décrire des états), un ensemble de constantes ou d’objets sur lesquels portent les prédicats, un état initial et un but, tous deux exprimés par un ensemble de prédicats instanciés, et enfin, un ensemble d’actions définies sur ces prédicats. Les actions (éventuellement précisées par un ensemble de variables appelées paramètres) sont spécifiées par leur préconditions (PRE), et leurs effets, qui sont positifs (ADD) ou négatifs (DEL). PRE, ADD et DEL sont tous trois des ensembles de prédicats, dans lequels ne peuvent apparaitre que des variables présentes dans les paramètres de l’action. 

Cette absence de variables libres dans PRE, ADD et DEL, fait que l’on peut toujours examiner les élements des ces ensembles individuellement par rapport à l’action (ils ne sont pas liés entre eux autrement que par l’action elle-même). On peut donc traduire par des prédicats pred(P), action(A), pre(A,P), del(A,P), add(A,P), init(P) et but(P) tel qu’illustré ici sur l’exemple du monde des blocs. On utilise aussi des faits de typage pour identifier les objets et constantes ainsi que les instanciations possibles des prédicats ci-dessus.

### Exemple (incomplet)
``` 
%%% MONDE DES BLOCS %%%
%Déclaration des prédicats (domain)
pred(on(X,Y)):-block(X;Y).
pred(ontable(X)):-block(X).
pred(clear(X)):-block(X).
pred(handempty).
pred(holding(X)):-block(X).
%Déclaration des actions (domain)
action(pickup(X)):-block(X).
%preconditions
pre(pickup(X),clear(X)):-action(pickup(X)).
pre(pickup(X),ontable(X)):-action(pickup(X)).
pre(pickup(X),handempty):-action(pickup(X)).
%effects
del(pickup(X),clear(X)):-action(pickup(X)).
del(pickup(X),ontable(X)):-action(pickup(X)).
del(pickup(X),handempty):-action(pickup(X)).
add(pickup(X),holding(X)):-action(pickup(X)).
action(putdown(X)):-block(X).
...
action(stack(X,Y)):-block(X;Y).
...
action(unstack(X,Y)):-block(X;Y).
% déclaration des objets (problem) ou constantes (domain)
block(a;b;c;d).
% état initial
init(clear(a)).
init(clear(b)).
...
init(ontable(a)).
...
% but
but(on(d,c)).
but(on(c,b)).
but(on(b,a)).
```

Exercice 5 Planificateur STRIPS
Le but de cet exercice est d’écrire le moteur d’un planificateur STRIPS en ASP, en s’appuyant sur les prédicats définis à l’exercice précédent. On ajoute une horloge discrète avec un prédicat time(0..n). Le temps 0 correspond à la situation initiale et le but doit ˆetre atteint à l’horizon n : on teste avec des n croissants jusqu’à trouver un plan de taille minimale. Les différents T représentent des étapes, et non forcément un écoulement régulier du temps (on change d’étape chaque fois qu’il se passe quelque chose).

Pour relier les états et actions à cette horloge, on introduit aussi le prédicat holds(P,T), qui signifie que le prédicat P est vrai au temps T, et le prédicat perform(A,T) qui indique que l’on fait l’action A au temps T. Cela n’est possible que si les préconditions de A sont vérifiées au temps T, et les effets de l’action détermineront l’état au temps T+1.

1. Etat initial. Traduire en ASP l’état initial (si quelque chose est initialement vrai, cela veut dire que c’est vrai au temps 0 ).
2. Préconditions. Traduire en ASP le fait qu’une action ne peut se produire que si toutes ses préconditions sont vérifiées. On utilisera pour cela une contrainte d’intégrité, en exprimant que si on fait une action alors qu’une de ses préconditions n’est pas vérifiée, on a une contradiction.
3. Effets positifs. Traduire en ASP les effets positifs d’une action : si une action a lieu au temps T, au temps T + 1 tous ses effets positifs sont vrais.
4. Inertie et effets négatifs. Traduire en ASP le fait que ce qui est vrai au temps T, reste vrai au temps suivant, à moins qu’une action n’y ait mis fin (c’est à dire, à moins qu’une action réalisée au temps T ne l’ait eu comme effet négatif).
5. Choix d’action. Traduire en ASP le choix d’une et une seule action effectuée à chaque pas de temps (sauf le dernier).
6. Spécification du but. Traduire par une contrainte d’intégrité l’exigence que le but soit atteint au temps n.
7. Test. Tester ce moteur de planification avec les problèmes de la feuille de TDs traduits dans les exercices précédents.
8. Ecrire un programme ASPPLAN qui, à partir de deux fichiers PDDL définissant le domaine et le problème, génère un plan minimal. Il faut en particulier tester des valeurs de n croissantes jusqu’à trouver un plan, et mettre en forme l’answer set pour afficher lisiblement le plan obtenu.
9. Comparer la vitesse de votre programme avec SATPLAN.