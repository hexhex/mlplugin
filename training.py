import cv2
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import MiniBatchKMeans
from sklearn.externals import joblib
from sklearn import preprocessing
import os
import numpy as np
import warnings
import lib.label_objects as lo
warnings.filterwarnings("ignore", category=DeprecationWarning) 

lo.segment_and_label('training')

k = 250

sift = cv2.xfeatures2d.SIFT_create()


sift_descriptors = []
labels = []

for item in os.listdir('temp/training/objects/'):
	image = cv2.imread('temp/training/objects/' +  item)
	keypoints, descriptors = sift.detectAndCompute(image, None)
	sift_descriptors[len(sift_descriptors):] = descriptors
	labels[len(labels):] = [[int(item.split('-')[2]),len(descriptors)]]


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

joblib.dump((model, k_means, scaler), "temp/keypoints.pkl", compress=1)

