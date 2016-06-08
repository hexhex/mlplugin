:~ assigned_label(X,trn), not in_trunk_position(X). [WEIGHT,X]
in_trunk_position(X2) :- contains(X1,X2), assigned_label(X1,tr).
