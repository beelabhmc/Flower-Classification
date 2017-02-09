#Import the thing syou need here. 
from MachineLearning import * 
from FullProgram import * 
from ImageProcess import * 
from DensityAlignment import *
from sklearn import cross_validation
from classification import *
from sklearn.metrics import classification_report
from sklearn.feature_selection import SelectKBest
from sklearn.cross_validation import train_test_split
import sklearn.utils.multiclass as mc
import numpy as np 
def GetTrainingMetrics(imageName, trainingType, densityList): 
    """Calculates or reads in pre calculated metrics on a training set to be used later."""
    
    #Get the training data 
    
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
        
    return metricList #return the claculated or read in training metrics. 
    
    
def VerifyTenfold(speciesList, metricList, est): 
    """Verification process using K-fold verification to test the accuracy of the algorithm.
    Takes in speciesList, the training species classes. 
    metricList, the training image metrics. 
    Estimator, a trained classification estimator. """ 
    
    #First, we need an estimator. 
    k = 10 #set the number of cross-validations (k)
    #estimator = SVR( kernel = 'rbf', gamma = 0.05, epsilon = 0.4) #Create an instance of the SVR estimator 
    #estimator = classifyKNN(metricList, densityList)
    #Now seperate out a final test set from the given data. 
    
    #Set aside 30% of the available data for the final test.  
    
    #M_train, M_test, d_train, d_test = cross_validation.train_test_split(metricList, densityList, test_size = 0.25, random_state = 0) 
    
    #Use the full set for testing 
    M_train = metricList 
    d_train = speciesList
    for i in range(len(d_train)): #Limit the test to only the top 2 species. 
        if d_train[i] > 2: 
            d_train[i] = 0 

    scaledMetrics, scaler = scaleMetrics(M_train)
    kbest = SelectKBest(k=18) 
    kbest.fit(M_train, d_train)
   # est = classifyTree(M_train, d_train)
    
    #M_train is the training set of metrics, d_train is the training set of densities
    #M_test is the metrics reserved for testing, d_test is the corresponding densities. 
    
    #Use the data set aside for training in a cross validation test. 
    scores = cross_validation.cross_val_score(est, M_train, d_train, cv = k)

    
    return scores

    
def VerifyTenfold_2stage(speciesList, metricList, clf_flower, clf_species): 
    """Verification process using K-fold verification to test the accuracy of the algorithm.
    Takes in speciesList, the training species classes. 
    metricList, the training image metrics. 
    Estimator, a trained classification estimator. """ 
    
    #First, we need an estimator. 
    k = 10 #set the number of cross-validations (k)
    #estimator = SVR( kernel = 'rbf', gamma = 0.05, epsilon = 0.4) #Create an instance of the SVR estimator 
    #estimator = classifyKNN(metricList, densityList)
    #Now seperate out a final test set from the given data.     
    
    scaledMetrics, scaler = scaleMetrics(metricList)

   # est = classifyTree(M_train, d_train)
    for i in range(10): #cross-validate 10 times 
        X_train, X_test, y_train, y_test = cross_validation.train_test_split(metricList, speciesList, test_size=0.4, random_state=0) #split the data. 
        est_flower = clf_flower.fit(X_train, y_train_flowers) #fit the estimator for flowers. 
        est_species = clf_species.fit(X_train, y_train_species) #fit the estimator for species. 
        
        #Score each set of testing and training results. 
    return scores
        
def classReport(metricTrain, speciesTrain, clf): 
    """Produces a report on how well an estimator performs on each class."""
    #split the training set. 
    y_true = speciesTrain #This is the actual classes 
    y_pred = clf.predict(metricTrain) #The classes predicted by the classifier. 
#    print(y_pred)
    print(classification_report(y_true, y_pred)) #print out the full report of performance by class. 

def classReport_2stage(metricTrain, speciesTrain, clf_flower, clf_species): 
    y_true = speciesTrain
    y_pred = []
    metricTrain = np.asarray(metricTrain) #Transform the data into a numpy array. 
    for i in range(len(metricTrain)): #for each point in the training set. 
        #y_pred.extend(clf_species.predict(metricTrain[i])) #Currently only predicting from the species alg. 
        flower = clf_flower.predict(metricTrain[i].reshape(1,-1)) #Check if this is a flower or not. The data is a single sample, so reshape to avoid deprecation warning. 
        if flower: #Check if the sample is a flower 
            y_pred.extend(clf_species.predict(metricTrain[i].reshape(1,-1))) #Get the species prediction. Reshape to avoid deprecation. 
        else: 
            y_pred += [flower]
    y_pred = [int(k) for k in y_pred]
    print(classification_report(y_true, y_pred))
    return y_true, y_pred

def featOrder(imps): 
    """Sort the importance list to return the feature numbers by order of importance.""" 
    #return sorted(range(len(imps)), key = lambda k:imps[k])
    return [i+1 for i in numpy.argsort(imps)]
    
    
def testFeatures(thresh, kfeatures): 
    """Test the features you are using to determine if they are valuable to actual classification.""" 
    
    #First determine which features have very low variance across the training set. 
    sel = VarianceThreshold(threshold = thresh)

    if 1:
        FullImList, FullSpeciesList = createAllTransectTraining()
        metricTrain, speciesTrain = allTrainMetrics(FullImList, FullSpeciesList) #get training metrics 
        
        ### Save the training set  - metrics
        f = open('TransectMetricTraining.txt', 'w')
        print >> f, list(metricTrain)
        f.close()
                
        ### Save the training set - densities 
        f = open('TransectSpeciesTraining.txt', 'w')
        print >> f, list(speciesTrain)
        f.close()
    if 0: 
        f = open('TransectMetricTraining.txt', 'r') 
        data = f.read() 
        metricTrain = eval(data) 
         
        g = open('TransectSpeciesTraining.txt', 'r') 
        data = g.read() 
        speciesTrain = eval(data) 
        
    scaledMetrics, scaler = scaleMetrics(metricTrain)
    sel.fit(metricTrain) #check the variance on metrics prior to scaling. 
    threshIndex = sel.get_support()
    
    ##Now, seperately, select the K best features 
    #Use the scaled metrics because this is what we will actually train with. 
    kbest = SelectKBest(k=kfeatures) 
    kbest.fit(scaledMetrics, speciesTrain)
    bestIndex = kbest.get_support()
    return metricTrain, threshIndex, bestIndex