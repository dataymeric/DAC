/* STRIPS programmé par Jean-Gabriel Ganascia */


test(Plan):- etat_initial(I), etat_final(F), resoudre(I, [F], Plan).

resoudre(_, [], []).
resoudre(Etat, [L|Buts], Plan) :- is_list(L), subset(L, Etat), !, marquer(1, Etat, Buts, Plan), resoudre(Etat,Buts,Plan).
resoudre(Etat, [L|Buts], Plan) :- is_list(L), !, subtract(L, Etat, LL), append(LL, [L|Buts], NButs), marquer(2, Etat, NButs, Plan), resoudre(Etat, NButs, Plan).
resoudre(Etat, [operateur(Op)|Buts], [Op|Plan]) :- !, appliquer_operateur(Etat, Op, NEtat), marquer(3, NEtat, Buts, Plan), resoudre(NEtat, Buts, Plan).
resoudre(Etat, [But|Buts], Plan) :- member(But, Etat), !,marquer(4, Etat, Buts, Plan), resoudre(Etat, Buts, Plan).
resoudre(Etat, [But|Buts], Plan) :- trouver_operateur(Etat, But, Op, P), intersection(P, Buts, []), operateur(Op, Preconds, _,_), marquer(5, Etat, [Preconds,operateur(Op),But|Buts], Plan), resoudre(Etat, [Preconds,operateur(Op),But|Buts], Plan).

marquer(N, E, B, P):- write('Appel prédicat résoudre '), write(N), nl, write('\tEtat: '), write(E), write('; Plan: '), write(P), nl, write('\tButs: '), write(B), nl.
trouver_operateur(Etat, But, Op, []) :- clause(operateur(Op, Preconds, _, AListe),Q), member(But, AListe), soustraction(Preconds, Etat,[]), call(Q), term_variables(Op,[]).
trouver_operateur(Etat, But, Op, [T|S]) :- clause(operateur(Op, Preconds, _, AListe),Q), member(But, AListe), soustraction(Preconds, Etat,[T|S]), call(Q), term_variables(Op,[]).

appliquer_operateur(Etat, Op, NEtat) :- operateur(Op, _, Dliste, Aliste), subtract(Etat, Dliste, DEtat), union(DEtat, Aliste, NEtat), write('Application opérateur '), write(Op), write('\n\tNouvel état: '), write(NEtat), nl.

soustraction([], _, []).
soustraction([X|L], D, LL) :- member(X, D), soustraction(L, D, LL).
soustraction([X|L], D, [X|LL]) :- soustraction(L, D, LL).

/************* Monde des blocs****************/
/*etat_initial([sur_table(a), sur_table(b), sur(c, a), libre(b), libre(c), poignet_vide, bloc(a), bloc(b), bloc(c)]).*/
etat_initial([sur_table(a), sur_table(b), sur_table(c), libre(a), libre(b), libre(c), poignet_vide, bloc(a), bloc(b), bloc(c)]).
/*etat_initial([sur_table(a), sur_table(b), sur(c, a), libre(b), libre(c), poignet_vide, bloc(a), bloc(b), bloc(c)]).*/


/*etat_final([sur_table(a), sur(c,b), sur(b, a), libre(c), poignet_vide]).*/
etat_final([sur_table(a), sur(b, a), sur(c ,b), libre(c), poignet_vide]).

operateur(deposer(B), [poignet_prise(B)], [poignet_prise(B)], [poignet_vide, sur_table(B),libre(B)]).
operateur(depiler(B, C), [poignet_vide, bloc(B), libre(B), sur(B, C)], [poignet_vide, libre(B), sur(B, C)], [poignet_prise(B), libre(C)]):- \+ B == C.
operateur(prendre(B), [poignet_vide, bloc(B), libre(B), sur_table(B)], [poignet_vide, libre(B), sur_table(B)], [poignet_prise(B)]).
operateur(empiler(B,C), [poignet_prise(B), bloc(B), bloc(C), libre(C)], [poignet_prise(B), libre(C)], [poignet_vide, sur(B, C),libre(B)]):- \+ B == C.
