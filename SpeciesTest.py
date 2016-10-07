#This script is written to speed up the testing of species classification code. 
from classification import *
from SpeciesClassProbability import *
from TrainingSpeciesList import *
from SpeciesClass import *
from createTraining import *
from Verification import *
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectKBest
from sklearn import grid_search, datasets
from Constants import *

def SpeciesTest():
    
    #input a training set - list of metrics and the corresponding species. The 2 lists must be the same length. 
    #metricTrain= [[33.411989795918366, 33.411989795918366, 33.411989795918366, 0.0, 82.525997400295523, 0.016581632653061226, 0.0], [31.682397959183675, 31.682397959183675, 31.682397959183675, 0.0, 82.525997400295523, 0.014668367346938776, 0.03125], [32.691964285714285, 32.691964285714285, 32.691964285714285, 0.0, 82.525997400295523, 0.01403061224489796, 0.03125], [32.63647959183673, 32.63647959183673, 32.63647959183673, 0.0, 82.525997400295523, 0.01211734693877551, 0.21875], [32.61224489795919, 32.61224489795919, 32.61224489795919, 0.0, 82.525997400295523, 0.012755102040816327, 0.0], [30.714923469387756, 30.714923469387756, 30.714923469387756, 0.0, 82.525997400295523, 0.008928571428571428, 0.0], [30.896045918367346, 30.896045918367346, 30.896045918367346, 0.0, 82.525997400295523, 0.01594387755102041, 0.0], [30.852040816326532, 30.852040816326532, 30.852040816326532, 0.0, 82.525997400295523, 0.01594387755102041, 0.0625], [29.049744897959183, 29.049744897959183, 29.049744897959183, 0.0, 82.525997400295523, 0.01211734693877551, 0.03125], [26.432397959183675, 26.432397959183675, 26.432397959183675, 0.0, 82.525997400295523, 0.008290816326530613, 0.25], [27.523596938775512, 27.523596938775512, 27.523596938775512, 0.0, 82.525997400295523, 0.001913265306122449, 0.0625], [27.310586734693878, 27.310586734693878, 27.310586734693878, 0.0, 82.525997400295523, 0.009566326530612245, 0.0], [26.762755102040817, 26.762755102040817, 26.762755102040817, 0.0, 82.525997400295523, 0.005739795918367347, 0.0], [31.371173469387756, 31.371173469387756, 31.371173469387756, 0.0, 82.525997400295523, 0.016581632653061226, 0.0], [29.536989795918366, 29.536989795918366, 29.536989795918366, 0.0, 82.525997400295523, 0.016581632653061226, 0.0], [26.915816326530614, 26.915816326530614, 26.915816326530614, 0.0, 82.525997400295523, 0.011479591836734694, 0.0], [27.807397959183675, 27.807397959183675, 27.807397959183675, 0.0, 82.525997400295523, 0.016581632653061226, 0.0], [28.81313775510204, 28.81313775510204, 28.81313775510204, 0.0, 82.525997400295523, 0.015306122448979591, 0.0], [26.301020408163264, 26.301020408163264, 26.301020408163264, 0.0, 82.525997400295523, 0.01020408163265306, 0.0], [27.67283163265306, 27.67283163265306, 27.67283163265306, 0.0, 82.525997400295523, 0.015306122448979591, 0.0], [28.051020408163264, 28.051020408163264, 28.051020408163264, 0.0, 82.525997400295523, 0.005739795918367347, 0.03125], [26.443877551020407, 26.443877551020407, 26.443877551020407, 0.0, 82.525997400295523, 0.01020408163265306, 0.0], [27.12563775510204, 27.12563775510204, 27.12563775510204, 0.0, 82.525997400295523, 0.011479591836734694, 0.0], [27.998086734693878, 27.998086734693878, 27.998086734693878, 0.0, 82.525997400295523, 0.008290816326530613, 0.21875], [28.012117346938776, 28.012117346938776, 28.012117346938776, 0.0, 82.525997400295523, 0.010841836734693877, 0.25], [25.68813775510204, 25.68813775510204, 25.68813775510204, 0.0, 82.525997400295523, 0.01211734693877551, 0.0], [25.45216836734694, 25.45216836734694, 25.45216836734694, 0.0, 82.525997400295523, 0.01020408163265306, 0.0], [26.017857142857142, 26.017857142857142, 26.017857142857142, 0.0, 82.525997400295523, 0.016581632653061226, 0.25], [24.292729591836736, 24.292729591836736, 24.292729591836736, 0.0, 82.525997400295523, 0.012755102040816327, 0.0], [24.325892857142858, 24.325892857142858, 24.325892857142858, 0.0, 82.525997400295523, 0.0012755102040816326, 0.0], [19.853954081632654, 19.853954081632654, 19.853954081632654, 0.0, 82.525997400295523, 0.0, 0.0], [19.130102040816325, 19.130102040816325, 19.130102040816325, 0.0, 82.525997400295523, 0.0, 0.0], [16.59502551020408, 16.59502551020408, 16.59502551020408, 0.0, 82.525997400295523, 0.0, 0.21875], [14.911989795918368, 14.911989795918368, 14.911989795918368, 0.0, 82.525997400295523, 0.0, 0.0], [14.662627551020408, 14.662627551020408, 14.662627551020408, 0.0, 82.525997400295523, 0.0, 0.0], [15.293367346938776, 15.293367346938776, 15.293367346938776, 0.0, 82.525997400295523, 0.0, 0.0], [14.072704081632653, 14.072704081632653, 14.072704081632653, 0.0, 82.525997400295523, 0.0, 0.0], [12.860969387755102, 12.860969387755102, 12.860969387755102, 0.0, 82.525997400295523, 0.0006377551020408163, 0.0], [13.991071428571429, 13.991071428571429, 13.991071428571429, 0.0, 82.525997400295523, 0.0, 0.0], [15.65625, 15.65625, 15.65625, 0.0, 82.525997400295523, 0.0, 0.0], [14.290816326530612, 14.290816326530612, 14.290816326530612, 0.0, 82.525997400295523, 0.0, 0.0], [14.454719387755102, 14.454719387755102, 14.454719387755102, 0.0, 82.525997400295523, 0.0, 0.0], [11.939413265306122, 11.939413265306122, 11.939413265306122, 0.0, 82.525997400295523, 0.0, 0.0], [12.299744897959183, 12.299744897959183, 12.299744897959183, 0.0, 82.525997400295523, 0.0, 0.0], [12.440688775510203, 12.440688775510203, 12.440688775510203, 0.0, 82.525997400295523, 0.0, 0.0], [11.645408163265307, 11.645408163265307, 11.645408163265307, 0.0, 82.525997400295523, 0.0, 0.0], [12.432397959183673, 12.432397959183673, 12.432397959183673, 0.0, 82.525997400295523, 0.0, 0.0], [13.03826530612245, 13.03826530612245, 13.03826530612245, 0.0, 82.525997400295523, 0.0, 0.0], [10.246811224489797, 10.246811224489797, 10.246811224489797, 0.0, 82.525997400295523, 0.0, 0.0], [9.606505102040817, 9.606505102040817, 9.606505102040817, 0.0, 82.525997400295523, 0.0, 0.0]]
    #speciesTrain = [1,3,2,5,2,5,4,6,3,7,4,1,5,4,3,5,7,8,4,2,5,9,7,4,3,2,7,6,8,7,6,5,6,7,9,0,5,3,1,2,3,2,5,6,0,6,0,6,0,5]
    imageName = IMAGE_PATH + 'Research_May20Marked_S2P1.jpg' 
    #
    #BSSImList, BSS_Train = BSSTrain() 
    #
    #imageList = BSSImList #choose an image list and corresponding training list 
    #
    #speciesList = BSS_Train
    #
    #
    #metricTrain, speciesTrain = allTrainMetrics(imageList, speciesList)
    if 0:
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
    if 1: 
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
        

    
        ### Save the training set  - metrics
        f = open('TotalMetricTraining.txt', 'w')
        print >> f, list(metricTrain)
        f.close()
                
        ### Save the training set - densities 
        f = open('TotalSpeciesTraining.txt', 'w')
        print >> f, list(speciesTrain)
        f.close()
        
    if 0: 
        f = open('TotalSpeciesTraining.txt', 'r') 
        data = f.read() 
        metricTrain = eval(data) 
        
        g = open('TransectSpeciesTraining.txt', 'r') 
        data = g.read() 
        speciesTrain = eval(data) 
        
    scaledMetrics, scaler = scaleMetrics(metricTrain) #scale the metrics and return both the scaled metrics and the scaler used. 
    kbest = SelectKBest(k=5) 
    newMetrics = kbest.fit_transform(scaledMetrics, speciesTrain)
    
    clf = classifyRF(newMetrics, speciesTrain) #Fit a function 
    clf.feature_importances_
    
    tileSize = 100 
    overlap = 0.2
    classifyMap(clf, speciesTrain, newMetrics, scaler, imageName, tileSize, overlap, kbest)
        
    plt.show()


def parameterSearch(): 
    iris = datasets.load_iris()
    parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10]}
    svr = svm.SVC()
    clf = grid_search.GridSearchCV(svr, parameters)
    clf.fit(iris.data, iris.target)
    return clf

# Allows us to simply run SpeciesTest without needing to load it in first.
if __name__ == '__main__':
        SpeciesTest()
