import cv2
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import MiniBatchKMeans
from sklearn.externals import joblib
from sklearn import preprocessing
import os
import numpy as np

k = 250

sift = cv2.xfeatures2d.SIFT_create()



sift_descriptors = []
labels = []

for item in os.listdir('data/training/'):
	image = cv2.imread('data/training/' +  item)
	keypoints, descriptors = sift.detectAndCompute(image, None)
	sift_descriptors[len(sift_descriptors):] = descriptors
	labels[len(labels):] = [[int(item.split('-')[0]),len(descriptors)]]


k_means = MiniBatchKMeans(n_clusters=k)
k_means.fit(sift_descriptors)


X = []
i = 0

for label in labels:
	attributes = [0] * k
	for j in range(label[1]):
		attributes[k_means.labels_[i]] += 1
		i += 1
	X[len(X):] = [attributes]


X = np.array(X,"float_")

scaler = preprocessing.StandardScaler().fit(X)

X = scaler.transform(X)

model = LogisticRegression()


model.fit(X,np.array(labels)[:,0])

joblib.dump((model, k_means, scaler), "keypoints.pkl", compress=1)


