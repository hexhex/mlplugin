:~ assigned_label(X,wi), not in_window_position(X). [97077]
in_window_position(X2) :- contains(X1,X2), not contains_bottom(X1,X2), assigned_label(X1,c).
in_window_position(X2) :- contains(X1,X2), assigned_label(X1,b).
:~ assigned_label(X,wh), not in_wheel_position(X). [46408,X]
in_wheel_position(X2) :- contains_bottom(X1,X2), assigned_label(X1,c).
:~ assigned_label(X,trn), not in_trunk_position(X). [101077,X]
in_trunk_position(X2) :- contains(X1,X2), assigned_label(X1,tr).
:~ not assigned_label(X,trn), in_trunk_position(X). [11894,X]
in_trunk_position(X2) :- contains(X1,X2), assigned_label(X1,tr).
:~ assigned_label(X,c), not contains_car_part(X). [43657,X]
contains_car_part(X1) :- contains(X1,X2), assigned_label(X2,L), car_part(L).
:~ higher(X1,X2), assigned_label(X1,L1), assigned_label(X2,L2), small_object(L1), large_object(L2), X1 != X2. [60539,X1,X2,L1,L2]
:~ higher(X1,X2), assigned_label(X1,L1), assigned_label(X2,L2), midsized_object(L1), large_object(L2), X1 != X2. [62905,X1,X2,L1,L2]
:~ higher(X1,X2), assigned_label(X1,L1), assigned_label(X2,L2), small_object(L1), midsized_object(L2), X1 != X2. [36836,X1,X2,L1,L2]
