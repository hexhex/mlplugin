import dlvhex
import sklearn
from sklearn.externals import joblib
from sklearn import datasets


# load the model:
clf = joblib.load('digit-model.pkl')
digits = datasets.load_digits()


def predict(o,p):

    probs = clf.predict_proba(digits.data[int(p.value())])
   
    options = []

    for x in dlvhex.getTrueInputAtoms():
        if x.tuple()[0] == o:
            options.append(x.tupleValues()[1])

    if options != []:
        ret = options[0]
        current_best = probs[0][int(options[0])]

        for x in range(1,len(options)-1):
            if probs[0][(options[x])] > current_best:
                ret = options[x]
                current_best = probs[0][(options[x])]

        # output the digit with the highest probability
        dlvhex.output((ret, ))
    else:
        dlvhex.output(("mismatch", ))



# register all external atoms
def register():
    # predict has a predicate and a constant input parametrer and its output arity is 1
    dlvhex.addAtom("predict", (dlvhex.PREDICATE, dlvhex.CONSTANT), 1)
