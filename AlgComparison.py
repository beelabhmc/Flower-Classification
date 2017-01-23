from classification import * 
from Verification import *
import numpy as np

f = open('TotalMetricTraining.txt', 'r') 
data = f.read() 
metricTrain = eval(data) 

g = open('TotalSpeciesTraining.txt', 'r') 
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
rfscores = VerifyTenfold(speciesTrain, metricTrain, clfRF)
print('RF', np.mean(rfscores) )

print('KNN Scores') 
classReport(metricTrain, speciesTrain, clfKNN)
knnscores = VerifyTenfold(speciesTrain, metricTrain, clfKNN)
print('KNN', np.mean(knnscores) )


print('SVM Scores') 
classReport(metricTrain, speciesTrain, clfSVM)
svmscores = VerifyTenfold(speciesTrain, metricTrain, clfSVM)
print('SVM', np.mean(svmscores) )

print('SGD Scores') 
classReport(metricTrain, speciesTrain, clfSGD)
sgdscores = VerifyTenfold(speciesTrain, metricTrain, clfSGD)
print('SGD', np.mean(sgdscores) )

print('Perceptron Scores') 
classReport(metricTrain, speciesTrain, clfPercep)
pscores = VerifyTenfold(speciesTrain, metricTrain, clfPercep)
print('Perceptron', np.mean(pscores) )

print('Decision Tree Scores') 
classReport(metricTrain, speciesTrain, clfTree)
dscores = VerifyTenfold(speciesTrain, metricTrain, clfTree)
print('Tree', np.mean(dscores) )

print (np.mean(rfscores), np.mean(knnscores), np.mean(svmscores),np.mean(sgdscores),np.mean(pscores),np.mean(dscores))