sum(X) :- object(X), not in_trunk_position(X).
in_trunk_position(X2) :- contains(X1,X2), assigned_label(X1,tr).
