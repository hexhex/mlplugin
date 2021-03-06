import cv2
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn.externals import joblib
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import os
import numpy as np
import warnings
import shutil
import re
import subprocess
import lib.label_objects as lo
import lib.visualization as vz
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning) 


def print_cm(cm, labels, hide_zeroes=False, hide_diagonal=False, hide_threshold=None):
    """pretty print for confusion matrixes"""
    columnwidth = max([len(x) for x in labels]+[5]) # 5 is value length
    empty_cell = " " * columnwidth
    # Print header
    print "    " + empty_cell,
    for label in labels: 
        print "%{0}s".format(columnwidth) % label,
    print
    # Print rows
    for i, label1 in enumerate(labels):
        print "    %{0}s".format(columnwidth) % label1,
        for j in range(len(labels)): 
            cell = "%{0}.f".format(columnwidth) % cm[i, j]
            if hide_zeroes:
                cell = cell if float(cm[i, j]) != 0 else empty_cell
            if hide_diagonal:
                cell = cell if i != j else empty_cell
            if hide_threshold:
                cell = cell if cm[i, j] > hide_threshold else empty_cell
            print cell,
        print



segment = raw_input("Segment and label scenes (y/n)? ")

if segment == "y":
	lo.segment_and_label('test')

model, k_means, scaler = joblib.load("temp/keypoints.pkl")

joblib.dump(model, "temp/test/model.pkl", compress=1)



label_list = joblib.load("temp/labels.pkl")

all_y_pred = []
all_y_true = []
model_all_y_pred = []
model_all_y_true = []

for directory in next(os.walk('temp/test/objects'))[1]:
	sift = cv2.xfeatures2d.SIFT_create()

	sift_descriptors = []
	labels = []

	empty = True
	for item in os.listdir('temp/test/objects/' + directory):
		if item[-4:] == ".jpg":
			empty = False
			image = cv2.imread('temp/test/objects/' + directory + '/' + item)
			keypoints, descriptors = sift.detectAndCompute(image, None)
			if descriptors != None:
				sift_descriptors[len(sift_descriptors):] = descriptors
				labels[len(labels):] = [[int(item.split('-')[2]),len(descriptors),int(item.split('-')[1])]]
			else:
				print "object too small"


	if not empty:
		print "Scene: " + directory
		print "--------------------------"
		X = []
		i = 0

		labels_ = k_means.predict(sift_descriptors)

		for label in labels:
			attributes = [0] * k_means.get_params()['n_clusters']
			for j in range(label[1]):
				attributes[labels_[i]] += 1
				i += 1
			X[len(X):] = [attributes]



		X = np.array(X,"float_")

		X = scaler.transform(X)


		if os.path.exists('temp/test/testscene/'):
			shutil.rmtree('temp/test/testscene/')
		os.makedirs('temp/test/testscene/')

		scene_file = open('temp/test/testscene/scene.hex', 'w')
		scene_file.write('scene("' + directory + '").\n')

		#print np.array(labels)[:,0]
		i = 0

		object_labels = dict()

		model_predictions = []


		for x in X:
			file = open('temp/test/testscene/object' + str(labels[i][2]), 'w')
			file.write(str(x.tolist()))
			file.close()
			
			object_labels[labels[i][2]] = label_list[labels[i][0]]

			scene_file.write('object("object' + str(labels[i][2]) + '").\n')
			
			print 'object' + str(labels[i][2]) + ':'
			print "Ground truth: " + label_list[labels[i][0]]

			print "Prediction:   " + label_list[model.predict(x)[0]]

			model_predictions.append((str(labels[i][2]),label_list[model.predict(x)[0]]))
			i += 1
			n = 0
			for prob in model.predict_proba(x)[0]:
				print str(prob)[:8] + "\t: " + label_list[n]
				n += 1
			print ''

		for label in label_list:
			scene_file.write('label(' + str(label_list.index(label)) + ',' + label + ').\n')
			scene_file.write('label_string("' + label + '",' + label + ').\n')

		scene_file.close()

		FNULL = open(os.devnull, 'w')
		hex_results = subprocess.check_output(["dlvhex2", "categorize.hex", "temp/test/testscene/scene.hex", "--python-plugin=lib/plugin.py", "--filter=assigned_label", "-n=1", "-s"], stderr=FNULL)

		predictions = re.findall('assigned_label\(\"object(\d+)\"\,(.+?)\)', hex_results)

		y_pred = []
		y_true = []
		for (obj,pred) in predictions:
			y_pred.append(pred)
			y_true.append(object_labels[int(obj)])

		all_y_pred += y_pred
		all_y_true += y_true


		true_labels = []
		for lbl in labels:
			true_labels.append(lbl[0])

		model_all_y_pred += model.predict(X).tolist()
		model_all_y_true += true_labels

		print 'Accuracy without constr.:  ' + str(accuracy_score(true_labels, model.predict(X)))
		print 'Accuracy with constraints: ' + str(accuracy_score(y_true, y_pred)) + '\n'


		vz.visualize(predictions,directory)
		vz.visualize(model_predictions,directory,True)

print 'Overall Accuracy without constr.:  ' + str(accuracy_score(model_all_y_true, model_all_y_pred))
print 'Overall Accuracy with constraints: ' + str(accuracy_score(all_y_true, all_y_pred)) + '\n'
print classification_report(all_y_true, all_y_pred)

labelss = label_list
cm = confusion_matrix(all_y_pred, all_y_true, labelss)

# then print it in a pretty way
print_cm(cm, labelss)

