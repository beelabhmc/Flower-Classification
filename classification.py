# -*- coding: utf-8 -*-

from sklearn import neighbors
from ImageProcess import *
from sklearn import svm 
from FullProgram import *
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import Perceptron
from sklearn import tree 
from sklearn.ensemble import RandomForestClassifier 



def classifyRF(metrics, classes): 
    clf = RandomForestClassifier(n_estimators = 10) 
    clf.fit(metrics, classes)
    return clf 
    
def classifyKNN(metrics, classes): 
    """Creates a K Nearest Neighbors algorithm trained on the data in metrics and classes. Metrics and classes are lists of the same length. Returns the fitted function."""
    n_neighbors = 2
    clf = neighbors.KNeighborsClassifier(n_neighbors)
    clf.fit(metrics, classes)
    return clf 
    
def classifySVM(metrics, classes):
    """Creates a Support Vector Machine trained on the data in metrics and classes. Metrics and classes are lists of the same length. Returns the fitted function."""
    weights = {}
    weights[0] = 0.1 
    weights[1] = 2.5
    clf = svm.SVC(class_weight = weights, kernel = 'rbf')
    clf.fit(metrics, classes)
    return clf
    
def classifySGD(metrics, classes): 
    clf = SGDClassifier(loss="perceptron", penalty="l2")
    clf.fit(metrics, classes) 
    return clf
    

  
def classifyPerceptron(metrics, classes): 
    clf = Perceptron() 
    clf.fit(metrics, classes) 
    return clf

    
def classifyTree(metrics, classes): 
    clf = tree.DecisionTreeClassifier(min_samples_leaf = 3) 
    clf.fit(metrics, classes) 
    return clf 
    
def getClassifier():    
    """Opens and processes training data, creates a classifier, trains it on 
    that data, and returns the resulting fit function."""
    densityList = makeDensList()

    
    NUMPICS = 50  ##Change the number of training pictures here. 
    imageList = makePicList(NUMPICS)
    #imageList += ['TreeTrain1.jpeg', 'TreeTrain2.jpeg', 'TreeTrain3.jpeg', 'TreeTrain4.jpeg', 'TreeTrain5.jpeg', 'TreeTrain6.jpeg', 'Grass1.jpg', 'Path1.jpg', 'Buckwheat.jpeg', 'Buckwheat2.jpeg', 'Buckwheat3.jpeg']
    imageList = makeImList(imageList)
    
    metricList, dL = allTrainMetrics(imageList, densityList)
  
    
    classList = densityList 
    
    for i in range(len(densityList)): 
        if densityList[i] > 0: 
            classList[i] = 1 
        else: 
            classList[i] = 0 
    

    fit = classify(metricList, classList)
    return fit
 
def makeDensList(): 
    """Creates a density list. Change the length of the list inside the code, as well as 
    entering the desired trainingData manually. Returns a numpy array of densities."""
    trainingData = numpy.zeros(83)

    
     #Uncomment below groupings for full data set from both transects, plus additional data.  
    #trainingData[2] = 14 
    #trainingData[3] = 3
    #trainingData[4] = 7
    #trainingData[6] = 8
    #trainingData[19] = 5
    #
    #trainingData[54] = 25830 
    #trainingData[58] = 7840 
    #trainingData[59] = 13600
    #trainingData[68] = 1 
    #trainingData[58] = 20000 
    #trainingData[64] = 20000 
    #trainingData[66] = 40000 
    
    ######Start of handmade density list. Do not use for final as this is not 
    ######based on field data. Just guessing. 
    #
    #trainingData[58] = 7800 
    #trainingData[64] = 10000
    #trainingData[66] = 5000
    #trainingData[108] = 20000
    #trainingData[109] = 10000
    #trainingData[110] = 20000
    
    #Uncomment group below if NNG data comes firt. 
 #   trainingData[4] = 25830 
    trainingData[4] = 1000
    trainingData[8] = 7840 
    trainingData[7] = 2000
  #  trainingData[9] = 13600 
    #trainingData[18] = 1
    #
    trainingData[58] = 20000
    trainingData[59] = 10000
    trainingData[60] = 20000
    trainingData[67] = 20000
    trainingData[68] = 10000
    trainingData[69] = 5000
    trainingData[70] = 10000
    trainingData[71] = 7000
    trainingData[72] = 2000
    #trainingData += [0,0,0,0,0,0,0,0,20000, 10000, 20000, 0,0,0,0,0,0, 20000, 10000, 5000,
    #10000, 7000, 2000] 
    

    return trainingData   
