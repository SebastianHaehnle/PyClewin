# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 10:30:11 2017

@author: sebastian
"""

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
    #antenna sizes
    wAntList = [0, 500, 1000, 2000, 3000]
    deltaMem = 200.
    antLocations = [[-5300, 6250], [-300, 6250], [4700, 6250], [-4000, -5750], [3000, -5750]]

    blindpos = [[-2500, 6200], [2000, 6200]]

    # KOH etch stuff
    if hWafer == None:
        hWafer = 375 # Thickness of wafer
    deltaKOH = KOHetchWidth(hWafer) # underetch due to KOH angle
#    membraneXYbot = npa([3000, 30000]) for wAnt in wAntList
    membraneXYtop = [npa([max(wAnt+deltaMem, 1200), max(wAnt+deltaMem, 1200)]) for wAnt in wAntList] # design size for membrane
    membraneXYbot = [imem + 2*deltaKOH for imem in membraneXYtop] # size of SiN opening on backside
    hTrenches = hWafer * 0.35
    wTrenches = 2*KOHetchWidth(hTrenches)
    holeTolerance = 30. #tolerance for alignment hole size
  
    #    Readoutline offset from chip edge
    distanceRoEdge = 1.5e3
    distanceRoBot = 3e3
#==============================================================================
#    Define KID 
#==============================================================================
    epsalOffmem = 6.6
    epsw = 7.77

    Qdatafile = 'C:\Users\sebastian\ownCloud\p27lib\clepywin\chip\M4002leakytest\kidQc_16-6-16_10-20-10.dat'  
    
    Nkidsmem = 5
    F0mem = [4.8e9, 5.0e9, 5.2e9, 5.4e9, 5.6e9]
    Qcmem = 20e3
    Nkidsblind = 2
    F0blind = [6.0e9, 7.5e9]
    Qcblind = 50e3
    kidDc = 6
    Nkids = Nkidsmem + Nkidsblind
    l0al = 1.5e-3
    F0 = 4.9e9
#    lal = [1.5e-3]*Nkids
    lwidemem, lalmem = kd.scaleHybridLengths(F0mem, F0, l0al, epsalOffmem, epsw)
    print lalmem
    lwidemem, lalOffmem = kd.scaleHybridLengths(F0blind, F0, l0al, epsalOffmem, epsw)
    print lalOffmem
#    name = ['leaky', 'onMembrane', 'offMembrane']

    kids = []
    index = 0
    for i in xrange(Nkidsmem):
        kids.append(kd.customHybrid(F0mem[i], epsalOffmem, lalmem[i], epsw, Qcmem, Qdatafile, name = 'membrane', index = index))
        index += 1
#    for i in xrange(Nkidsblind):
    kids.append(kd.customHybrid(F0blind[0], epsalOffmem, lalOffmem[0], epsw, Qcblind, Qdatafile, name = 'blind', index = index))
    index += 1
    kids.append(kd.customHybrid(F0blind[1], epsalOffmem, 0, epsw, Qcblind, Qdatafile, name = 'nbtin', index = index))
    
    
    kiddatafile = 'leakytest_antennasize_kidinfo.dat'
    with open(kiddatafile, 'w') as ff:
        ff.write('kidid\tF0\tlal\tQc\tname\n')
        for k in kids:
            ff.write('%d\t%d\t%f\t%f\t%s\n' % (k.index, k.F0, k.lal, k.Qc, k.name))
    # blind kid short positions relativ to center of antenna
    
#==============================================================================
#   Start clewin script  
#==============================================================================

    chipsize = testchip20x20(layers = layers)
    # Each location: Antenna + membrane + KID
    for i in xrange(len(antLocations)):
        gomark('antenna')
        go(*antLocations[i])
        setmark('memcenter')
        # Antenna
        if wAntList[i] == 0:
            setmark('antennaShort%d' % i)
        elif wAntList[i] == 4000:
            leakyStraight(-1j, kidHybrid, wAntList[i], 30, 'antennaShort%d' % i)
        elif antLocations[i][1] < 0:
            leakyAdjustable(-1j, kidHybrid, wAntList[i], 'antennaShort%d' % i)
        else:
            leakyAdjustable(1j, kidHybrid, wAntList[i], 'antennaShort%d' % i)
        # Membrane
        layername('SiNbackside')
        bar(1, *membraneXYbot[i])
        layername('text')
        bar(1, *membraneXYtop[i])
        # direct coupled kid
        gomark('antennaShort%d' % i)
        if antLocations[i][1] < 0:
            kidStraight(1j, kids[i], None, kidHybrid, kidWide, lShort, None, kidTrans, externalSiN = ['SiNwafer', sinWidth])
        else:
            kidStraight(-1j, kids[i], None, kidHybrid, kidWide, lShort, None, kidTrans, externalSiN = ['SiNwafer', sinWidth])
        layername('SiNwafer')
        gomark('memcenter')
        if antLocations[i][1] < 0:
            wire(-1j, 2.5e3, 400.)
            sinsize = max(y2m('KIDsin%d' % i) + sinWidth, membraneXYtop[i][1]/2. + 500)
            wire(1j, sinsize, 400)
        else:
            wire(1j, 2.5e3, 400.)
            sinsize = y2m('KIDsin%d' % i) + sinWidth
            wire(-1j, sinsize, 400)
        gomark('memcenter')
        go(200, 0)
        wire(1, max(1.8e3, membraneXYtop[i][0]/2 + 1e3), 5e3)
        gomark('memcenter')
        go(-200, 0)
        wire(-1, max(1.8e3,membraneXYtop[i][0]/2 + 1e3), 5e3)    
    
    # Place blindkids
    for i, pos in enumerate(blindpos):
        gomark('antenna')
        go(*pos)
        kidStraight(-1j, kids[-(i+1)], None, kidHybrid, kidWide, lShort, None, kidTrans, externalSiN = ['SiNwafer', sinWidth])
#==============================================================================
#     Draw readoutline
#==============================================================================
    # line from left bondpad
    gomark('bondpadleft')
    bondpadM4001(-1, ro, x2m('chip00'))
    ro.wirego(1, distanceRoEdge, bridgeStart = True)
    setmark('readout_left')
    # line from right bondpad
    gomark('bondpadright')
    bondpadM4001(1, ro, x2m('chipFF'))
    ro.wirego(-1, distanceRoEdge, bridgeStart = True)
    # order kids from right to left
    xpos = [gg.mark['KIDend%d' % k.index][0][0] for k in kids]
    a = sorted(zip(xpos,kids))
    kidordered = [k for (pos,k) in a][::-1]

    for k in kidordered:
        marker = 'KIDend%d' % k.index
        print k.index, gg.mark['KIDend%d' % k.index][0], k.F0
        if gg.mark['KIDend%d' % k.index][0][1] < chipsize[1]/2.:
            couplerM4000left(-1j, marker, k.lcouple, kidDc, kidWide, ro, roRadius)
        else:
            couplerM4000(marker, k.lcouple, kidDc, kidWide, ro, roRadius)
            
    ro.wirego(-1, x2m('readout_left'))
    # add blindkids
    
#==============================================================================
#     Draw SiN everywhere except KIDs
#==============================================================================
#    gomark('antenna')
#    distanceNosinChipY = min([y2m('KIDsin%d' % k.index) for k in kid]) + sinWidth/2.
#    distanceNosinCenterX = 1e3    
#    layername('SiNwafer')
#    wire(1j, y2m('chipFF'), 2*distanceNosinCenterX)
#    wire(-1j, distanceNosinChipY, 2*distanceNosinCenterX)
#    go(distanceNosinCenterX, 0)
#    wire(1, x2m('chipFF'), 2*y2m('chipFF'))
#    go(-2*distanceNosinCenterX, 0)
#    wire(-1, x2m('chip00'), 2*y2m('chipFF'))
    
#==============================================================================
#   Border of chip: Draw Al cleaving lines, trenches and isolate chips
#==============================================================================
    
    def drawBorders(ldraw, wdraw):
        gomark('chip00')
        go(x2m('chipFF')/2., wdraw/2.)
        bar(1, ldraw[0], wdraw)
        gomark('chip00')
        go(wdraw/2., y2m('chipFF')/2.)
        bar(1j, ldraw[1], wdraw)
        gomark('chipFF')
        go(-x2m('chip00')/2., -wdraw/2.)
        bar(1, ldraw[0], wdraw)
        gomark('chipFF')
        go(-wdraw/2., -y2m('chip00')/2.)
        bar(1j, ldraw[1], wdraw)

    layername('Hybrids')
    wCleave = 50
    drawBorders(chipsize, wCleave)
#    gomark('chip00')
#    go(x2m('chipFF')/2., wIso/2.)
#    bar(1, chipsize[0], wIso)
#    gomark('chip00')
#    go(wIso/2., y2m('chipFF')/2.)
#    bar(1j, chipsize[1], wIso)
#    gomark('chipFF')
#    go(-x2m('chip00')/2., -wIso/2.)
#    bar(1, chipsize[0], wIso)
#    gomark('chipFF')
#    go(-wIso/2., -y2m('chip00')/2.)
#    bar(1j, chipsize[1], wIso)
#
    layername('MSgnd')
    wIso = 80
    drawBorders(chipsize, wIso)

    
#    layername('SiNbackside')
#    lTrenches = (chipsize[0] - 600, chipsize[1] - 600)
#    wTrenches = wTrenches
#    drawBorders(lTrenches, wTrenches)
    
#==============================================================================
#     Write some stuff
#==============================================================================
    layername('Hybrids')
    gomark('chip00')
    go(1e3, y2m('chipFF')-1e3)
#    Qstring = 'Qc = %de3' % int(Qc[0]/1000)
    text(1, 'M4001 v1 antennasize', 200)
#    go(0, -1e3)
#    text(1, Qstring, 500)
#==============================================================================
#     end
#==============================================================================
    return chipsize, kids


    

#==============================================================================
# Final touches    
#==============================================================================      


if __name__ == '__main__':
    filename = 'leakytest_antennasize.cif'

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
    size, kids = main()
    
    outroScript(symbols.keys()[-1])
    # write to file
    writeScript(filename)