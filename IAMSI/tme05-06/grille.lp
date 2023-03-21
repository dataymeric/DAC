pos(0..8).
n(1..9).


subgrid(X, Y, A, B) :- pos(X), n(A), pos(Y), pos(B), X/3 == A/3, Y/3 == B/3.

case(0,1,7).
case(0,3,6).
case(0,5,3).
case(0,7,1).

:- case(X, Y, V), case(A, B, V), subgrid(X, Y, A, B), X != A, Y != B.
