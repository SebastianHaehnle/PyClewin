# -*- coding: utf-8 -*-
"""
Created on Thu Sep 08 10:29:21 2016

Functions:
    msloc_readout_attachright()
    msloc_bondpad()


@author: sebastian
"""

from clepywin import *

def msloc_bridge(direction, w_cpw, s_cpw):
    wsin_bridge = 40.
    wnbtin_bridge = 20.
    lsin_addbridge = 30.
    lnbtin_addbridge = 65.
    layer1 = 'SiNdiel'
    layer2 = 'MSline'
    lsin = w_cpw + 2*s_cpw + lsin_addbridge
    lnbtin = lsin + lnbtin_addbridge
    layername(layer1)
    bar(direction, wsin_bridge, lsin)
    layername(layer2)
    bar(direction, wnbtin_bridge, lnbtin)
    
def msloc_bridge_cpwonly(direction, w_cpw, s_cpw):
    wsin_bridge = 40.
    wnbtin_bridge = 20.
    lsin_addbridge = 30.
    lnbtin_addbridge = 65.
    layer1 = 'SiNdiel'
    layer2 = 'Hybrids'
    lsin = w_cpw + 2*s_cpw + lsin_addbridge
    lnbtin = lsin + lnbtin_addbridge
    layername(layer1)
    bar(direction, wsin_bridge, lsin)
    layername(layer2)
    bar(direction, wnbtin_bridge, lnbtin)    

def msfb_bridge(direction, w_cpw, s_cpw):
    wsin_bridge = 30.
    wnbtin_bridge = 10.
    lsin_addbridge = 20.
    lnbtin_addbridge = 55.
    layer1 = 'SiNdiel'
    layer2 = 'MSline'
    lsin = w_cpw + 2*s_cpw + lsin_addbridge
    lnbtin = lsin + lnbtin_addbridge
    layername(layer1)
    bar(direction, wsin_bridge, lsin)
    layername(layer2)
    bar(direction, wnbtin_bridge, lnbtin)

def msloc_readout_attachright(kidmark, Lc, dc, wwide, swide, wro, sro, rturn, mesh, bridgefun, cornerbridge = True, **kwargs):
    d_bridge_0 = 100
    x_dist = swide + dc + sro + (wwide + wro)/2   
    setmark('temp')
    gomark(kidmark)
    go(x_dist, 0)    
    ro_go(1j, Lc, wro, sro, bridgefun, **kwargs)
    ro_downgo(1j, rturn, wro, sro, mesh, bridgefun, bridge = False, **kwargs)    
    ro_downgo(1, rturn, wro, sro, mesh, bridgefun, bridge = cornerbridge, **kwargs)
    ro_go(-1j, Lc, wro, sro, msloc_bridge)
    ro_go(-1j, dist2mark('temp')[1]-rturn, wro, sro, bridgefun, d_bridge_0 = d_bridge_0, **kwargs)
    ro_upgo(-1j, rturn, wro, sro, mesh, bridgefun, **kwargs)
    ro_go(1, dist2mark('temp')[0], wro, sro, bridgefun, **kwargs)
    gomark(kidmark)
    go(x_dist, 0)
    ro_go(-1j, dist2mark('temp')[1]-rturn, wro, sro, bridgefun, d_bridge_0 = d_bridge_0, **kwargs)
    ro_downgo(-1j, rturn, wro, sro, mesh, bridgefun, **kwargs)
    
def msloc_bondpad(wro, sro, wsin, wbond = 600., sbond = 225., ltaper = 500., lbond = 400., lisolation = 50., layer0 = 'MSgnd', layer4 = 'SiNwafer'):
    '''
    bondpad geometry from sonnet for 50 Ohm, crosschecked with Svens tool
    '''
    setmark('temp')
    layername(layer4)
    wire(1, (ltaper + lbond), 600 + 2*sbond + 2*wsin)
    layername(layer0)
    cpwbroadengo(1, ltaper, wro, sro, wbond, sbond)
    cpwgo(1, lbond, wbond, sbond)
    # Add isolation from ground
    wire(-1, lisolation, wbond + 2*sbond)
    gomark('temp')    

def msloc_bondpad(wro, sro, wsin, wbond = 600., sbond = 225., ltaper = 500., lbond = 400., lisolation = 50., layer0 = 'MSgnd', layer4 = 'SiNwafer'):
    '''
    bondpad geometry from sonnet for 50 Ohm, crosschecked with Svens tool
    '''
    setmark('temp')
    layername(layer4)
    wire(1, (ltaper + lbond), 600 + 2*sbond + 2*wsin)
    layername(layer0)
    cpwbroadengo(1, ltaper, wro, sro, wbond, sbond)
    cpwgo(1, lbond, wbond, sbond)
    # Add isolation from ground
    wire(-1, lisolation, wbond + 2*sbond)
    gomark('temp')    

 
def ro_go(direction, L, w_cpw, s_cpw, bridgefun, d_bridge_0 = None, bridge_delta = 2e3, layer0 = 'MSgnd', layer1 = 'SiNdiel', layer2 = 'MSline', layer4 = 'SiNwafer', **kwargs): 
    w_sincpw = (w_cpw + s_cpw)
    layername(layer4)
    wire(direction, L, w_sincpw)
    if d_bridge_0:
        layername(layer0)
        cpwgo(direction, d_bridge_0, w_cpw, s_cpw)
        bridgefun(direction, w_cpw, s_cpw, **kwargs)
        L -= d_bridge_0
    for i in range(int(L/bridge_delta)):
        layername(layer0)
        cpwgo(direction, bridge_delta, w_cpw, s_cpw)
        bridgefun(direction, w_cpw, s_cpw, **kwargs)
        L -= bridge_delta
    layername(layer0)
    cpwgo(direction, L, w_cpw, s_cpw)

    
def ro_upgo(direction, r, w_cpw, s_cpw, mesh, bridgefun, layer0 = 'MSgnd', layer1 = 'SiNdiel', layer2 = 'MSline', layer4 = 'SiNwafer', bridge = True, **kwargs):
    w_sincpw = (w_cpw + s_cpw)
    rot(direction)
    if bridge:
        bridgefun(1, w_cpw, s_cpw, **kwargs)
    layername(layer4)
    turnup(1, r, w_sincpw, mesh)
    layername(layer0)
    cpwupgo(1, r, w_cpw, s_cpw, mesh)
    if bridge:
        bridgefun(1j, w_cpw, s_cpw, **kwargs)
    layername(layer0)
    rot(np.conjugate(direction))

def ro_downgo(direction, r, w_cpw, s_cpw, mesh, bridgefun, layer0 = 'MSgnd', layer1 = 'SiNdiel', layer2 = 'MSline', layer4 = 'SiNwafer', bridge = True, **kwargs):
    w_sincpw = (w_cpw + s_cpw)
    rot(direction)
    if bridge:
        bridgefun(1, w_cpw, s_cpw, **kwargs)
    layername(layer4)
    turndown(1, r, w_sincpw, mesh)
    layername(layer0)
    cpwdowngo(1, r, w_cpw, s_cpw, mesh)
    if bridge:
        bridgefun(-1j, w_cpw, s_cpw, **kwargs)
    layername(layer0)
    rot(np.conjugate(direction))

if __name__ == '__main__':
    pass    
