# -*- coding: utf-8 -*-
"""
Created on Tue Sep 06 13:00:39 2016

@author: sebastian
"""

from clepywin import *

def c_filter_msl_v1(wmsl, rturn, Lc, Lvert, mesh, wsin, is_solo = False):
    '''
    Draws c-shaped filter:
        (0,0)----
           ----
          -
          -
           ----
       input:
           wmsl : width of ms line
           rturn : radius of ms curve
           Lc : coupling length
           Lvert : vertical section
           mesh : meshing for ms curve
           wsin : width of SiN coverage
           is_solo : set to True if not attached to KID, default = False
    '''
#==============================================================================
#     SIN layer
#==============================================================================
    # if filter is with kid, do not draw SiN on other side of it
    if is_solo:
        xy = [[wsin/2., -(Lc+rturn+wsin/2.), -(Lc+rturn+wsin/2.), wsin/2.], [0, 0, -(2*rturn+Lvert+wmsl/2.), -(2*rturn+Lvert+wmsl/2.)]]
        layername('SiNdiel')
        poly(np.array(xy), shift = (0, dist2mark('thzwire')[1] - wsin/2.))
        layername('SiNwafer')
        xy = [[wsin, -(Lc+rturn+wsin), -(Lc+rturn+wsin), wsin], [0, 0, -(2*rturn+Lvert+wmsl/2.), -(2*rturn+Lvert+wmsl/2.)]]
        poly(np.array(xy), shift = (0, dist2mark('thzwire')[1] - wsin))
    else:
        pass     
#==============================================================================
# MSline layer
#==============================================================================    
    layername('MSline')
    wire(1, manVars.nbtinLine, wmsl)
    wirego(-1, Lc, wmsl)
    turnupgo(-1, rturn, wmsl, mesh)
    wirego(-1j, Lvert, wmsl)
    turnupgo(-1j, rturn, wmsl, mesh)
    wirego(1, Lc, wmsl)
    wire(1, manVars.nbtinLine, wmsl)
#   SiN part

    
        

if __name__ == '__main__':
    pass
    