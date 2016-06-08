violated(X) :- assigned_label(X,wi), not in_window_position(X).
in_window_position(X2) :- contains(X1,X2), not contains_bottom(X1,X2), assigned_label(X1,c).
in_window_position(X2) :- contains(X1,X2), assigned_label(X1,b).
