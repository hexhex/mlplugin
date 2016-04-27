import dlvhex
import json
from sklearn.externals import joblib
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def predict(classifier,object,filter,threshold):
	f = open("temp/test/testscene/"+object.value().strip('"'), 'r')
	X_test = json.load(f)
	f.close()
	model = joblib.load(classifier.value().strip('"'))


	prob_dist = model.predict_proba(X_test)[0]

	prob_dict = {}	

	threshold_val = float(threshold.value())/100

	filter_list = []
	non_filter_list = []

	for x in dlvhex.getInputAtoms():
		if x.tuple()[0] == filter and x.isTrue() and x.tuple()[1].value() == object.value():
			print "yes"
			filter_list.append(int(x.tuple()[2].value()))
		if x.tuple()[0] == filter and x.isFalse() and x.tuple()[1].value() == object.value():
			print "yes2"
			non_filter_list.append(int(x.tuple()[2].value()))

	for prob, label in zip(prob_dist.tolist(),model.classes_):
		if label in filter_list or prob < threshold_val:
			prob_dict[label] = 0
		else:		
			prob_dict[label] = prob

	cur_label = ""
	cur_prob = 0

	unknown_labels = []    

	for key, value in prob_dict.iteritems():
		if value > cur_prob:
			cur_prob = value
			cur_label = key
		if value != 0:
			unknown_labels.append(key)

	if cur_label != "" and cur_label in non_filter_list:
		dlvhex.output((cur_label,))
	else:
		for unknown_label in unknown_labels:
			dlvhex.outputUnknown((unknown_label,))


def ranking(classifier,object,threshold):
	f = open("scene/"+object.value().strip('"'), 'r')
	X_test = json.load(f)
	f.close()
	model = joblib.load(classifier.value().strip('"'))


	prob_dist = model.predict_proba(X_test)[0].tolist()

	labels = model.classes_

	zipped = zip(prob_dist, labels)
	zipped.sort()
	sorted_labels = [label for (prob, label) in zipped]

	threshold_val = float(threshold.value())/100

	rank = 0

	for prob, label in zipped:
		if prob >= threshold_val:
			dlvhex.output((label,rank))
			rank += 1

def spatial(object1,object2,scene,slack):
    polygons = joblib.load('temp/test/objects/' + scene.value().strip('"') + '.pkl')

    if polygons[int(object1.value().strip('"')[6:])-1][2][0] - int(slack.value()) < polygons[int(object2.value().strip('"')[6:])-1][2][0] and \
            polygons[int(object1.value().strip('"')[6:])-1][2][1] - int(slack.value()) < polygons[int(object2.value().strip('"')[6:])-1][2][1] and \
            polygons[int(object1.value().strip('"')[6:])-1][2][2] + int(slack.value()) > polygons[int(object2.value().strip('"')[6:])-1][2][2] and \
            polygons[int(object1.value().strip('"')[6:])-1][2][3] + int(slack.value()) > polygons[int(object2.value().strip('"')[6:])-1][2][3]:
        dlvhex.output(("contains",))
            

def register():
	prop = dlvhex.ExtSourceProperties()
	prop.setFunctional(True)
	prop.setProvidesPartialAnswer(True)
	dlvhex.addAtom("predict", (dlvhex.CONSTANT, dlvhex.CONSTANT, dlvhex.PREDICATE, dlvhex.CONSTANT), 1, prop)
	dlvhex.addAtom("ranking", (dlvhex.CONSTANT, dlvhex.CONSTANT, dlvhex.CONSTANT), 2)
	dlvhex.addAtom("spatial", (dlvhex.CONSTANT, dlvhex.CONSTANT, dlvhex.CONSTANT, dlvhex.CONSTANT), 1)

