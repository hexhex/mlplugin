sum(X) :- object(X), not contains_car_part(X).
contains_car_part(X1) :- contains(X1,X2), assigned_label(X2,L), car_part(L).
