# -*- coding: utf-8 -*-
"""
Created on Wed Sep 07 15:56:57 2016

@author: sebastian
"""

from clepywin import *
import numpy as np

def msl_delayline(wmsl, ltot, mesh, wsin, rturn):
    x_kidright = 500
    x_kidleft = 100
    x_lower = 0
    lturntot = 4 * rturn*np.pi/2.
    y_downmax = 7e3    
    
#    some logic to deal with delay line being longer than length of one up+down section
    lmax = 2*y_downmax + x_kidright + x_kidleft + lturntot
    lmin = x_kidright + x_kidleft + lturntot
    if ltot < lmin:
        msgo(1, ltot, wmsl, wsin)
    else:
        N = np.ceil(ltot/lmax)
        lsect = ltot / N
        y_down = (lsect - x_kidright - x_kidleft - lturntot)/2.   
    #    print y_down
    #    drawing long delay line
        for n in range(int(N)):
            msgo(1, x_kidright, wmsl, wsin)
            msdowngo(1, rturn, wmsl, mesh, wsin)
            msgo(-1j, y_down, wmsl, wsin)
            msupgo(-1j, rturn, wmsl, mesh, wsin)
            msupgo(1, rturn, wmsl, mesh, wsin)
            msgo(1j, y_down, wmsl, wsin)
            msdowngo(1j, rturn, wmsl, mesh, wsin)
            msgo(1, x_kidleft, wmsl, wsin)
    setmark('thzwire')
            

def msl_delayline_up(wmsl, ltot, ydiff, mesh, wsin, rturn = 100):
    x_kidright = 500
    x_kidleft = 100
    x_lower = 0
    lturntot = 4 * 100*np.pi/2.
    y_downmax = 7e3
    
#    some logic to deal with delay line being longer than length of one up+down section
    lmax = 2*y_downmax + ydiff + x_kidright + x_kidleft + lturntot
    lmin = x_kidright + x_kidleft + lturntot
    if ltot < lmin:
        msgo(1, ltot, wmsl, wsin)
    else:
        N = np.ceil(ltot/lmax)
        lsect = ltot / N
        y_down = (lsect - x_kidright - x_kidleft - lturntot - ydiff) / 2.
        y_up = y_down + ydiff
    #    print y_down
    #    drawing long delay line
        for n in range(int(N)):
            msgo(1, x_kidright, wmsl, wsin)
            msdowngo(1, rturn, wmsl, mesh, wsin)
            msgo(-1j, y_down, wmsl, wsin)
            msupgo(-1j, rturn, wmsl, mesh, wsin)
            msupgo(1, rturn, wmsl, mesh, wsin)
            msgo(1j, y_up, wmsl, wsin)
            msdowngo(1j, rturn, wmsl, mesh, wsin)
            msgo(1, x_kidleft, wmsl, wsin)
    setmark('thzwire')
    
def msl_sCurve(wmsl, lx, ly, mesh, wsin, rturn = 100):
    x_kidleft = 100.
    lx1 = lx - x_kidleft - 2*rturn
    lx2 = x_kidleft
    ly = ly - 2*rturn
    msgo(1, lx1, wmsl, wsin)
    msupgo(1, rturn, wmsl, mesh, wsin)
    msgo(1j, ly, wmsl, wsin)
    msdowngo(1j, rturn, wmsl, mesh, wsin)
    msgo(1, lx2, wmsl, wsin)
    setmark('thzwire')
    
    

if __name__ == '__main__':
    msl_delayline(1.4, 30e3, 36)