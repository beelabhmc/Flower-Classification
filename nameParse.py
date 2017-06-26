speciesDict={'NOFL': 0,
            'SAAP':'Salvia apiana',
            'MAVU': 'Marrubium vulgare',
            'ERTR':'Eriodictyon trichocalyx',
            'PESP': 'Penstemon spectabilis',
            'ACGL': 'Acmispon glaber',
            'CRIN':'Cryptantha intermedia'}

def getSpeciesandImg():
    hand=open('selectedTrainingImgs.txt', 'r')
    imgs = hand.readlines()
    imgs = [x.strip() for x in imgs] 
    noflList=[]
    noflImgs=[]
    speciesList=[]
    speciesImgs=[]
    for i in imgs:
        for key in list(speciesDict.keys()):
            if key in i:
                if key=='NOFL':
                    noflList.append(speciesDict[key])
                    noflImgs.append(i)
                else:
                    speciesList.append(speciesDict[key])
                    speciesImgs.append(i)
    return noflList, noflImgs, speciesList, speciesImgs

