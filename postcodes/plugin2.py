import dlvhex
import sklearn
from sklearn.externals import joblib
from sklearn import datasets


# load the model:
clf = joblib.load('digits.pkl')
digits = datasets.load_digits()


def prob_dist(p):

    probs = clf.predict_proba(digits.data[int(p.value())])

    for x in range(0, 10):
        dlvhex.output((x,int(probs[0][x] * 1000)))


# register all external atoms
def register():
    # prob_dist has a constant input parametrer and its output arity is 2
    dlvhex.addAtom("prob_dist", (dlvhex.CONSTANT, ), 2)
