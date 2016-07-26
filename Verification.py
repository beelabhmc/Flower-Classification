#Import the thing syou need here. 
import numpy as np 
import matplotlib 
from MachineLearning import * 
from FullProgram import * 
from ImageProcess import * 
from DensityAlignment import *
from sklearn import cross_validation
from classification import *
from sklearn.metrics import classification_report

def GetTrainingMetrics(imageName, trainingType, densityList): 
    """Calculates metrics on a training set to be used later."""
    k=10 #set the number of folds for the verification. Generally set to 10-fold but could be changed based on further research 
    
    #Get the training data 
    image = Image.open(imageName)
    imageSize = image.size
    
    #trainingType: 0 = transect 
    #              1 = picList 
    #              2 = previous data set 
                  
    ##Note that if you have multiple transects you can simply save each transects group of pictures as a picList and then use method 1. 
    
                  
    if trainingType == 0: ###You want to pull data from a transect picture. 
        
        #Get user inputs to determine the transect image being used, and the start and end coordinates of the transect. 
        TransectName = input("Please input the transect image name as a string:" )
        Start = input("Please input the coordinates at the START of the transect:")
        End = input("Please input the coordinates at the END of the transect:")

        #Based on those user inputs create a list of transect images 
        imageList = DensityAlignment.divideTransect(Start, End,TransectName) ## Divide the transect into 50 images. Store in a list. 
        print len(imageList)
        
        ##Compute the metrics on each training image. 
        metricList, densityList = allTrainMetricsTransect(imageList, densityList)
        
        ### Save the training set  - metrics
        f = open('metricListTraining.txt', 'w')
        print >> f, list(metricList)
        f.close()
        
        ### Save the training set - densities 
        f = open('densityListTraining.txt', 'w')
        print >> f, densityList 
        f.close()
        
    if trainingType == 1:  ##pull in pictures titled '1.jpg', etc. 
        numpics = len(densityList)  ##Get the number of training images from the density list (these must be the same length). 
        imageList = makePicList(numpics)
        
        metricList, densityList = allTrainMetrics(imageList, densityList)
        
        ### Save the training set  - metrics
        f = open('metricListTraining.txt', 'w')
        print >> f, list(metricList)
        f.close()
        
        ### Save the training set - densities 
        f = open('densityListTraining.txt', 'w')
        print >> f, densityList 
        f.close()        
            
        
    if trainingType == 2: 
        print('Using previously calculated metric and density lists for training.')
        f = open('metricListTraining.txt', 'r')
        data = f.read()
        metricList = eval(data)
        
        
        g = open('densityListTraining.txt', 'r')
        data = g.read()
        densityList = eval(data)
        
    return metricList
    
    
def VerifyTenfold(densityList, metricList, estimator): 
    """Verification process using K-fold verification to test the accuracy of the algorithm.""" 
    #First, we need an estimator. 
    k = 10 #set the number of cross-validations (k)
    #estimator = SVR( kernel = 'rbf', gamma = 0.05, epsilon = 0.4) #Create an instance of the SVR estimator 
    #estimator = classifyKNN(metricList, densityList)
    #Now seperate out a final test set from the given data. 
    
    #Set aside 30% of the available data for the final test.  
    
    #M_train, M_test, d_train, d_test = cross_validation.train_test_split(metricList, densityList, test_size = 0.25, random_state = 0) 
    
    #Use the full set for testing 
    M_train = metricList 
    d_train = densityList
    
    #M_train is the training set of metrics, d_train is the training set of densities
    #M_test is the metrics reserved for testing, d_test is the corresponding densities. 
    
    #Use the data set aside for training in a cross validation test. 
    scores = cross_validation.cross_val_score(estimator, M_train, d_train, cv = k)

    
    return scores
    
def classReport(metricTrain, speciesTrain, clf): 
    from sklearn.metrics import classification_report
    y_true = speciesTrain
    y_pred = clf.predict(metricTrain)
    print(classification_report(y_true, y_pred))
