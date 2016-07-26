f = open('TransectMetricTraining.txt', 'r') 
data = f.read() 
metricTrain = eval(data) 

g = open('TransectSpeciesTraining.txt', 'r') 
data = g.read() 
speciesTrain = eval(data) 