flowers = [610,960,327,1984,5487,19,7,11,59,4,7,16,11,174]
locations = [1,2,3,5,8,14,16,18,21,26,27,46,49,50]


import numpy 

densList = numpy.zeros(50)

for i in range(len(locations)): 
    place = locations[i]-1 
    flowerCount = flowers[i]
    densList[place] = flowerCount 
    
    
finalList = []
for i in range(len(densList)): 
    newNum = int(densList[i])
    print newNum
    finalList += [newNum]

print finalList

f = open('uncleanedTraining.txt', 'w')
print >> f, finalList 
f.close()   


cleanedList = finalList 
for i in range(50): 
    if i+1 not in [5,6,7,8,12,13,14,15,16,17]+range(19, 51): 
        cleanedList[i] = 0
        
print cleanedList

f = open('cleanedTraining.txt', 'w')
print >> f, cleanedList 
f.close()   

