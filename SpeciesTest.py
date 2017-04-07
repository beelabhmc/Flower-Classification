#This script is written to speed up the testing of species classification code. 
from classification import *
from SpeciesClassProbability import *
from TrainingSpeciesList import *
from SpeciesClass import *
from StageSpeciesClass import * 
from createTraining import *
from Verification import *
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectKBest
from sklearn import grid_search, datasets
from Constants import *
import numpy as np

def SpeciesTest(trainingMode):
    #input a training set - list of metrics and the corresponding species. The 2 lists must be the same length. 
    #metricTrain= [[33.411989795918366, 33.411989795918366, 33.411989795918366, 0.0, 82.525997400295523, 0.016581632653061226, 0.0], [31.682397959183675, 31.682397959183675, 31.682397959183675, 0.0, 82.525997400295523, 0.014668367346938776, 0.03125], [32.691964285714285, 32.691964285714285, 32.691964285714285, 0.0, 82.525997400295523, 0.01403061224489796, 0.03125], [32.63647959183673, 32.63647959183673, 32.63647959183673, 0.0, 82.525997400295523, 0.01211734693877551, 0.21875], [32.61224489795919, 32.61224489795919, 32.61224489795919, 0.0, 82.525997400295523, 0.012755102040816327, 0.0], [30.714923469387756, 30.714923469387756, 30.714923469387756, 0.0, 82.525997400295523, 0.008928571428571428, 0.0], [30.896045918367346, 30.896045918367346, 30.896045918367346, 0.0, 82.525997400295523, 0.01594387755102041, 0.0], [30.852040816326532, 30.852040816326532, 30.852040816326532, 0.0, 82.525997400295523, 0.01594387755102041, 0.0625], [29.049744897959183, 29.049744897959183, 29.049744897959183, 0.0, 82.525997400295523, 0.01211734693877551, 0.03125], [26.432397959183675, 26.432397959183675, 26.432397959183675, 0.0, 82.525997400295523, 0.008290816326530613, 0.25], [27.523596938775512, 27.523596938775512, 27.523596938775512, 0.0, 82.525997400295523, 0.001913265306122449, 0.0625], [27.310586734693878, 27.310586734693878, 27.310586734693878, 0.0, 82.525997400295523, 0.009566326530612245, 0.0], [26.762755102040817, 26.762755102040817, 26.762755102040817, 0.0, 82.525997400295523, 0.005739795918367347, 0.0], [31.371173469387756, 31.371173469387756, 31.371173469387756, 0.0, 82.525997400295523, 0.016581632653061226, 0.0], [29.536989795918366, 29.536989795918366, 29.536989795918366, 0.0, 82.525997400295523, 0.016581632653061226, 0.0], [26.915816326530614, 26.915816326530614, 26.915816326530614, 0.0, 82.525997400295523, 0.011479591836734694, 0.0], [27.807397959183675, 27.807397959183675, 27.807397959183675, 0.0, 82.525997400295523, 0.016581632653061226, 0.0], [28.81313775510204, 28.81313775510204, 28.81313775510204, 0.0, 82.525997400295523, 0.015306122448979591, 0.0], [26.301020408163264, 26.301020408163264, 26.301020408163264, 0.0, 82.525997400295523, 0.01020408163265306, 0.0], [27.67283163265306, 27.67283163265306, 27.67283163265306, 0.0, 82.525997400295523, 0.015306122448979591, 0.0], [28.051020408163264, 28.051020408163264, 28.051020408163264, 0.0, 82.525997400295523, 0.005739795918367347, 0.03125], [26.443877551020407, 26.443877551020407, 26.443877551020407, 0.0, 82.525997400295523, 0.01020408163265306, 0.0], [27.12563775510204, 27.12563775510204, 27.12563775510204, 0.0, 82.525997400295523, 0.011479591836734694, 0.0], [27.998086734693878, 27.998086734693878, 27.998086734693878, 0.0, 82.525997400295523, 0.008290816326530613, 0.21875], [28.012117346938776, 28.012117346938776, 28.012117346938776, 0.0, 82.525997400295523, 0.010841836734693877, 0.25], [25.68813775510204, 25.68813775510204, 25.68813775510204, 0.0, 82.525997400295523, 0.01211734693877551, 0.0], [25.45216836734694, 25.45216836734694, 25.45216836734694, 0.0, 82.525997400295523, 0.01020408163265306, 0.0], [26.017857142857142, 26.017857142857142, 26.017857142857142, 0.0, 82.525997400295523, 0.016581632653061226, 0.25], [24.292729591836736, 24.292729591836736, 24.292729591836736, 0.0, 82.525997400295523, 0.012755102040816327, 0.0], [24.325892857142858, 24.325892857142858, 24.325892857142858, 0.0, 82.525997400295523, 0.0012755102040816326, 0.0], [19.853954081632654, 19.853954081632654, 19.853954081632654, 0.0, 82.525997400295523, 0.0, 0.0], [19.130102040816325, 19.130102040816325, 19.130102040816325, 0.0, 82.525997400295523, 0.0, 0.0], [16.59502551020408, 16.59502551020408, 16.59502551020408, 0.0, 82.525997400295523, 0.0, 0.21875], [14.911989795918368, 14.911989795918368, 14.911989795918368, 0.0, 82.525997400295523, 0.0, 0.0], [14.662627551020408, 14.662627551020408, 14.662627551020408, 0.0, 82.525997400295523, 0.0, 0.0], [15.293367346938776, 15.293367346938776, 15.293367346938776, 0.0, 82.525997400295523, 0.0, 0.0], [14.072704081632653, 14.072704081632653, 14.072704081632653, 0.0, 82.525997400295523, 0.0, 0.0], [12.860969387755102, 12.860969387755102, 12.860969387755102, 0.0, 82.525997400295523, 0.0006377551020408163, 0.0], [13.991071428571429, 13.991071428571429, 13.991071428571429, 0.0, 82.525997400295523, 0.0, 0.0], [15.65625, 15.65625, 15.65625, 0.0, 82.525997400295523, 0.0, 0.0], [14.290816326530612, 14.290816326530612, 14.290816326530612, 0.0, 82.525997400295523, 0.0, 0.0], [14.454719387755102, 14.454719387755102, 14.454719387755102, 0.0, 82.525997400295523, 0.0, 0.0], [11.939413265306122, 11.939413265306122, 11.939413265306122, 0.0, 82.525997400295523, 0.0, 0.0], [12.299744897959183, 12.299744897959183, 12.299744897959183, 0.0, 82.525997400295523, 0.0, 0.0], [12.440688775510203, 12.440688775510203, 12.440688775510203, 0.0, 82.525997400295523, 0.0, 0.0], [11.645408163265307, 11.645408163265307, 11.645408163265307, 0.0, 82.525997400295523, 0.0, 0.0], [12.432397959183673, 12.432397959183673, 12.432397959183673, 0.0, 82.525997400295523, 0.0, 0.0], [13.03826530612245, 13.03826530612245, 13.03826530612245, 0.0, 82.525997400295523, 0.0, 0.0], [10.246811224489797, 10.246811224489797, 10.246811224489797, 0.0, 82.525997400295523, 0.0, 0.0], [9.606505102040817, 9.606505102040817, 9.606505102040817, 0.0, 82.525997400295523, 0.0, 0.0]]
    #speciesTrain = [1,3,2,5,2,5,4,6,3,7,4,1,5,4,3,5,7,8,4,2,5,9,7,4,3,2,7,6,8,7,6,5,6,7,9,0,5,3,1,2,3,2,5,6,0,6,0,6,0,5]

    #BSSImList, BSS_Train = BSSTrain()
    imageName = 'images/Research_May15_small.jpeg' 
    tileSize = 100  #define the tilesize and overlap to be used in training and testing. 
    overlap = 0.2
    n = tileSize

    #Training modes: 
        #1: Transect training only.
        #2: Read in from previously saved data for transects
        #3: Transect and research, with research unsegmented (left at original size)
        #4: Read in from previously saved data for transects and research. 
        #5: Research, with research segmented further to match test size. 
    
    if trainingMode == 1:
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
    if trainingMode == 2: 
        f = open('TransectMetricTraining.txt', 'r') 
        data = f.read() 
        metricTrain = eval(data) 
        
        g = open('TransectSpeciesTraining.txt', 'r') 
        data = g.read() 
        speciesTrain = eval(data) 
    if trainingMode == 3: 
        imList, coordLeft, coordRight, speciesList, numFlowers = createAllResearchTraining()
        speciesList = numericalSpecies(speciesList)
        metricTrainResearch, speciesTrainResearch = allTrainMetrics(imList, speciesList)
        
        ### Save the training set  - metrics
        f = open('RADMetricTraining.txt', 'w')
        print >> f, list(metricTrainResearch)
        f.close()
                
        ### Save the training set - densities 
        f = open('RADSpeciesTraining.txt', 'w')
        print >> f, list(speciesTrainResearch)
        f.close()
        
        FullImList, FullSpeciesList = createAllTransectTraining()
        metricTrainTransect, speciesTrainTransect = allTrainMetrics(FullImList, FullSpeciesList) #get training metrics 
        
        metricTrain = metricTrainResearch
        speciesTrain = speciesTrainResearch
        metricTrain.extend(metricTrainTransect) #combine metric lists
        speciesTrain.extend(speciesTrainTransect) #Combine the species lists. 
        
        flowerTrain = [1 if i else 0 for i in speciesTrain] #create a list of species training that only denotes flower vs. non-flower 
        
        ### Save the training set  - metrics
        f = open('TransectTrainSpecies.txt', 'w')
        print >> f, list(metricTrain)
        f.close()
                
        ### Save the training set - densities 
        f = open('TransectTrainSpecies.txt', 'w')
        print >> f, list(speciesTrain)
        f.close()
        
        ### Save the training set - flower vs. non-flower 
        f = open('FlowerTrain.txt', 'w')
        print >> f, list(flowerTrain)
        f.close()

    if trainingMode == 4: 
        f = open('TotalMetricTraining.txt', 'r') 
        data = f.read() 
        metricTrain = eval(data) 
        
        g = open('TotalSpeciesTraining.txt', 'r') 
        data = g.read() 
        speciesTrain = eval(data) 
        
        flowerTrain = [1 if i else 0 for i in speciesTrain]
    if trainingMode == 5: #Training based on segmented research area images. 
        transectIms, transectSpecies = createBSSTraining() #Get a list of images and species for the transects. 
        transectSpecies = numpy.asarray(transectSpecies)
        transectIms = numpy.asarray(transectIms)
        nonFlowerLocations = numpy.nonzero(transectSpecies)   
        nonFlowerSpecies = numpy.delete(transectSpecies, nonFlowerLocations, None)
        nonFlowerIms = numpy.delete(transectIms, nonFlowerLocations, None)
        
        nonFlowerIms = np.asarray(nonFlowerIms) #Convert to a numpy array to allow for index selection
        nonFlowerSpecies = np.asarray(nonFlowerSpecies) 
        
        #indices = np.random.choice(len(nonFlowerSpecies), 5) #Randomly choose 300 samples of non-flowers 
        #usednonFlowerIms = nonFlowerIms[indices] #Use only the randomly chosen images. 
        #usednonFlowerSpecies = nonFlowerSpecies[indices]
                                
        metricTrainTransect, speciesTrainTransect = tiledTraining(nonFlowerIms, nonFlowerSpecies, n, overlap) #get training metrics for transects, non-flower only. 
        
        #Now that you have all of the image, randomly choose several to use so that teh data set remains balanced. 
        indices = np.random.choice(len(metricTrainTransect), 50) #Randomly choose 50 sample images of non-flowers 
        metricTrainTransect = np.asarray(metricTrainTransect) 
        speciesTrainTransect = np.asarray(speciesTrainTransect)
        metricTrainTransect = metricTrainTransect[indices] 
        speciesTrainTransect = speciesTrainTransect[indices]
        
        #Input the segmented research area images. 
        imListResearch, coordLeft, coordRight, speciesListResearch, numFlowers = createAllResearchTraining()  #Get all of the training images and species information 
        speciesListResearch_num = numericalSpecies(speciesListResearch) #Convert to a numerical species (i.e. 1,2,3 instead of names)
        metricTrainResearch, speciesTrainResearch = tiledTraining(imListResearch, speciesListResearch_num, n, overlap) #get the metrics for segmented research images. 
        #Combine the two kinds of training data to create one comprehensive list. 
        metricTrain = np.concatenate((metricTrainTransect, metricTrainResearch), axis = 0) #add the research data at the end of the training list for metrics. 
        speciesTrain = np.concatenate((speciesTrainTransect, speciesTrainResearch), axis = 0)
        
            
        flowerTrain = [1 if i else 0 for i in speciesTrain] #create a list of species training that only denotes flower vs. non-flower 
        #Save all of the training data to files so that it can be read in without calculation in the future. 
        ### Save the training set - metrics 
