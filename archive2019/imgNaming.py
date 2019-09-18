import numpy
import csv
from Constants import *
import os

def addNum(LS):
    unique=list(set(LS))
    outName=[]
    for one in unique:
        c=1
        for i in range(len(LS)):
            if LS[i]==one:
                LS[i]=LS[i]+'-'+str(c).zfill(2)+'.jpg'
                c+=1  
    return LS  


def noneFlowerImgs():
    """saves the list new nams for the nonFlower transect images"""
    hand=open('oldNonFlower.txt', 'r')
    old = hand.readlines()
    old = [x.strip() for x in old]
    year='2016'
    LocationCode=[x[7:10] for x in old]
    SpeciesCode='NOFL'
    DATE=[]
    monthday=''
    for i in old:
        j=i.split('_')
        if j[1]=='June8':
            DATE+=[year+'0608']
        elif j[1]=='June3':
            DATE+=[year+'0603']
        elif j[1]=='May26':
            DATE+=[year+'0526']
        elif j[1]=='May19':
            DATE+=[year+'0519']
    new =list(map(lambda x,y: "images/new/"+x+"-"+y+"-"+SpeciesCode, DATE, LocationCode))
    handout=open('newNonFlower.txt', 'w')
    new2=addNum(new)
    for i in new2:
        print>>handout, i
    handout.close()
    return old, new


    





def getImgNamesAndSpecies():
    """return a list of current image names as strings and a list of is corresponding species"""
    #Initialize empty lists to store all of the relevant information.  
    imageNames = []
    SpeciesList = []
    NumFlowers = []   
    #with open('Research Map Data Association - Sheet1.csv', 'rb') as csvfile: 
    with open('EditedResearchMapData.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        i = 0 
        for row in reader:
            if i == 0: #throw out the first row. 
                print(i) 
            elif len(row)<8: 
                print("Row too short")
            else:
                if row[2] == '' or row[3] == '' or row[4] == '' or row[5] == '' or row[7] == '': 
                    print('missing information')
                else: 
                    imageNames += ['images/' + row[2] + '.jpg']
                    SpeciesList += [row[5]]
                    NumFlowers += [float(row[7])]
            i += 1
        return imageNames, SpeciesList
    

def FlowerImgs(imageNames, SpeciesList, LocationCode="REA"):
    newNames=[]
    for i in range(len(imageNames)):
        if 'April24' in imageNames[i]:
            DATE='20160424'
        elif 'April29' in imageNames[i]:
            DATE='20160429'
        elif 'May15' in imageNames[i]:
            DATE='20160515'
        elif 'May20' in imageNames[i]:
            DATE='20160520'
        else:
            print("ERROR")
        word=str(SpeciesList[i])
        spList=word.split(' ')
        spCode=spList[0][:2]+spList[1][:2]
        spCode=spCode.upper()
        newNames+=["images/new/"+DATE+'-'+LocationCode+'-'+spCode]
    new2=addNum(newNames)
    handout=open('newFlower.txt', 'w')
    for i in new2:
        print>>handout, i
    handout.close()
    return imageNames, new2



def main():
    nm, sp=getImgNamesAndSpecies()
    oldF, newF=FlowerImgs(nm, sp)
    old, new=noneFlowerImgs()
    print(old)
    print(new)
    for i in range(len(old)):
        os.system("mv "+old[i]+" "+new[i])
    for i in range(len(oldF)):
        os.system("mv "+oldF[i]+" "+newF[i])




if __name__ == '__main__':
   #main()


