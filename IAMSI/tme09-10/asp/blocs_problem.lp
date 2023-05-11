%%% MONDE DES BLOCS (PROBLEM) %%%
%%% Déclaration des objets (problem)
#const n=4.
time(0..n).
block(a;b;c;d).

%%% Etat initial (problem)
init(clear(b)).
init(ontable(a)).
init(on(b,a)).
init(clear(c)).
init(ontable(d)).
init(on(c,d)).
init(handempty).

%%% But (problem)
but(on(a,b)).
but(on(b,c)).
but(on(c,d)).
but(clear(a)).
but(ontable(d)).
but(handempty).

%%% Solution
% 1 unique AS

% perform(unstack(b,a),0)
% perform(stack(b,c),1)
% perform(pickup(a),2)
% perform(stack(a,b),3)