import warnings
warnings.filterwarnings("ignore")


import sys
from class_vis import prettyPicture
from prep_terrain_data import makeTerrainData

import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
from sklearn import tree

features_train, labels_train, features_test, labels_test = makeTerrainData()



#################################################################################


########################## DECISION TREE #################################

### your code goes here--now create 2 decision tree classifiers,
### one with min_samples_split=2 and one with min_samples_split=50
### compute the accuracies on the testing data and store
### the accuracy numbers to acc_min_samples_split_2 and
### acc_min_samples_split_50, respectively

#creatin 1st dec. tree with num_splits 1
clf2 = tree.DecisionTreeClassifier(min_samples_split=2)
clf2 = clf2.fit(features_train, labels_train)
acc2 = clf2.score(features_test, labels_test)

#creating 2nd dec tree with num_splits 50
clf50 = tree.DecisionTreeClassifier(min_samples_split=50)
clf50 = clf50.fit(features_train, labels_train)
acc50 = clf50.score(features_test, labels_test)


acc_min_samples_split_2 = acc2
acc_min_samples_split_50 = acc50

def submitAccuracies():
  return {"acc_min_samples_split_2":round(acc_min_samples_split_2,3),
          "acc_min_samples_split_50":round(acc_min_samples_split_50,3)}

