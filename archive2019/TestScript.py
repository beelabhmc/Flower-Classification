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

# Allows us to simply run SpeciesTest without needing to load it in first.
if __name__ == '__main__':
    SpeciesTest()