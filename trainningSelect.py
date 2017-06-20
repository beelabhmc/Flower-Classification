#!/usr/bin/python
#import systotal = len(sys.argv)
import glob

"""cmdargs = str(sys.argv)
print ("The total numbers of args passed to the script: %d " % total)
print ("Args list: %s " % cmdargs)
# Pharsing args one by one
print ("Script name: %s" % str(sys.argv[0]))
print ("First argument: %s" % str(sys.argv[1]))
print ("Second argument: %s" % str(sys.argv[2]))"""

def getTrainingList(year='****', month='**',date='**', location='Research', species='****'):
    hand=open('newNonFlower.txt', 'r')
    nonFlowerIms = hand.readlines()
    nonFlowerIms = [x.strip() for x in nonFlowerIms] 
    grepItem=year+'-'+location+'-'+species+'.jpg'
    files = nonFlowerIms.glob(grepItem)
    return files

