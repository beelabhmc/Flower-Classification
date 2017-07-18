import re
import argparse
from Constants import *
import os

def itFinder(yearL, monL, dayL, specL, locL):
    matches = []
    trainImgs = os.listdir(IMAGE_PATH+'new')
    trainImgs=list(map(lambda x:IMAGE_PATH+'new/'+x, trainImgs))
    print(trainImgs)
    #trainImgs = [x.strip() for x in trainImgs] 
    yearL=list(map(lambda x:str(x), yearL))
    monthL=list(map(lambda x:str(x).zfill(2), monL))
    dayL=list(map(lambda x:str(x).zfill(2), dayL))
    locL=list(map(lambda x:str(x), locL))
    specL=list(map(lambda x:str(x), specL))
    if yearL:
        reyear=''
        for i in range(len(yearL[0])):
            yearint=str([int(''.join(list(map(lambda x:x[i], yearL))))])
            reyear+=yearint
    else:
        reyear='....'
    if monthL:
        remonth=''
        for i in range(len(monthL[0])):
            monint=str([''.join(list(map(lambda x:x[i], monthL)))]).replace("\'","")
            remonth+=monint
    else:
        remonth='..'
    if dayL:
        reday=''
        for i in range(len(dayL[0])):
            dayint=str([''.join(list(map(lambda x:x[i], dayL)))]).replace("\'","")
            reday+=dayint
    else:
        reday='..'
    if locL:
        reloc=''
        for i in range(len(locL[0])):
            locint=str([''.join(list(map(lambda x:x[i], locL)))])
            reloc+=locint
    else:
        reloc='...'
    if specL:
        respec=''
        for i in range(len(specL[0])):
            speint=str([''.join(list(map(lambda x:x[i], specL)))])
            respec+=speint
    else:
        respec='....'
    regex='images\/new\/'+reyear+remonth+reday+'[\-]'+reloc+'[\-]'+respec+'\-..\.jpg'
    print(regex)
    for name in trainImgs:
        a=re.match(regex, name)
        if a:
            mat=a.group(0)
            matches.append(mat)
    return matches

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--years',
                            type=str,
                            default=[],
                            help='a list of desired years')
    arg_parser.add_argument('--months',
                            type=str,
                            default=[],
                            help='a list of desired months')
    arg_parser.add_argument('--days',
                            type=str,
                            default=[],
                            help='a list of desired days')
    arg_parser.add_argument('--locations',
                            type=str,
                            default=[],
                            help='a list of desired locations')
    arg_parser.add_argument('--species',
                            type=str,
                            default=[],
                            help='a list of desired locations')
    args = arg_parser.parse_args()
    if args.years:
        yearL=args.years.split(',')
    else:
        yearL=[]
    if args.months:
        monL=args.months.split(',')
    else:
        monL=[]
    if args.days:
        dayL=args.days.split(',')
    else:
        dayL=[]
    if args.species:
        specL=args.species.split(',')
    else:
        specL=[]
    if args.locations:
        locL=args.locations.split(',')
    else:
        locL=[]
    print('you have selected training images with the following parameters:')
    print('year: '+str(yearL))
    print('month: '+str(monL))
    print('days: '+str(dayL))
    print('species: '+str(specL))
    print('locations: '+str(locL))
    matches=itFinder(yearL, monL, dayL, specL, locL)
    handout=open('selectedTrainingImgs.txt', 'w')
    for i in matches:
        print>>handout, i
    handout.close()

if __name__ == '__main__':
    main()
    