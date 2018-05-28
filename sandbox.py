import numpy
import scipy.constants as spc

from clepywin import *

import sympy as sym
import sympy.geometry as symgeo

hwafer = 375
membot = 2542

memtop = membot - 2*KOHetchWidth(hwafer)

#print membot, memtop

hlist = [355, 394]
xmasklist = [2486., 2542.]
xmeaslist = [1991., 1997.]
dxlist = [0,0]
theta = [0,0]

def calcdx(meas, mask):
    return (mask - meas)/2.


def calctheta(hwafer, dx):
    return np.arctan(hwafer/dx)/spc.degree

for i in xrange(len(xmeaslist)):
    dxlist[i] = calcdx(xmeaslist[i], xmasklist[i])
    theta[i] = calctheta(hlist[i], dxlist[i])

print dxlist
print theta




#print fun(1, 2)
#print otherfun(1,2)


#%%



