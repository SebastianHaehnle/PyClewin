# -*- coding: utf-8 -*-
"""
Created on Mon Sep 05 11:20:37 2016

@author: sebastian
"""

from PyClewin import *

import numpy as np

filename = 'clepytest.cif'
layers = collections.OrderedDict()
layers['SiNwafer'] = '0f00ffcb'
layers['MSgnd'] =  '0ff00ff00'
layers['SiNdiel'] = '0f00cbff'
layers['MSline'] = '0ff0000ff'
#    layers['Circles'] = '0f808080'
layers['Hybrids'] = '0fff0000'
layers['TantalumFront'] = '0f888800'
layers['TantalumBack'] = '0fc0c0c0'
layers['SiNbackside'] = '0fff00cb'
layers['text'] = '0f000000'
# misc stuff at the start
introScript()
# define Layers
introLayers()
for i, k in enumerate(layers):
    addLayer(i, k, layers[k])

# write actual symbols
introSymbols()
defineSymbol(1, 'Main')
# .. first symbol here
meshbla = 36

a = [0, 0, 1]
b = [0, 1000, 1]
c = [300, 1000, 1]
d = [300, 700, 0]
e = [700, 700, 0]
f = [700, 1000, 1]
g = [1000, 1000, 1]
h = [1000, 0, 1]

layername('MSline')
foo = parts.CPWs.CPW(2,2,36,100, gndlayer ='MSline')

foo.wirego(1, 100)

go(-1e3, -1e3)
setmark('test')
go(1e3, 1e3)
foo.connect(connector(-1, 'test'))


#alignmentCircles('Hybrids')
#alignmentSquares('MSgnd')

#endSymbol()



#misc stuff at the end
outroScript(1)
# write to file
writeScript(filename)

#print gg.cle
#print gg.s
