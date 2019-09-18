from classification import * 
from Verification import *
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix
import Plot_Conf_Matrix as pcm


metricTrain = np.load('metricTrainFull.npy')
speciesTrain = np.load('speciesTrainFull.npy')

#
##f = open('TotalMetricTraining.txt', 'r') 
#f = open('metricTrainFull.txt', 'r')
#data = f.read() 
#metricTrain = eval(data) 
#
##g = open('TotalSpeciesTraining.txt', 'r') 
#g = open('speciesTrainFull.txt', 'r')
#data = g.read() 
#speciesTrain = eval(data) 
#print(sum(speciesTrain))

#split the data set. 
metric_train, metric_test, species_train, species_test = train_test_split(metricTrain, speciesTrain, test_size=0.5, random_state=0)

#species_train = [i if i<3 else 0 for i in species_train]
#species_test = [i if i<3 else 0 for i in species_test]
flower_train = [1 if i else 0 for i in species_train] #create a flower training set 
        
clfRF = classifyRF(metric_train, species_train) 
clfKNN = classifyKNN(metric_train, species_train)
#clfSVM = classifySVM(metric_train, species_train)
#clfSGD = classifySGD(metric_train, species_train)
#clfPercep = classifyPerceptron(metric_train, species_train)
clfTree = classifyTree(metric_train, species_train)

clf_flower =  classifyTree(metric_train, flower_train)

#print('Random Forest Scores')
#classReport(metric_test, species_test, clfRF)
#scores = VerifyTenfold(speciesTrain, metricTrain, clfRF)
#print('RF', np.mean(scores) )
#
#print('KNN Scores') 
#classReport(metric_test, species_test, clfKNN)
#scores = VerifyTenfold(speciesTrain, metricTrain, clfKNN)
#print('KNN', np.mean(scores) )


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
flower_locations = numpy.nonzero(species_train) #Find all of the nonzero (i.e. actually flower) elements 
species_train = np.asarray(species_train) #convert to a numpy array. 
metric_train = np.asarray(metric_train)
species_train_nonzero = species_train[list(flower_locations[0])] #Create an array containing only the data points for flowers. 
metric_train_nonzero = metric_train[list(flower_locations[0])] #Corresponding metrics 

clfRF_stage2 = classifyRF(metric_train_nonzero, species_train_nonzero)  #Train a new classifier on only flower data
clfTree_stage2 = classifyTree(metric_train_nonzero, species_train_nonzero)
clfKNN_stage2 = classifyKNN(metric_train_nonzero, species_train_nonzero) 
clfSGD_stage2 = classifySGD(metric_train_nonzero, species_train_nonzero)
clfPercep_stage2 = classifyPerceptron(metric_train_nonzero, species_train_nonzero)


y_true, y_pred = classReport_2stage(metric_test, species_test, clf_flower, clfRF_stage2) 
#conf_matrix = confusion_matrix(y_true, y_pred)
#scores = VerifyTenfold(speciesTrain, metricTrain, clfRF)
#print('2 stage', np.mean(scores))
print(classification_report(y_true, y_pred))


#Plot the Confusion matrix 

class_names = np.asarray(['Non-flower', 'Penstemon spectabilis', 'Acmispon glaber', 'Marrubium vulgare', 'Salvia apiana'])
# Compute confusion matrix
cnf_matrix = confusion_matrix(y_true, y_pred)
cnf_matrix2 = np.asarray([list(cnf_matrix[0]),list(cnf_matrix[1]),list(cnf_matrix[2]),list(cnf_matrix[3]),list(cnf_matrix[6])])  #Remove species that aren't of interest. 
cnf_matrix2 = np.delete(cnf_matrix2, 4, 1)
cnf_matrix2 = np.delete(cnf_matrix2, 4,1)
np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
plt.figure()
pcm.plot_confusion_matrix(cnf_matrix2, classes=class_names,
                      title='Confusion matrix, without normalization')

# Plot normalized confusion matrix
plt.figure()
cnf_matrix_normalized = np.round(cnf_matrix2.astype('float') / cnf_matrix2.sum(axis=1)[:, np.newaxis], decimals = 2)
print("Normalized confusion matrix")
pcm.plot_confusion_matrix(cnf_matrix_normalized, classes=class_names, normalize=False,
                      title='Normalized confusion matrix')

plt.show()


