pos(0..8).
n(1..9).
border(0,3,6);

{case(X, Y, N): n(N)} 1 :- pos(X), pos(Y).

subgrid(X, Y, A, B) :- pos(X), pos(A), pos(Y), pos(B), X/3 == A/3, Y/3 == B/3.
% je pense que ça marche pas pcq pos et n sont pas sur le même intervalle


:- case(X1, Y, N), case(X2, Y, N), X1 != X2. 
:- case(X, Y1, N), case(X, Y2, N), Y1 != Y2.
:- case(X, Y, V), case(A, B, V), subgrid(X, Y, A, B), X != A, Y != B.

#show case/3.