import cv2
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn.externals import joblib
from sklearn import preprocessing
import os
import numpy as np



model, k_means, scaler = joblib.load("keypoints.pkl")


sift = cv2.xfeatures2d.SIFT_create()


sift_descriptors = []
labels = []

label_names = {}

for item in os.listdir('data/test/'):
	image = cv2.imread('data/test/' +  item)
	keypoints, descriptors = sift.detectAndCompute(image, None)
	sift_descriptors[len(sift_descriptors):] = descriptors
	labels[len(labels):] = [[int(item.split('-')[0]),len(descriptors)]]
	label_names[int(item.split('-')[0])] = item.split('-')[1]

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


i = 0

scene_file = open('scene.hex', 'w')

print np.array(labels)[:,0]

for x in X:
	file = open('scene/object' + str(i), 'w')
	file.write(str(x.tolist()))
	file.close()

	scene_file.write('object("object' + str(i) + '").\n')
	i += 1
	print model.predict(x)[0]
	print model.predict_proba(x)[0]

for label in set(np.array(labels)[:,0]):
	scene_file.write('label(' + str(label) + ',' + label_names[label] + ').\n')

scene_file.close()

joblib.dump(model, "model.pkl", compress=1)
