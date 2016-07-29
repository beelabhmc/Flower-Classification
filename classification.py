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
    """Creates a Random Forest classifier trained on the data in metrics and classes.
    Returns the fitted function. Note that metrics and classes must be lists of the same length. """
    clf = RandomForestClassifier(n_estimators = 10) #adjust the parameters for the function here. 
    clf.fit(metrics, classes) #fit to the given training data 
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
    """Creates a Stochastic Gradient Descent classifier trained on the data in metrics and classes.
    Returns the fitted function. Note that metrics and classes must be lists of the same length. """
    clf = SGDClassifier(loss="perceptron", penalty="l2")
    clf.fit(metrics, classes) 
    return clf
    

  
def classifyPerceptron(metrics, classes):
    """Creates a Perceptron classifier trained on the data in metrics and classes.
    Returns the fitted function. Note that metrics and classes must be lists of the same length. """ 
    clf = Perceptron() 
    clf.fit(metrics, classes) 
    return clf

    
def classifyTree(metrics, classes): 
    """Creates a Decision Tree classifier trained on the data in metrics and classes.
    Returns the fitted function. Note that metrics and classes must be lists of the same length. """
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
 