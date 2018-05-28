# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 13:28:34 2017

@author: sebastian
"""

from clepywin import *

import chip.M4002leakytest_update as chip

filename = 'M4002waferbasis.cif'

layers = collections.OrderedDict()
layers['SiNwafer'] = '0f00ffcb'
layers['MSgnd'] =  '0ff00ff00'
layers['text'] = '05000000'
layers['SiNbackside'] = '0fff00cb'
layers['Hybrids'] = '0fff0000'
layers['dummy0'] = '00000000'
layers['SiNdiel'] = '0f00cbff'
layers['AlignmentHoles'] = '0fff00ff'
layers['TantalumFront'] = '0f00f000'
layers['TantalumBack'] = '0fc0c0c0'
      
# Define the base unit for all lengths in the design
unit_scale = 1e3    # micron
gg.scale = unit_scale

# Wafer definitions:
hWafer = 375


introScript()
introLayers()
for i, k in enumerate(layers):
    print i, k
    addLayer(i, k, layers[k])

# Define symbols (i.e. chips)
symbols = {1 : 'lowQ',
           2 : 'mediumQ',
           3 : 'highQ',
           4 : 'sizetest', 
           5 : 'Main'}
introSymbols()
#low Qc chip
defineSymbol(*symbols.items()[0])
setmark('wafercenter')
sizeLowq = chip.M4002_v2_leakytest_lowq.main(hWafer)
endSymbol()
gomark('wafercenter') # ensure that you start at 0 for next symbol
#medium Qc chip
defineSymbol(*symbols.items()[1])
setmark('wafercenter')
sizeHighq, kid = chip.M4002_v2_leakytest_mediumq.main(hWafer)
endSymbol()
gomark('wafercenter') # ensure that you start at 0 for next symbol
#high Qc chip
defineSymbol(*symbols.items()[2])
setmark('wafercenter')
sizeHighq, kids = chip.M4002_v2_leakytest_highq.main(hWafer)
endSymbol()
gomark('wafercenter') # ensure that you start at 0 for next symbol
#sizetest chip
defineSymbol(*symbols.items()[3])
setmark('wafercenter')
sizeHighq, kids = chip.M4002_v2_leakytest_antennasize.main(hWafer)
endSymbol()
gomark('wafercenter') # ensure that you start at 0 for next symbol

# Draw wafer
numx = 3
numy = 3
chipgrid = [(-30e3+i*sizeLowq[0], -30e3+(numy-1-j)*sizeLowq[1]) for j in xrange(numy) for i in xrange(numx)]
lowqpos = [1,2]
mediumqpos = [3,4,5]
highqpos = [6,7]
sizetest = [0,8]
# place chips
toplevelSymbol(*symbols.items()[-1])
for i, pos in enumerate(chipgrid):
    if i in lowqpos:
        placeSymbol(1, pos)
    elif i in mediumqpos:
        placeSymbol(2, pos)
    elif i in highqpos:
        placeSymbol(3, pos)
    elif i in sizetest:
        placeSymbol(4, pos)
        
# draw trenches
layername('SiNbackside')
gaptrenches = 300
ltrenches = sizeLowq[0] - 2*gaptrenches
wtrenches = 2*KOHetchWidth(0.39*hWafer)

for pos in chipgrid:
    gomark('wafercenter')
    go(*pos)
    go(gaptrenches, 0)
    wirego(1, ltrenches, wtrenches)
    go(gaptrenches, gaptrenches)
    wirego(1j, ltrenches, wtrenches)
    go(-gaptrenches, gaptrenches)
    wirego(-1, ltrenches, wtrenches)
    go(-gaptrenches, -gaptrenches)
    wirego(-1j, ltrenches, wtrenches)

maskorder = [0, 1, 6, 5, 4, 7]
# write dummy as nr 5 so nothing is written in sinbackside
maskversion = [1, 1, 1, 1, 1, 1]
gomark('wafercenter')
go(0, 35e3)
for i in xrange(len(maskorder)):
    layer(maskorder[i])
    text(1, 'M4001-%d v%d' % (i+1, maskversion[i]), 100)
    go(0, -100)
    


outroScript(len(symbols))
# write to file
writeScript(filename)