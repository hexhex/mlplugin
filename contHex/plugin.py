import dlvhex
import json
from sklearn.externals import joblib

def predict(classifier_file,features_file,additional_features,omit_classes):
	f = open(features_file.value().strip('"'), 'r')
	X_test = json.load(f)
	f.close()
	model = joblib.load(classifier_file.value().strip('"'))
	dlvhex.output((model.predict(X_test)[0], 3))

def register():
    prop = dlvhex.ExtSourceProperties()
    prop.setFunctional(True)
    dlvhex.addAtom("predict", (dlvhex.CONSTANT, dlvhex.CONSTANT, dlvhex.PREDICATE, dlvhex.PREDICATE), 2, prop)
