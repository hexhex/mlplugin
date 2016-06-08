violated(X) :- assigned_label(X,wh), not in_wheel_position(X).
in_wheel_position(X2) :- contains_bottom(X1,X2), assigned_label(X1,c).
