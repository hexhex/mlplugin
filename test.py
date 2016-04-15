import cv2
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn.externals import joblib
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
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

segment = raw_input("Segment and label scenes (y/n)? ")

if segment == "y":
	lo.segment_and_label('test')

model, k_means, scaler = joblib.load("temp/keypoints.pkl")

joblib.dump(model, "temp/test/model.pkl", compress=1)



name_dict, name_num, name_list = joblib.load("temp/labels.pkl")

label_names = {v: k for k, v in name_dict.items()}

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


	if not empty:
		print "Scene: " + directory
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

		#print np.array(labels)[:,0]
		i = 0

		object_labels = dict()

		for x in X:
			file = open('temp/test/testscene/object' + str(labels[i][2]), 'w')
			file.write(str(x.tolist()))
			file.close()
			
			object_labels[labels[i][2]] = label_names[labels[i][0]]

			scene_file.write('object("object' + str(labels[i][2]) + '").\n')
			
			print "Ground truth: " + label_names[labels[i][0]]

			print "Prediction:   " + label_names[model.predict(x)[0]]
			i += 1
			n = 0
			for prob in model.predict_proba(x)[0]:
				print str(prob)[:8] + "\t: " + label_names[n]
				n += 1
			print ''

		for label in label_names:
			scene_file.write('label(' + str(label) + ',' + label_names[label] + ').\n')

		scene_file.close()
		FNULL = open(os.devnull, 'w')
		hex_results = subprocess.check_output(["dlvhex2", "categorize.hex", "temp/test/testscene/scene.hex", "--python-plugin=lib/plugin.py", "--filter=assigned_label", "-s"], stderr=FNULL)

		predictions = re.findall('assigned_label\(\"object(\d+)\"\,(.+?)\)', hex_results)

		y_pred = []
		y_true = []
		for (obj,pred) in predictions:
			y_pred.append(pred)
			y_true.append(object_labels[int(obj)])
		print 'Accuracy: ' + str(accuracy_score(y_true, y_pred)) + '\n'

		vz.visualize(predictions,directory)
