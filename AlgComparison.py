from classification import * 
from Verification import *
import numpy as np
from sklearn.cross_validation import train_test_split

f = open('TotalMetricTraining.txt', 'r') 
data = f.read() 
metricTrain = eval(data) 

g = open('TotalSpeciesTraining.txt', 'r') 
data = g.read() 
speciesTrain = eval(data) 

#split the data set. 
metric_train, metric_test, species_train, species_test = train_test_split(metricTrain, speciesTrain, test_size=0.5, random_state=0)

species_train = [i if i<3 else 0 for i in species_train]
species_test = [i if i<3 else 0 for i in species_test]
flower_train = [1 if i else 0 for i in species_train] #create a flower training set 
        
clfRF = classifyRF(metric_train, species_train) 
clfKNN = classifyKNN(metric_train, species_train)
#clfSVM = classifySVM(metric_train, species_train)
#clfSGD = classifySGD(metric_train, species_train)
#clfPercep = classifyPerceptron(metric_train, species_train)
clfTree = classifyTree(metric_train, species_train)

clf_flower =  classifyKNN(metric_train, flower_train)

print('Random Forest Scores')
classReport(metric_test, species_test, clfRF)
scores = VerifyTenfold(speciesTrain, metricTrain, clfRF)
print('RF', np.mean(scores) )

print('KNN Scores') 
classReport(metric_test, species_test, clfKNN)
scores = VerifyTenfold(speciesTrain, metricTrain, clfKNN)
print('KNN', np.mean(scores) )


#print('SVM Scores') 
#classReport(metric_test, species_test, clfSVM)
#scores = VerifyTenfold(speciesTrain, metricTrain)
#print('SVM', np.mean(scores) )

#print('SGD Scores') 
#classReport(metricTrain, speciesTrain, clfSGD)
#scores = VerifyTenfold(speciesTrain, metricTrain, clfSGD)
#print('SGD', np.mean(scores) )
#
#print('Perceptron Scores') 
#classReport(metricTrain, speciesTrain, clfPercep)
#scores = VerifyTenfold(speciesTrain, metricTrain, clfPercep)
#print('Perceptron', np.mean(scores) )

print('Decision Tree Scores') 
classReport(metric_test, species_test, clfTree)
scores = VerifyTenfold(speciesTrain, metricTrain, clfTree)
print('Tree', np.mean(scores) )

print('2 stage scores') 
classReport_2stage(metric_test, species_test, clf_flower, clfRF)
scores = VerifyTenfold(speciesTrain, metricTrain, clfRF)
print('2 stage', np.mean(scores))