#        f = open('metricTrainFull.txt', 'w')
#        print >> f, list(metricTrain)
#        f.close()
#
#        ### Save the training set - species 
#        f = open('speciesTrainFull.txt', 'w')
#        print >> f, list(speciesTrain)
#        f.close()

        np.save('metricTrainFull', metricTrain)
        np.save('speciesTrainFull', speciesTrain)
#        
        ### Save the training set - flower vs. non-flower 
        f = open('FlowerTrainFull.txt', 'w')
        print >> f, list(flowerTrain)
        f.close()
        
    if trainingMode == 6: 
        f = open('metricTrainFull.txt', 'r') 
        data = f.read() 
        metricTrain = eval(data) 
        
        g = open('speciesTrainFull.txt', 'r') 
        data = g.read() 
        speciesTrain = eval(data) 
        
        h = open('FlowerTrainFull.txt', 'r') 
        data = h.read() 
        flowerTrain = eval(data)

        speciesTrain = [int(i) for i in speciesTrain]
    #Training data has been acquired. Scale the metrics.
    metricTrain = np.asarray(metricTrain) 
    scaledMetrics, scaler = scaleMetrics(metricTrain) #scale the metrics and return both the scaled metrics and the scaler used. 
    kbest = SelectKBest(k = 19) 
    newMetrics = kbest.fit_transform(scaledMetrics, speciesTrain) #Select onlyk the k best metrics. (Comment out to use all metrics.)
    #Train the classifier (or classifiers in a 2 stage process). 
    clf_flower = classifyKNN(newMetrics, flowerTrain) #fit a function that only considers flower vs. non-flower 
    print(len(newMetrics[0]))
    #Find all of the zero training points in the set. 
    flower_locations = numpy.nonzero(speciesTrain) #Find all of the nonzero (i.e. actually flower) elements 
    speciesTrain = np.asarray(speciesTrain) #convert to a numpy array. 
    newMetrics = np.asarray(newMetrics)
    speciesTrain_nonzero = speciesTrain[list(flower_locations[0])] #Create an array containing only the data points for flowers. 
    metricTrain_nonzero = newMetrics[list(flower_locations[0])] #similarly reduce the metrics array to only the corresponding metrics. 
    
    clf_species = classifyTree(metricTrain_nonzero, speciesTrain_nonzero) #Fit a function to distinguish between species. 
    
    #return clf, speciesTrain, newMetrics, scaler, tileSize, overlap, kbest
    species = classifyMap_2stage(clf_species, clf_flower, speciesTrain, newMetrics, scaler, imageName, tileSize, overlap, kbest)
    #classifyMap(clf_species, speciesTrain, newMetrics, scaler, imageName, tileSize, overlap, kbest)   
    plt.show()

    return species
    
def parameterSearch(): 
    iris = datasets.load_iris()
    parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10]}
    svr = svm.SVC()
    clf = grid_search.GridSearchCV(svr, parameters)
    clf.fit(iris.data, iris.target)
    return clf

# Allows us to simply run SpeciesTest without needing to load it in first.
#if __name__ == '__main__':
#        species = SpeciesTest(6) #currently running with training mode five. 

