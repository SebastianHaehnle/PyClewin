# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 16:02:29 2017

@author: sebastian
"""

from PyClewin import *

import numpy as np
import scipy.constants as spc
import collections

def leakyM4001(direction, cpw):
    """
    Leaky Antenna:
        BW = 300 GHz - 900 GHz
        Size: 990 um x 282.5 um
        Feed = CPW
        Designed by Ozan
    """
    wTotal = 990 #2778./3
    hTotal = 282.5
    wSlot = 3.
    hSlot = 2.
    lTaper = (wTotal - wSlot)/2.

    rot(direction)
    layername(cpw.gndlayer)
    bar(1j, wSlot, hSlot)
    go(0, wSlot/2.)
    broaden(1j, lTaper, hSlot, hTotal)
    go(0, -wSlot)
    broaden(-1j, lTaper, hSlot, hTotal)
    go(hSlot/2., wSlot/2.)
    rot(np.conjugate(direction))
    setmark('antennaShort')

def leakyAdjustable(direction, cpw, wTotal, markname = 'antennaShort'):
    wSlot = 3.
    hSlot = 2.

    hTotal = 282.5 * (wTotal - wSlot)/(990. - wSlot)
    lTaper = (wTotal - wSlot)/2.

    rot(direction)
    layername(cpw.gndlayer)
    bar(1j, wSlot, hSlot)
    go(0, wSlot/2.)
    broaden(1j, lTaper, hSlot, hTotal)
    go(0, -wSlot)
    broaden(-1j, lTaper, hSlot, hTotal)
    go(hSlot/2., wSlot/2.)
    rot(np.conjugate(direction))
    setmark(markname)
    return hTotal

def leakyAdjustableNarrow(direction, cpw, wTotal, markname = 'antennaShort'):
    hTotal = 10. # Check correct number from original leaky paper
    wSlot = 3.
    hSlot = 2.
    lTaper = (wTotal - wSlot)/2.

    rot(direction)
    layername(cpw.gndlayer)
    bar(1j, wSlot, hSlot)
    go(0, wSlot/2.)
    broaden(1j, lTaper, hSlot, hTotal)
    go(0, -wSlot)
    broaden(-1j, lTaper, hSlot, hTotal)
    go(hSlot/2., wSlot/2.)
    rot(np.conjugate(direction))
    setmark(markname)

def leakyStraight(direction, cpw, w, h, markname = 'antennaShort'):
    rot(direction)
    layername(cpw.gndlayer)
    bar(1j, w, h)
    go(h/2., 0)
    rot(np.conjugate(direction))
    setmark(markname)

if __name__ == '__main__':
    folder = r'C:\Users\sebastian\ownCloud\p27lib\clepywin'
    filename = 'part_leakyM4001.cif'
    import os
    filepath = os.path.join(folder, filename)

    layers = collections.OrderedDict()
    layers['SiNwafer'] = '0f00ffcb'
    layers['MSgnd'] =  '0ff00ff00'
    layers['SiNdiel'] = '0f00cbff'
#    layers['MSline'] = '0ff0000ff'
    layers['Hybrids'] = '0fff0000'
#    layers['TantalumFront'] = '0f888800'
#    layers['TantalumBack'] = '0fc0c0c0'
    layers['SiNbackside'] = '0fff00cb'
    layers['text'] = '05000000'
    layers['AlignmentHoles'] = '0fff00ff'

    # Define the base unit for all lengths in the design
    unit_scale = 1e3    # micron
    gg.scale = unit_scale
    #actual

    introScript()
    introLayers()
    for i, k in enumerate(layers):
        addLayer(i, k, layers[k])

    symbols = {1 : 'Main'}
    introSymbols()
    defineSymbol(*symbols.items()[0])
    kidHybrid = CPWhybrid(line = 2.0 + manVars.alLine,
                          gap = 2.4 + (manVars.nbtinSlot-manVars.alLine)/2.,
                          linelayer = 'Hybrids',
                          gndlayer = 'MSgnd',
                          mesh = 36)
    go(0, 0)
    print leakyAdjustable(1j, kidHybrid, 700)


    outroScript(symbols.keys()[-1])
    # write to file
    writeScript(filepath)
