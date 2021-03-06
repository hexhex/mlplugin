from sklearn.externals import joblib
import os
import numpy as np
import warnings
import shutil
import re
import subprocess
import lib.label_objects as lo
import lib.visualization as vz
import math
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning) 




num_constraints = 8

label_list = joblib.load("temp/labels.pkl")

num_violations = []
num_summ = []

for i in range(1,num_constraints+1):
	num_violations.append(0)
	num_summ.append(0)

for directory in next(os.walk('temp/training/objects'))[1]:
	labels = []

	for item in os.listdir('temp/training/objects/' + directory):
		if item[-4:] == ".jpg":

			labels[len(labels):] = [[int(item.split('-')[2]),0,int(item.split('-')[1])]]

	if os.path.exists('temp/training/testscene/'):
		shutil.rmtree('temp/training/testscene/')
	os.makedirs('temp/training/testscene/')

	scene_file = open('temp/training/testscene/scene.hex', 'w')
	scene_file.write('scene("' + directory + '").\n')


	object_labels = dict()



	for i in range(0,len(labels)):

		object_labels[labels[i][2]] = label_list[labels[i][0]]

		scene_file.write('object("object' + str(labels[i][2]) + '").\n')
		scene_file.write('assigned_label("object' + str(labels[i][2]) + '",' + label_list[labels[i][0]] + ').\n')



	for label in label_list:
		scene_file.write('label(' + str(label_list.index(label)) + ',' + label + ').\n')
		scene_file.write('label_string("' + label + '",' + label + ').\n')

	scene_file.close()

	print directory

	for i in range(1,num_constraints+1):

		FNULL = open(os.devnull, 'w')
		hex_results = subprocess.check_output(["dlvhex2", "getweights.hex", "temp/training/testscene/scene.hex", "constraints/constraint"+str(i)+"-violations.lp", "--python-plugin=lib/plugin.py", "--filter=violated", "-n=1", "-s"], stderr=FNULL)
	
		violations = len(re.findall('violated\((.+?)\)', hex_results)) + float(0.001)

		num_violations[i-1] += violations


		hex_results = subprocess.check_output(["dlvhex2", "getweights.hex", "temp/training/testscene/scene.hex", "constraints/constraint"+str(i)+"-sum.lp", "--python-plugin=lib/plugin.py", "--filter=sum", "-n=1", "-s"], stderr=FNULL)

		summ = len(re.findall('sum\((.+?)\)', hex_results)) + float(0.001)
		
		num_summ[i-1] += summ

		print math.log(num_violations[i-1]/(num_summ[i-1]-num_violations[i-1])) * -1

all_constraints = ""

for i in range(1,num_constraints+1):
	constraints_file = open('constraints/constraint' + str(i) + '.lp', 'r')
	constr = constraints_file.read()
	constraints_file.close()
	all_constraints += constr.replace("WEIGHT",str(int(math.log(num_violations[i-1]/(num_summ[i-1]-num_violations[i-1])) * -10000)))

print all_constraints

constraints_file = open('constraints.lp', 'w')
constraints_file.write(all_constraints)
constraints_file.close()




