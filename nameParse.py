speciesDict={'NOFL': 'No flower',
            'SAAP':'Salvia apiana',
            'MAVU': 'Marrubiumvulare',
            'ERTR':'Eriodictyon trichcalyx',
            'PESP': 'Pestemon spectabilis',
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
    print(imgs)
    for i in imgs:
        for key in list(speciesDict.keys()):
            if key in i:
                if key=='NOFL':
                    noflList.append(speciesDict[key])
                    noflImgs.append(i)
                else:
                    speciesList.append(speciesDict[key])
                    speciesImgs.append(i)
        print(i)
    return noflList, noflImgs, speciesList, speciesImgs

