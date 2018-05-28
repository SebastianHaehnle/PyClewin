# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 11:41:35 2016

@author: sebastian
"""

from clepywin import *

import numpy as np
import scipy.constants as spc
import collections
import mwlib as mw
import KIDdesignNew as newKD

import numpy as np
npa = np.array


if __name__ == '__main__' :
    filename = 'msloc1_leakytest_ms_v2.cif'

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
    layers['text'] = '05000000'
    # Define the base unit for all lengths in the design
    unit_scale = 1e3    # micron
    gg.scale = unit_scale
    
#    Define meshing for corners
    mesh = 36

#==============================================================================
#   LINE GEOMETRIES
#==============================================================================
    #MSL
    w_msl = 1.9  + manVars.nbtinLine    #width of line
    w_sin = 60.     #width of dielectric

#    Readout CPW
    w_ro = 19. + manVars.nbtinLine      #width of line
    s_ro = 8. + manVars.nbtinSlot       #width of slot
    
    r_ro = 100.             # radius of readoutline
    kid_offset = 5*r_ro     # distance of kid to readoutline (not coupling distance)
    
#    KID wide CPW
    w_wide = 6. + manVars.nbtinLine     #width of line
    s_wide = 16. + manVars.nbtinSlot    #width of slot
    
#    KID hybrid CPW
    w_hybrid = 1.4 + manVars.alLine #width of line
    s_hybrid = 2.4 + (manVars.nbtinSlot-manVars.alLine)/2. #width of slot
   
#   Bridge
    bridgefun = msloc_bridge   
    
#    Readoutline offset from chip edge
    offset_ro2chip = 1.5e3
#==============================================================================
# KID GEOMETRY
#==============================================================================
#    Epsilon effective
    epsms = 20.7 #for w=1.9 msl
    lambda600GHz = mw.f_2_lambda(600e9, epsms)*1e6
    l_transformer = lambda600GHz/4.    
    epsal = 9.78 # for GHz readout signal
    epsw = 7.77 #
    Zcpw = 85.0
    Zms = 82.0
#    filtkid kids
    def kidgenerator(epsms, epsal, epsw):
        # LENGTHS
        lal = 1.6e-3
        lms = 1550e-6
        #KID FREQUENCIES
        F0 = 5.5e9
        Fgap = None
        delgap = None
        FN = 5.5e9
        #KID Qc values
        Qc = 20e3
        Qcblind = 100e3
        #NUM KIDS
        Nbb = 0
        Nfilt = 0 
        Npure = 0 #outside readout band, noise with vna
        Nblind = 1      
        N = Nbb + Nfilt + Nblind
        Ffilt  = []
#        kids =  mw.KIDSdesign(F0, FN, N, epsal, lal, epsms, lms, epsw, Ffilt, Nblind, Fgap = Fgap, delgap = delgap)
        kids = newKD.KIDSdesign(F0, FN, N, epsal, lal, Zcpw, epsms, lms, Zms, epsw, Ffilt, Nblind, Fgap = Fgap, delgap = delgap)
        # generate coupling lengths for kids in original F-position
        path = 'C:\Users\sebastian\ownCloud\Chipdesign\M4000\msloc1\sonnet\msloc1_v1\kidQc.dat'                
        kids.gen_lcouple(path, Qc, Qcblind)
        return kids, Nblind + Npure
    kids, num_blind = kidgenerator(epsms, epsal, epsw)
    kid = kids[0]
#    blindkid = kids[1]
    d_kidQ_c = 6
    
    print kids
#==============================================================================
#     Start clewin script
#==============================================================================
    
    introScript()
    # define Layers
    introLayers()
    for i, k in enumerate(layers):
        addLayer(i, k, layers[k])
    # write actual symbols
    introSymbols()
    defineSymbol(1, 'MAIN')
    
#    Base chip
    testchip_20x20_base(layers, mesh)
#    Antenna
    leaky_300to900_990um(-1j, w_sin, directkid = True)
#    Remove Backside Tantalum at membrane and bondpads
    msloc_tantalum_mesh('TantalumBack')
    edge_chip = 1e3
#    layername('TantalumBack')
#    gomark('chip00')
#    go(0, y2m('chipFF')/2.)
#    wire(1, x2m('chipFF'), 2*y2m('chipFF'))
    gomark('bondpadleft')
    wire(-1, x2m('chip00'), 2*edge_chip)
    gomark('bondpadright')
    wire(1, x2m('chipFF'), 2*edge_chip)
    
#   Remove Frontside Tantalum everywhere
    layername('TantalumFront')
    gomark('chip00')
    go(0, y2m('chipFF')/2.)
    wire(1, x2m('chipFF'), 2*y2m('chipFF'))    
    
#    misc definitions
    gomark('chip00')
    l_chip = dist2mark('chipFF')[0]
#    write KID
    gomark('antennaOut')    
    msloc_kid_v2(kid, w_hybrid, s_hybrid, w_wide, s_wide, w_msl, 0, 0, 0, mesh, w_sin, kidid = 0, wmsl2 = w_msl)
#    write readout from left side
    gomark('bondpadleft')
    flip('x')
    msloc_bondpad(w_ro, s_ro, w_sin, wbond = 400)
    flip('x')
    ro_go(1, offset_ro2chip, w_ro, s_ro, bridgefun)
    ro_downgo(1, r_ro, w_ro, s_ro, mesh, bridgefun)
#    ro_go(-1j, y2m('KIDend0') + kid_offset, w_ro, s_ro, bridgefun) # adjust readout line to KID length
    ro_go(-1j, y2m('chip00') - 3e3, w_ro, s_ro, bridgefun)
    ro_upgo(-1j, r_ro, w_ro, s_ro, mesh, bridgefun)
    setmark('readout_left')
#    write readout from right side
    gomark('bondpadright')
    msloc_bondpad(w_ro, s_ro, w_sin, wbond = 400)
    ro_go(-1, offset_ro2chip, w_ro, s_ro, bridgefun)
    ro_upgo(-1, r_ro, w_ro, s_ro, mesh, bridgefun)
#    ro_go(-1j, dist2mark('KIDend0')[1] + kid_offset, w_ro, s_ro, bridgefun) # adjust readout line to KID length
    ro_go(-1j, y2m('chip00') - 3e3, w_ro, s_ro, bridgefun)
    ro_downgo(-1j, r_ro, w_ro, s_ro, mesh, bridgefun)
    # Enter blindkid
    if len(kids) == 2:
        setmark('roline')
        go(-l_chip/8., kids[1].ltot*1e6 + kid_offset)
        msloc_kid_v2(kids[1], w_hybrid, s_hybrid, w_wide, s_wide, w_msl, 0, 0 ,0, mesh, w_sin, kidid = 1)
        gomark('roline')
        msloc_readout_attachright('KIDend1', kid.lcouple, d_kidQ_c, w_wide, s_wide, w_ro, s_ro, r_ro, mesh, bridgefun)
        # Exit blindkid
    msloc_readout_attachright('KIDend0', kid.lcouple, d_kidQ_c, w_wide, s_wide, w_ro, s_ro, r_ro, mesh, bridgefun)
    ro_go(-1, dist2mark('readout_left')[0], w_ro, s_ro, bridgefun)
#==============================================================================
# Alignment pin holes    
#==============================================================================
    
    holes = [[4500, 4500],
             [4500, 15500],
             [15500, 15500],
             [15500, 4500]]
    sizeHoleFront = 1990.
    heightWafer = 375.
    tanThetaKOH = np.sqrt(2)
    sizeHoleBack = 2542 #Hard copy from Juan
#    sizeHoleBack = sizeHoleFront + 2*(heightWafer/tanThetaKOH)
    layername('SiNbackside')
    for hole in holes:
        gomark('chip00')
        go(*hole)
        layername('text')
        bar(1, sizeHoleFront, sizeHoleFront)
        layername('SiNbackside')
        bar(1, sizeHoleBack, sizeHoleBack)        
#==============================================================================
# v2: draw isolation around chip 
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
    layername('MSgnd')
    ldraw = (20e3, 20e3)
    wdraw = 50.
    drawBorders(ldraw, wdraw)    
#==============================================================================
#     outro
#==============================================================================
    outroScript(1)
    
    writeScript(filename)