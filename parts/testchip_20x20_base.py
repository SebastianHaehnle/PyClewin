# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 16:14:01 2016

@author: sebastian
"""

from clepywin import *

import scipy.constants as spc

def testchip_20x20_base(layers, mesh):
    lx_chip = 20e3
    ly_chip = 20e3
    layername('text')
    setmark('chip00')   
   
    # Antenna origin
    go(lx_chip/2., ly_chip/2.)
    setmark('antenna')
    go(lx_chip/2., ly_chip/2.)
    setmark('chipFF')       
    gomark('chip00')    
    # Chip corners
    def writecorner(direction):
        '''
        written for bottom left
        '''
        
        setmark('temp')
        rot(direction)
        go(0,25)
        wire(1, 2000, 50)
        go(25, -25)
        wire(1j, 2000, 50)
        gomark('temp')
    writecorner(1)
    go(lx_chip, 0)
    writecorner(1j)
    go(0, ly_chip)
    writecorner(-1)
    go(-lx_chip, 0)
    writecorner(-1j)
    
    # define starting positions of readout CPW
    dx_bondpad = 1e3
    gomark('chip00')
    go(dx_bondpad, ly_chip/2.)
    setmark('bondpadleft')
    gomark('chip00')
    go(lx_chip - dx_bondpad, ly_chip/2.)
    setmark('bondpadright')
    
    
    
    # Draw trenches   
    KOHangle = 54.7
    KOHangle *= spc.degree
    h_wafer = 350.
    cornerspace = 300
    h_trenches = h_wafer * 0.35
    w_draw = h_trenches / np.tan(KOHangle) * 2
    
    layername('SiNbackside')
    gomark('chip00')
    

#    go(cornerspace, 0)
#    wirego(1, x2m('chipFF') - cornerspace, w_draw)
#    go(cornerspace, cornerspace)
#    wirego(1j, y2m('chipFF') - cornerspace, w_draw)
#    go(-cornerspace, cornerspace)
#    wirego(-1, x2m('chip00') - cornerspace, w_draw)
#    go(-cornerspace, -cornerspace)
#    wirego(-1j, y2m('chip00') - cornerspace, w_draw)   
    
    gomark('chip00')
    
