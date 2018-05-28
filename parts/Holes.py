# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 17:15:47 2017

@author: sebastian
"""

from clepywin import *

def juansHoles1990(backsidelayer, frontsidelayer, hwafer, tolerance, gndlayer, tantalumFront = None, tantalumBack = None):
    """
    Alignment holes for 20x20 testchip, positioning as in M4000, copied from Juans leaky antennas
    """
    sizeHoleFront = 1990.
    sizeHoleBack = sizeHoleFront + 2*KOHetchWidth(hwafer) + tolerance
    def dohole():    
        layername('text')
        square(sizeHoleFront)
        layername(backsidelayer)
        square(sizeHoleBack)
        layername(frontsidelayer)
        square(sizeHoleFront + 200)
        layername(gndlayer)
        square(sizeHoleFront + 200)
        if tantalumFront:
            layername(tantalumFront)
            square(sizeHoleFront + 220)
        if tantalumBack:
            layername(tantalumBack)
            square(sizeHoleBack + 20)
            
    holePos = [[5500, 5500], [0, -11000], [-11000, 0], [0, 11000]] 
            
    gomark('antenna') #chip center
#    go(5500, 5500) # top right
    go(*holePos[0])
    dohole()
#    go(0, -11000) # bot right
    go(*holePos[1])
    dohole()
#    go(-11000, 0) # bot left
    go(*holePos[2])
    dohole()
    go(*holePos[3])
#    go(0, 11000) # top left
    dohole()
    return holePos
    