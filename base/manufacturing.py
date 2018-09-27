# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 16:36:04 2016

@author: sebastian
"""

import scipy.constants as spc
import numpy as np


class manVars():
    '''
    Stores variables for processing overetching and stuff
    just add these values to all lines with the appropriate material
    (e.g. for width of hybrid al part do #width = width + manVars.alLine)
    '''
    alLine = 0.6
    nbtinLine = 0.1 * 2
    nbtinSlot = -0.1 * 2

def KOHetchWidth(hWafer):
    theta = 54.7*spc.pi/180.
    return hWafer/np.tan(theta)

def KOHopening(t_wafer, w_membrane):
    return w_membrane + 2*KOHetchWidth(t_wafer)

if __name__ == '__main__':
    hlist = [350, 375]
    KOHdict = {}
    for h in hlist:
        KOHdict[h] = KOHetchWidth(h)

    d_target = 1990
    d_mask = d_target + 2*KOHdict[350]
    d_add = KOHdict[350]
    print d_mask, d_add