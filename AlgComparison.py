from classification import * 
from Verification import *
import numpy as np

f = open('TransectMetricTraining.txt', 'r') 
data = f.read() 
metricTrain = eval(data) 

g = open('TransectSpeciesTraining.txt', 'r') 
data = g.read() 
speciesTrain = eval(data) 


clfRF = classifyRF(metricTrain, speciesTrain) 
clfKNN = classifyKNN(metricTrain, speciesTrain)
clfSVM = classifySVM(metricTrain, speciesTrain)
clfSGD = classifySGD(metricTrain, speciesTrain)
clfPercep = classifyPerceptron(metricTrain, speciesTrain)
clfTree = classifyTree(metricTrain, speciesTrain)

print('Random Forest Scores') 
classReport(metricTrain, speciesTrain, clfRF)
scores = VerifyTenfold(speciesTrain, metricTrain, clfRF)
print('RF', np.mean(scores) )

print('KNN Scores') 
classReport(metricTrain, speciesTrain, clfKNN)
scores = VerifyTenfold(speciesTrain, metricTrain, clfKNN)
print('KNN', np.mean(scores) )


print('SVM Scores') 
classReport(metricTrain, speciesTrain, clfSVM)
scores = VerifyTenfold(speciesTrain, metricTrain, clfSVM)
print('SVM', np.mean(scores) )

print('SGD Scores') 
classReport(metricTrain, speciesTrain, clfSGD)
scores = VerifyTenfold(speciesTrain, metricTrain, clfSGD)
print('SGD', np.mean(scores) )

print('Perceptron Scores') 
classReport(metricTrain, speciesTrain, clfPercep)
scores = VerifyTenfold(speciesTrain, metricTrain, clfPercep)
print('Perceptron', np.mean(scores) )

print('Decision Tree Scores') 
classReport(metricTrain, speciesTrain, clfTree)
scores = VerifyTenfold(speciesTrain, metricTrain, clfTree)
print('Tree', np.mean(scores) )