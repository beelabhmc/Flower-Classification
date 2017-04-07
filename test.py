import numpy
a = [1,0,9,8,0,8,6,5,6,0,9,8,9,0,3,0,9,0,9,0,0,0,0,78,9,9,0,0]
a = numpy.asarray(a)
locs = numpy.nonzero(a)   
b = numpy.delete(a, locs, None)
                                    
