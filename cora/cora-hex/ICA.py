import numpy as np
import pandas as pd
import json
from copy import deepcopy
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib

def init_nb_counts(data,targets,pred,relations):
	nb_counts = np.zeros((len(data), len(targets)))

	for relation in relations:
		if pred[relation[1]] != -1:
			nb_counts[relation[0]][pred[relation[1]]] += 1
		if pred[relation[0]] != -1:
			nb_counts[relation[1]][pred[relation[0]]] += 1

	return nb_counts


def update_nb_counts(data,pred,rels):
	for rel in rels:
		data[rel[0]][1433+pred[rel[1]]] += 1
		data[rel[1]][1433+pred[rel[0]]] += 1


np.set_printoptions(edgeitems=100)


### PREPROCESSING ###

df = pd.read_table("cora.content", header=None)
rels = pd.read_table("cora.cites", header=None)

targets = df[1434].unique()

map_to_int = {name: n for n, name in enumerate(targets)}
df[1434] = df[1434].replace(map_to_int)

data = df.as_matrix()
data = data[0:300]

relation_list = rels.as_matrix().tolist()

nodes = data[:,0:1].tolist()


relations = []

for relation in relation_list:
	if [relation[0]] in nodes and [relation[1]] in nodes:
		relations.append([nodes.index([relation[0]]),nodes.index([relation[1]])])


X = data[:,1:1434]
y = data[:,1434]


### TRAINING ###

split_list = range(0,len(X))

split_train, split_test = train_test_split(split_list, test_size=0.33, random_state=2)

X_updated = np.concatenate((X,init_nb_counts(X,targets,y,relations)),1)

split_train.sort()
split_test.sort()

X_train = []
y_train = []

for i in range(0,len(X_updated)):
	if i in split_train:
		X_train.append(X_updated[i])
		y_train.append(y[i])
	
model = LogisticRegression()
model.fit(X_train,y_train)

joblib.dump(model, 'papers.pkl') 


### TEST ###



predictions = []

for i in range(0,len(X)):
	if i in split_train:
		predictions.append(y[i])
	elif i in split_test:
		predictions.append(-1)

X_updated = np.concatenate((X,init_nb_counts(X,targets,predictions,relations)),1)


X_test = []
y_test = []

for i in range(0,len(X)):
	if i in split_test:
		X_test.append(X_updated[i].tolist())
		y_test.append(y[i])



f = open("data.txt", 'w')
json.dump(X_test, f)
f.close()

new_relations = []

for relation in relations:
	if relation[0] in split_test and relation[1] in split_test:
		new_relations.append([split_test.index(relation[0]),split_test.index(relation[1])])

f = open("relations.hex", 'w')
for rel in new_relations:
	f.write("cites("+str(rel[0])+","+str(rel[1])+").\n")
for i in range(0,len(X_test)):
	f.write("paper("+str(i)+").\n")

f.close()




y_pred = []

for i in range(0,len(X_test)):
	y_pred.append(model.predict(X_test[i])[0])

print accuracy_score(y_test,y_pred)



y_pred_old = []

X_test_old = deepcopy(X_test)

while y_pred != y_pred_old:
	X_test = deepcopy(X_test_old)
	update_nb_counts(X_test,y_pred,new_relations)

	y_pred_old = y_pred
	y_pred = []

	for i in range(0,len(X_test)):
		y_pred.append(model.predict(X_test[i])[0])

	print accuracy_score(y_test,y_pred)


