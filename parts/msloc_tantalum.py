# -*- coding: utf-8 -*-
"""
Created on Mon Oct 03 11:04:04 2016

@author: sebastian
"""

from clepywin import *

import numpy as np
npa = np.array

def msloc_tantalum_mesh(layer, d_sq = 3, l_sq = 50):
    layername(layer)    
    
    # 350 GHz    
#    l_sq = 113
#    d_sq = 7
    # 850 GHz = default
    d_sq = d_sq
    l_sq = l_sq - d_sq    
    
    gomark('chip00')
    lx_chip, ly_chip = dist2mark('chipFF')
    squares_inverse('TantalumFront', ly_chip, lx_chip, l_sq, d_sq)
    # TODO add free spaces


    
    
    
    
#==============================================================================
# #    Alternative 
#==============================================================================
#    # Top side of antenna
#    gomark('antenna')
#    go(0, d_leaky)
#    lx = dist2mark('chip00')[0]
#    ly = dist2mark('chipFF')[1]    
#    lx_upperedge = (ly-d_edge)/np.tan(np.pi/4.)
#    polyupper = [[0, lx_upperedge, lx_upperedge, -lx, -lx], [0, ly-d_edge, ly, ly, 0]]
#    poly(polyupper) 
#
#    # Bottom side of antenna    
#    gomark('antenna')
#    go(0, -d_leaky)
#    lx1 = dist2mark('chip00')[0]
#    lx2 = dist2mark('tunnelout')[0]
#    ly = dist2mark('chip00')[1]
#    polylower = [[-lx1, -lx1, lx2, lx2], [0, -ly, -ly, 0]]
#    poly(polylower)
##    squares(layer, polylower, l_sq, d_sq)
#
#    # Left side of antenna
#    gomark('antenna')
#    go(-d_leaky, 0)
#    lx = dist2mark('chip00')[0]
#    ly = d_leaky
#    polyleft = [[0, -lx, -lx, 0], [ly, ly, -ly, -ly]]
#    poly(polyleft)
#
#    # Right side of antenna
#    gomark('antenna')
#    go(d_leaky, 0)
#    lx1 = dist2mark('tunnelin')[0]
#    lx2 = dist2mark('tunnelout')[0]
#    ly = d_leaky
#    polyright = [[0, lx1, lx2, lx2, 0], [0, lx1*np.tan(np.pi/4.), lx1*np.tan(np.pi/4.), -ly, -ly]]
#    poly(polyright)
#    
#    gomark('chip00')
#    go(lx_upperedge, dist2mark('chipFF')[1] - d_edge/2.)
#    wire(1, dist2mark('chipFF')[0], d_edge)
#
#    gomark('chip00')
#    go(dist2mark('tunnelout')[0], d_edge/2.)
#    wire(1, dist2mark('chipFF')[0], d_edge)
    
