# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 13:47:42 2016

@author: sebastian
"""

from clepywin import *
from .msloc_kid_v1 import transition_mslhyb, transition_mslcpw
from .msloc_readout import msloc_bridge

import numpy as np

LOVERLAP = 7

def msloc_linetermination(wmsl, wsin, wtrans, strans, ltrans, wterm, sterm, lterm, rturn, xyspace, mesh, layer0 = 'MSgnd', layer1 = 'MSline', layer2 = 'SiNdiel', layer3 = 'Hybrids', layer4 = 'SiNwafer'):
    setmark('inner')
    # MSL - CPW transition
    taperangle = 30.
    taperangle = taperangle * np.pi/180.
    ltaper = (wtrans + 2*strans - wmsl)/2. / np.tan(taperangle)
    transition_mslcpw(wmsl, wtrans, strans, wsin, ltaper)
    # lambda/4 transformer    
    layername(layer0)
    wire(-1j, ltrans, wtrans + 2*strans)
    layername(layer1)
    wirego(-1j, ltrans, wtrans)    
    # Taper to hybrid
    setmark('temp')
    ltaper = LOVERLAP * 2
    layername(layer0)
    broaden(-1j, ltaper, wtrans + 2*strans, wterm + 2*sterm)
    layername(layer1)    
    wire(-1j, 0.75*ltaper, wtrans)
    layername(layer3)    
    go(0, -0.25*ltaper)
    wirego(-1j, 0.75*ltaper, wterm)
    # start absorbing section
    lturns = 2 * rturn*np.pi
    xsec = xyspace[0] - 2*rturn   
    wcpw = wterm + 2*sterm
    
    y0 = 100
    layername(layer0)
    wire(-1j, y0, wcpw)
    layername(layer3)
    wirego(-1j, y0, wterm)
    lterm -= y0
    Nsec = np.ceil(lterm / (2*xsec + lturns))
    for i in range(int(Nsec)):
        setmark('temp')
#        def bridgefun(direction, function, wcpw, scpw, *kwargs):
#            msloc_bridge(-1j, wterm, sterm)
#            layername(layer0)
#            function(direction, *kwargs)
#        bridgefun(-1j, turnupgo, wterm, sterm, rturn, wcpw, mesh)
        layername(layer0)
        turnupgo(-1j, rturn, wcpw, mesh)
        wirego(1, xsec, wcpw)
        turndowngo(1, rturn, wcpw, mesh)
        turndowngo(-1j, rturn, wcpw, mesh)
        wirego(-1, xsec, wcpw)
        turnupgo(-1, rturn, wcpw, mesh)
        gomark('temp')
        layername(layer3)
        turnupgo(-1j, rturn, wterm, mesh)
        wirego(1, xsec, wterm)
        turndowngo(1, rturn, wterm, mesh)
        turndowngo(-1j, rturn, wterm, mesh)
        wirego(-1, xsec, wterm)
        turnupgo(-1, rturn, wterm, mesh)
    layername(layer3)
    wire(-1j, 10, wterm)
    layername(layer4)
    xy = [[-2*wsin, -2*wsin, xyspace[0] + 2*wsin, xyspace[0] + 2*wsin], [-2*wsin, dist2mark('inner')[1], dist2mark('inner')[1], -2*wsin]]
    poly(xy)    
    
    
if __name__ == '__main__':
    wmsl = 1.4
    wsin = 30
    wterm = 1.4
    sterm = 4.0
    lterm = 5e3
    rturn = 1e2
    xyspace = [2e3, 5e3]
    mesh= 36
    msloc_linetermination(wmsl, wsin, wterm, sterm, lterm, rturn, xyspace, 36)
    
