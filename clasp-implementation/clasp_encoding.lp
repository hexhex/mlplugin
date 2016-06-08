assigned_label_prob(X,L,P) :- label_prob(X,L,P), not n_assigned_label_prob(X,L,P).
n_assigned_label_prob(X,L,P) :- label_prob(X,L,P), not assigned_label_prob(X,L,P).

:- #count{L : assigned_label_prob(X,L,P)} != 1, object(X).

:~ assigned_label_prob(X,L,P). [P,X,L]

assigned_label(X,L) :- assigned_label_prob(X,L,P).





