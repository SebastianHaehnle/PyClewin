# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 14:11:32 2017

@author: sebastian
"""

from clepywin import *

import numpy as np
import scipy.constants as spc
import collections
import mwlib as mw
import KIDdesignNew as kd
npa = np.array

def main(hWafer = None):    
    import commonParts
#    Define meshing for corners
    mesh = 36   
    
#==============================================================================
# Define lines
#==============================================================================
    lShort = 10 # Length of shorts on KIDs
    sinWidth = 120

    kidTrans = transHybridWideM4000
    
    #----------- KID sections
    kidHybrid = CPWhybrid(line = 2.0 + manVars.alLine,
                              gap = 2.4 + (manVars.nbtinSlot-manVars.alLine)/2.,
                              linelayer = 'Hybrids',
                              gndlayer = 'MSgnd',
                              mesh = mesh)
    
    kidWide = CPW(line = 6. + manVars.nbtinLine,
                      gap = 16. + manVars.nbtinSlot,
                      mesh = mesh,
                      gndlayer = 'MSgnd')
    kidRadius = 50.
    #Bridge
    roBridgefun = bridgeM4000CPWleaky.draw
    
    ro = CPWreadout(line = 20. + manVars.nbtinLine, 
                gap = 10. + manVars.nbtinSlot, 
                cpwlayer = 'MSgnd', 
                diellayer = 'SiNwafer', 
                bridgefun = roBridgefun, 
                bridgeDistance = 2e3, 
                mesh = mesh)
    roRadius = 80.
    
#==============================================================================
#     Define other geometries
#==============================================================================
    # KOH etch stuff
    if hWafer == None:
        hWafer = 375 # Thickness of wafer
    deltaKOH = KOHetchWidth(hWafer) # underetch due to KOH angle
    membraneXYtop = npa([1200, 1200]) # design size for membrane
    membraneXYbot = membraneXYtop + 2*deltaKOH # size of SiN opening on backside
    hTrenches = hWafer * 0.35
    wTrenches = 2*KOHetchWidth(hTrenches)
    holeTolerance = 25. #tolerance for alignment hole size
  
    #    Readoutline offset from chip edge
    distanceRoEdge = 1.5e3
    distanceRoBot = 3e3
#==============================================================================
#    Define KID 
#==============================================================================
    epsalOnmem = 3.76
    epsalOffmem = 6.6
    epsw = 7.77

    Qdatafile = 'C:\Users\sebastian\ownCloud\p27lib\clepywin\chip\M4002leakytest_update\kidQc_16-6-16_10-20-10.dat'  
    
    Nkids = 3
    F0 = [5.0e9, 5.2e9, 5.4e9]
    Qc = [2e3, 50e3, 50e3]
    kidDc = 6
    lal = [1.5e-3]*Nkids
    epsal = [epsalOnmem, epsalOnmem, epsalOffmem]
    name = ['leaky', 'onMembrane', 'offMembrane']

    kid = [None]*Nkids
    for i in xrange(Nkids):
        kid[i] = kd.customHybrid(F0[i], epsal[i], lal[i], epsw, Qc[i], Qdatafile, name = name[i], index = i)    
    # blind kid short positions relativ to center of antenna
    locationKids = [[0,0], [550, -320], [-650, -1000]] # on membrane and off membrane
    
#==============================================================================
#   Start clewin script  
#==============================================================================



    
    chipsize = testchip20x20(layers = layers)
    holePos = juansHoles1990('SiNbackside', 'AlignmentHoles', hWafer, holeTolerance, 'MSgnd', 
                   tantalumFront = 'TantalumFront',
                   tantalumBack = 'TantalumBack')
    
    # Antenna
    gomark('antenna')
    leakyM4001(1j, kidHybrid)
    # Membrane
    layername('SiNbackside')
    bar(1, *membraneXYbot)
    layername('text')
    bar(1, *membraneXYtop)
    # direct coupled kid
    gomark('antennaShort')
    kidStraight(-1j, kid[0], None, kidHybrid, kidWide, lShort, None, kidTrans, externalSiN = ['SiNwafer', sinWidth])
    
    #Draw blind kids
    #Draw blind kids
    # On membrane
    gomark('antenna')
    go(*locationKids[1])
    lmemkid = membraneXYtop[1]/2.
    kidM4001membrane(-1j, kid[1], kidHybrid, kidWide, lShort, kidTrans, ['SiNwafer', sinWidth], [lmemkid, lmemkid - abs(locationKids[1][1])], kidRadius)
    
    
    # Off membrane
    gomark('antenna')
    go(*locationKids[2])
    kidStraight(-1j, kid[2], None, kidHybrid, kidWide, lShort, None, kidTrans, externalSiN = ['SiNwafer', sinWidth])
    
#==============================================================================
#     Draw readoutline
#==============================================================================
    # line from left bondpad
    gomark('bondpadleft')
    bondpadM4001(-1, ro, x2m('chip00'))
    gomark('bondpadleft')
    ro.wirego(1, distanceRoEdge, bridgeStart = True)
    ro.downgo(1, roRadius)
    ro.wirego(-1j, y2m('chip00') - distanceRoBot)
    ro.upgo(-1j, roRadius)
    setmark('readout_left')
    # line from right bondpad
    gomark('bondpadright')
    bondpadM4001(1, ro, x2m('chipFF'))
    ro.wirego(-1, distanceRoEdge, bridgeStart = True)
    ro.upgo(-1, roRadius)
    ro.wirego(-1j, y2m('chip00') - distanceRoBot)
    ro.downgo(-1j, roRadius)
    setmark('readout_right')
    ro.wirego(-1, 1e3)
    # order kids from right to left
    xpos = [gg.mark['KIDend%d' % k.index][0][0] for k in kid]
    a = sorted(zip(xpos,kid))
    kidordered = [k for (pos,k) in a][::-1]

    for k in kidordered:
        marker = 'KIDend%d' % k.index
        couplerM4000(marker, k.lcouple, kidDc, kidWide, ro, roRadius)
    ro.wirego(-1, x2m('readout_left'))
    # add blindkids
    
#==============================================================================
#     Draw SiN everywhere except KIDs
#==============================================================================
    gomark('antenna')
    distanceNosinChipY = min([y2m('KIDsin%d' % k.index) for k in kid]) + sinWidth/2.
    distanceNosinCenterX = 1e3    
    layername('SiNwafer')
    wire(1j, y2m('chipFF'), 2*distanceNosinCenterX)
    wire(-1j, distanceNosinChipY, 2*distanceNosinCenterX)
    go(distanceNosinCenterX, 0)
    wire(1, x2m('chipFF'), 2*y2m('chipFF'))
    go(-2*distanceNosinCenterX, 0)
    wire(-1, x2m('chip00'), 2*y2m('chipFF'))
    
#==============================================================================
#   Border of chip: Draw Al cleaving lines, trenches and isolate chips
#==============================================================================
    


    layername('Hybrids')
    wCleave = 50
    commonParts.drawBorders(chipsize, wCleave)
    layername('MSgnd')
    wIso = 80
    commonParts.drawBorders(chipsize, wIso)

    
#    layername('SiNbackside')
#    lTrenches = (chipsize[0] - 600, chipsize[1] - 600)
#    wTrenches = wTrenches
#    drawBorders(lTrenches, wTrenches)
    

#==============================================================================
# Write tantalum meshes, GND plane removal
#==============================================================================

    
    commonParts.tantalumMesh(chipsize, membraneXYbot, membraneXYtop, ro, kidWide)
    
    

#==============================================================================
#     Write some stuff
#==============================================================================
    layername('Hybrids')
    gomark('antenna')
    go(-3e3, y2m('chipFF')/2. + 1e3)
    Qstring = 'Qc = %de3' % int(Qc[0]/1000)
    text(1, 'M4001 leaky', 500)
    go(0, -1e3)
    text(1, Qstring, 500)
    
#    gomark('chip00')
#    go(1e3, y2m('chipFF')-1e3)
    
#==============================================================================
#     end
#==============================================================================
    return chipsize


    

#==============================================================================
# Final touches    
#==============================================================================      


if __name__ == '__main__':
    filename = 'M4002_v2_leaky_lowQc.cif'

    layers = collections.OrderedDict()
    layers['SiNwafer'] = '0f00ffcb'
    layers['MSgnd'] =  '0ff00ff00'
    layers['SiNdiel'] = '0f00cbff'
#    layers['MSline'] = '0ff0000ff'
    layers['Hybrids'] = '0fff0000'
    layers['SiNbackside'] = '0fff00cb'
    layers['text'] = '05000000'
    layers['AlignmentHoles'] = '0fff00ff'
    layers['TantalumFront'] = '0f888800'
    layers['TantalumBack'] = '0fc0c0c0'          
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
    size = main()
    
    outroScript(symbols.keys()[-1])
    # write to file
    writeScript(filename)