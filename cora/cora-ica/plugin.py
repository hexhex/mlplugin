import dlvhex
import numpy as np
import pandas as pd
import json
from sklearn.externals import joblib

def predict(p,n1,n2,n3,n4,n5,n6,n7):
	print "start"
	df = pd.read_table("cora.content", header=None)

	f = open("data.txt", 'r')
	X_test = json.load(f)
	f.close()

	attributes = X_test[int(p.value())]

	attributes[1433] += int(n1.value())
	attributes[1434] += int(n2.value())
	attributes[1435] += int(n3.value())
	attributes[1436] += int(n4.value())
	attributes[1437] += int(n5.value())
	attributes[1438] += int(n6.value())
	attributes[1439] += int(n7.value())

	model = joblib.load('papers.pkl')
	dlvhex.output((model.predict(attributes)[0],))
	print "stop"

def register():
    prop = dlvhex.ExtSourceProperties()
    prop.setFunctional(True)
    dlvhex.addAtom("predict", (dlvhex.CONSTANT, dlvhex.CONSTANT,dlvhex.CONSTANT,dlvhex.CONSTANT,dlvhex.CONSTANT,dlvhex.CONSTANT,dlvhex.CONSTANT,dlvhex.CONSTANT), 1, prop)
