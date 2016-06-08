import dlvhex
import json
import math
from sklearn.externals import joblib
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from shapely.geometry import Polygon


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

def predictProb(classifier,object,threshold,maxnum,mode,threshold_mode):
	f = open("temp/test/testscene/"+object.value().strip('"'), 'r')
	X_test = json.load(f)
	f.close()
	model = joblib.load(classifier.value().strip('"'))
	
	prob_dist = model.predict_proba(X_test)[0].tolist()

	labels = model.classes_

	zipped = zip(prob_dist, labels)
	zipped.sort()

	if threshold_mode.value() == "t":
		threshold_val = float(threshold.value())/100
	elif threshold_mode.value() == "d":
		threshold_val = max(prob_dist) - float(threshold.value())/100

	num_count = 0

	for prob, labeled in zipped:
		if (prob >= threshold_val and num_count < int(maxnum.value())) or (num_count == 0 and prob < threshold_val):
			if mode.value() == "prob":
				dlvhex.output((str(labeled), int(1000 - (prob * 1000))))
			elif mode.value() == "logprob":
				dlvhex.output((str(labeled), int( - (math.log(prob) * 1000))))
			elif mode.value() == "logodds":
				dlvhex.output(( str(labeled),'"' + str(-1 * int(math.log(prob/(1-prob)) * 10000)) + '"' ))
			elif mode.value() == "rank":
				dlvhex.output((str(labeled), num_count))
			num_count += 1


def ranking(classifier,object,threshold):
	f = open("temp/test/testscene/"+object.value().strip('"'), 'r')
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


def spatial(scene,slack,mode):
        polygons = joblib.load('temp/' + mode.value() + '/objects/' + scene.value().strip('"') + '.pkl')
        
        for i in range(0,len(polygons)-1):
                for j in range(0,len(polygons)-1):
                        if i != j:

                                if polygons[i][2][0] - int(slack.value()) < polygons[j][2][0] and \
                                        polygons[i][2][1] - int(slack.value()) < polygons[j][2][1] and \
                                        polygons[i][2][2] + int(slack.value()) > polygons[j][2][2] and \
                                        polygons[i][2][3] + int(slack.value()) > polygons[j][2][3]:
                                        p1=Polygon(polygons[i][0])
                                        p2=Polygon(polygons[j][0])
                                        if p1.intersects(p2):
                                                dlvhex.output(('contains','"object' + str(i+1) + '"','"object' + str(j+1) + '"'))

                                if polygons[i][2][0] - int(slack.value()) < polygons[j][2][0] and \
                                        polygons[i][2][1] - int(slack.value()) + ((polygons[i][2][3] - polygons[i][2][1])/2) < polygons[j][2][1] and \
                                        polygons[i][2][2] + int(slack.value()) > polygons[j][2][2] and \
                                        polygons[i][2][3] + int(slack.value()) > polygons[j][2][3]:
                                        p1=Polygon(polygons[i][0])
                                        p2=Polygon(polygons[j][0])
                                        if p1.intersects(p2):
                                                dlvhex.output(('contains_bottom','"object' + str(i+1) + '"','"object' + str(j+1) + '"'))

                                if polygons[i][2][3] - polygons[i][2][1] + int(slack.value()) > polygons[j][2][3] - polygons[j][2][1]:
                                        dlvhex.output(('higher','"object' + str(i+1) + '"','"object' + str(j+1) + '"'))
            

def register():
	prop = dlvhex.ExtSourceProperties()
	prop.setFunctional(True)
	prop.setProvidesPartialAnswer(True)
	dlvhex.addAtom("predict", (dlvhex.CONSTANT, dlvhex.CONSTANT, dlvhex.PREDICATE, dlvhex.CONSTANT), 1, prop)
	dlvhex.addAtom("predictProb", (dlvhex.CONSTANT, dlvhex.CONSTANT, dlvhex.CONSTANT, dlvhex.CONSTANT, dlvhex.CONSTANT, dlvhex.CONSTANT), 2)
	dlvhex.addAtom("ranking", (dlvhex.CONSTANT, dlvhex.CONSTANT, dlvhex.CONSTANT), 2)
	dlvhex.addAtom("spatial", (dlvhex.CONSTANT, dlvhex.CONSTANT, dlvhex.CONSTANT), 3)

