

import random, re
from sklearn import datasets
from sklearn import svm
from sklearn.externals import joblib
import subprocess
import matplotlib.pyplot as plt
import pylab


clf = svm.SVC(probability=True, gamma=0.001, C=100.)


digits = datasets.load_digits()

perc_train = input("On which percentage of the patterns should the SVM be trained (0-100)? ")

num_train = int(float(len(digits.data))*(float(perc_train)/100))

clf.fit(digits.data[:num_train], digits.target[:num_train])



print("SVM has been trained on " + str(num_train) + " patterns.\n")

num_test = input("How many postcodes do you want to test? ")

print("Generating " + str(num_test) + " random postcodes.")

test_postcodes = []

for i in range(0,num_test):
	t = [random.randint(0,9),random.randint(0,9),random.randint(0,9),random.randint(0,9)]
	while t in test_postcodes:
		t = [random.randint(0,9),random.randint(0,9),random.randint(0,9),random.randint(0,9)]
	test_postcodes.append(t)

print("Building testing set.")

indices = []

for d in range(0,10):
	indices.append([i for i, x in enumerate(digits.target[num_train:].tolist()) if x == d])

test_patterns = []

for i in range(0,num_test):
	test_patterns.append([\
        indices[test_postcodes[i][0]][random.randint(0, len(indices[test_postcodes[i][0]]) - 1)],\
        indices[test_postcodes[i][1]][random.randint(0, len(indices[test_postcodes[i][1]]) - 1)],\
        indices[test_postcodes[i][2]][random.randint(0, len(indices[test_postcodes[i][2]]) - 1)],\
        indices[test_postcodes[i][3]][random.randint(0, len(indices[test_postcodes[i][3]]) - 1)]])

print("Testing recognition rate of SVM alone.")

num_correct = 0

for i in range(0,num_test):
	if clf.predict(digits.data[num_train:][test_patterns[i][0]]) == test_postcodes[i][0] and \
           clf.predict(digits.data[num_train:][test_patterns[i][1]]) == test_postcodes[i][1] and \
           clf.predict(digits.data[num_train:][test_patterns[i][2]]) == test_postcodes[i][2] and \
           clf.predict(digits.data[num_train:][test_patterns[i][3]]) == test_postcodes[i][3]:
		num_correct += 1


print("SVM classified " + str(num_correct) + " of " + str(num_test) + " postcodes correctly.\n")



print("Testing recognition rate of dlvhex + SVM.")

joblib.dump(clf, 'digits_model.pkl')

f = open('postcodes.hex', 'w')
for i in range(0,num_test):
	f.write('postcode(' + str(i) + ',' + str(test_postcodes[i][0]) + ',' \
                                      + str(test_postcodes[i][1]) + ',' \
                                      + str(test_postcodes[i][2]) + ',' \
                                      + str(test_postcodes[i][3]) + ').\n')
f.close()

num_correct = 0

f = open('num_train', 'w')
f.write(str(num_train))
f.close()


classifications = []

for i in range(0,num_test):
	
	f = open('input_pattern.hex', 'w')
	f.write('pattern(' + str(test_patterns[i][0]) + ',' \
                           + str(test_patterns[i][1]) + ',' \
                           + str(test_patterns[i][2]) + ',' \
                           + str(test_patterns[i][3]) + ').')
        f.close()

	out = subprocess.check_output(["dlvhex2", "postcode_clf.hex", "postcodes.hex", "input_pattern.hex",\
                         "--python-plugin=postcode_clf.py", "--filter=highest", "--strongsafety"])

	patOut = re.findall("highest\((\d+),\d+\)", out)

	classifications.append(patOut[0])

	prob = re.findall("highest\(\d+,(\d+)\)", out)

	if int(patOut[0]) == int(i):
		num_correct += 1
		print(str(i) + " - Target: " + str(test_postcodes[int(i)]) + "; Classification: " + str(test_postcodes[int(patOut[0])]) + "; Confidence: " + str(float(prob[0])/10))
	else:
		print(str(i) + " - Target: " + str(test_postcodes[int(i)]) + "; Classification: " + str(test_postcodes[int(patOut[0])]) + "; Confidence: " + str(float(prob[0])/10) + " --- X") 


print("\ndlvhex + SVM classified " + str(num_correct) + " of " + str(num_test) + " postcodes correctly.\n")

strInp = ""
while not str(strInp) == "q":
	strInp = raw_input("Show pattern: ")
	if strInp.isdigit() and int(strInp) >= 0 and int(strInp) < num_test:
		print("Target: " + str(test_postcodes[int(strInp)]) + ", Classification: " + str(test_postcodes[int(classifications[int(strInp)])]))
		#Display the first digit
		fig = pylab.figure()
		fig.add_subplot(1,4,1)
		pylab.imshow(digits.images[num_train:][test_patterns[int(strInp)][0]], cmap=plt.cm.gray_r, interpolation='nearest')
		fig.add_subplot(1,4,2)
		pylab.imshow(digits.images[num_train:][test_patterns[int(strInp)][1]], cmap=plt.cm.gray_r, interpolation='nearest')
		fig.add_subplot(1,4,3)
		pylab.imshow(digits.images[num_train:][test_patterns[int(strInp)][2]], cmap=plt.cm.gray_r, interpolation='nearest')
		fig.add_subplot(1,4,4)
		pylab.imshow(digits.images[num_train:][test_patterns[int(strInp)][3]], cmap=plt.cm.gray_r, interpolation='nearest')
		pylab.title(str(test_postcodes[int(classifications[int(strInp)])]))
		pylab.show()






