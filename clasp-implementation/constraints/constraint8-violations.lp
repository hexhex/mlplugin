violated(X1,X2) :- higher(X1,X2), assigned_label(X1,L1), assigned_label(X2,L2), small_object(L1), midsized_object(L2), X1 != X2.
