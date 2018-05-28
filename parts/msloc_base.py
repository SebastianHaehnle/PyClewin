# -*- coding: utf-8 -*-
"""
Created on Wed Sep 07 17:49:52 2016

@author: sebastian
"""

from clepywin import *
import numpy as np
import scipy.constants as spc
import collections

def msloc_base_v06(layers, w_msl, w_sin, mesh):
    '''
    Old version for msloc1_v0.6 and msfb1_v0.6
    Wrong tunnel position
    '''    
    
    #    Chip size
    chip_lx = 42e3
    chip_ly = 14e3
    
#    antenna origin    
    origin_antenna = (7200,7000)
    #==============================================================================
    # write chip edge    
    #==============================================================================
    #    write in ?? layer
    layername('text')
    setmark('chip00')
    go(chip_lx, chip_ly)
    setmark('chipFF')
    gomark('chip00')
    go(*origin_antenna)
    setmark('antenna')
    gomark('chip00')
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
    go(chip_lx, 0)
    writecorner(1j)
    go(0, chip_ly)
    writecorner(-1)
    go(-chip_lx, 0)
    writecorner(-1j)
    
#    define coordinates where readout cpws end
    gomark('chip00') 
    go(41e3, 12.1e3)
    setmark('bondpadtop')
    gomark('chip00')    
    go(41e3, 1.9e3)
    setmark('bondpadbot')
    
#==============================================================================
#     define labyrinth layout
#==============================================================================    
    diagonal = True
    rturn = 0.5e3  
    # v06
    x_prelab = 2*(2181+1000)
    y_prelab = 2750 + 2*1000
#    x_prelab = 2*(2181+500)
#    y_prelab = 2250 + 2*500
    l_tunnel = 2e3
    l_safety = 1e3
    gomark('antenna')
    go(x_prelab, y_prelab)
    setmark('tunnelin')
    go(l_tunnel, 0)
    setmark('tunnelout')
    go(l_safety, 0)
    setmark('labyend')
    x45 = 1./np.sqrt(2)*rturn
    y45 = rturn - x45
#==============================================================================
#     Leaky antenna here
#==============================================================================    
    
    from .leaky_antenna import leaky_300to900
    xy_membrane = leaky_300to900(1, w_sin)   

#==============================================================================
#   Draw tunnel
#==============================================================================
    # Path to tunnel
    gomark('antennaOut')
    l_diag = np.sqrt(2)*(y_prelab-2*y45)
    x_diagmode2 = (x_prelab - 2*x45 - l_diag/np.sqrt(2))/2.
    x_diagmode1 = x_diagmode2 - x2m('antenna') # This takes care of transformer or other at antenna
    print 'labyrinth x-lengths: {:1.3f} mm, {:1.3f} mm'.format(x_diagmode1, x_diagmode2)
    push_away = True
    if push_away:
        x_diagmode1 = x_diagmode1 + x_diagmode2
        x_diagmode2 = 0
        print 'CHANGED labyrinth x-lengths: {:1.3f} mm, {:1.3f} mm'.format(x_diagmode1, x_diagmode2)
    layername('MSline')    
    if diagonal:
        # Do turn diagonally:
        msgo(1, x_diagmode1, w_msl, w_sin)
        ms45upgo(1, rturn, w_msl, mesh, w_sin)
        msgo(1+1j, l_diag, w_msl, w_sin)
        ms45downgo(1+1j, rturn, w_msl, mesh, w_sin)        
        msgo(1, x_diagmode2, w_msl, w_sin)
        ltot_laby = x_diagmode1 + x_diagmode2 + l_diag + rturn*np.pi/2.+l_tunnel+l_safety
        print 'labyrinth length : {:1.3f} mm'.format(ltot_laby)
    else:
        # 2*90deg turns (standard)
        wirego(1, x_prelab/2. - rturn, w_msl)
        turnupgo(1, rturn, w_msl, mesh)
        wirego(1j, y_prelab - 2*rturn, w_msl)
        turndowngo(1j, rturn, w_msl, mesh)
        wirego(1, x_prelab/2. - rturn, w_msl)
        ltot_laby = (x_prelab/2. - rturn)*2 + y_prelab - 2*rturn + rturn*np.pi + l_tunnel + l_safety
        print 'labyrinth length : {:1.3f} mm'.format(ltot_laby)
        
    # tunnel indicator
    msgo(1, l_tunnel, w_msl, w_sin)  # line through tunnel   
    msgo(1, l_safety, w_msl, w_sin) # distance from tunnel
 

    # do stuff...


#==============================================================================
#     write SiN Backside
#==============================================================================
    layername('SiNbackside')
    gomark('chip00')
    KOHangle = 54.7
    KOHangle *= spc.degree
    h_wafer = 350.
    cornerspace = 300
        
    # Trenches
    h_trenches = h_wafer * 0.35
    w_draw = h_trenches / np.tan(KOHangle) * 2
    print 'Trenchwidth:', w_draw
    print 'Trenchspacing:', cornerspace
    print 'Poly', makeWire(x2m('chipFF') - 2*cornerspace, w_draw)
#    go(cornerspace, 0)
#    wirego(1, x2m('chipFF') - cornerspace, w_draw)
#    go(cornerspace, cornerspace)
#    wirego(1j, y2m('chipFF') - cornerspace, w_draw)
#    go(-cornerspace, cornerspace)
#    wirego(-1, x2m('chip00') - cornerspace, w_draw)
#    go(-cornerspace, -cornerspace)
#    wirego(-1j, y2m('chip00') - cornerspace, w_draw)
#    xy_mem_back = msloc_membrane('SiNbackside', xy_membrane)
#==============================================================================
#     write tantalum
#==============================================================================
    from msloc_tantalum import msloc_tantalum_mesh
    msloc_tantalum_mesh('TantalumFront')
    msloc_tantalum_freespace_front(xy_membrane, 'TantalumFront', 'MSgnd')
    msloc_tantalum_mesh('TantalumBack')
    msloc_tantalum_freespace_back('TantalumBack')
#==============================================================================
# Some markers for the labyrinth : TODO: make actual layer for Tantalum and put in empty spaces
#==============================================================================
    layername('text')
    gomark('tunnelin')
    wirehollow(1, l_tunnel, 1e3, 1)    
    wire(1j, dist2mark('chipFF')[1], 1)
    wire(-1j, dist2mark('chip00')[1], 1)
    gomark('tunnelout')
    wire(1j, dist2mark('chipFF')[1], 1)
    wire(-1j, dist2mark('chip00')[1], 1)    
    gomark('labyend')


def msloc_base(layers, w_msl, w_sin, mesh, rotate_leaky):
    #    Chip size
    chip_lx = 42e3
    chip_ly = 14e3
    
#    antenna origin    
    origin_antenna = (7200,7000)
    #==============================================================================
    # write chip edge    
    #==============================================================================
    #    write in ?? layer
    layername('text')
    setmark('chip00')
    go(chip_lx, chip_ly)
    setmark('chipFF')
    gomark('chip00')
    go(*origin_antenna)
    setmark('antenna')
    gomark('chip00')
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
    go(chip_lx, 0)
    writecorner(1j)
    go(0, chip_ly)
    writecorner(-1)
    go(-chip_lx, 0)
    writecorner(-1j)
    
#    define coordinates where readout cpws end
    gomark('chip00') 
    go(41e3, 12.1e3)
    setmark('bondpadtop')
    gomark('chip00')    
    go(41e3, 1.9e3)
    setmark('bondpadbot')
    
#==============================================================================
#     define labyrinth layout
#==============================================================================    
    diagonal = True
    rturn = 0.5e3  
#    x_prelab = 2*(2181+1000)
#    y_prelab = 2750 + 2*1000
    x_prelab = 2*(2181+500)
    y_prelab = 2250 + 2*500
    l_tunnel = 4e3
    l_safety = 1e3
    gomark('antenna')
    go(x_prelab, y_prelab)
    setmark('tunnelin')
    go(l_tunnel, 0)
    setmark('tunnelout')
    go(l_safety, 0)
    setmark('labyend')
    x45 = 1./np.sqrt(2)*rturn
    y45 = rturn - x45
#==============================================================================
#     Leaky antenna here
#==============================================================================    
    
    from .leaky_antenna import leaky_300to900
    if rotate_leaky:
        xy_membrane = leaky_300to900(1j, w_sin)   
    else:
        xy_membrane = leaky_300to900(1, w_sin)
#==============================================================================
#   Draw tunnel
#==============================================================================
    # Path to tunnel
    gomark('antennaOut')
    
    if rotate_leaky:
        x_draw = x2m('tunnelin')
        y_draw = y2m('tunnelin')
        y_straight = xy_membrane[1]/2. - y2m('antenna')
        y_diag = y_draw - y_straight - rturn
        x_diag = y_diag
        l_diag = np.sqrt(2)*y_diag
        x_straight = x_draw - x_diag - rturn
        msgo(1j, y_straight, w_msl, w_sin)
        setmark('diaginit')
        ms45downgo(1j, rturn, w_msl, mesh, w_sin)
        msgo(1+1j, l_diag, w_msl, w_sin)
        ms45downgo(1+1j, rturn, w_msl, mesh, w_sin)
        setmark('diagoutoun')
        msgo(1, x_straight, w_msl, w_sin)
#        Non-diagonal
#        msgo(1j, y_draw - rturn, w_msl, w_sin)
#        msdowngo(1j, rturn, w_msl, mesh, w_sin)
#        msgo(1, x_draw - rturn, w_msl, w_sin)
        ltot_laby = x_straight + y_straight + l_diag + l_tunnel + l_safety + rturn*np.pi/2.
        print 'labyrinth length : {:1.3f} mm'.format(ltot_laby)
    else:
        l_diag = np.sqrt(2)*(y_prelab-2*y45)
        x_diagmode2 = (x_prelab - 2*x45 - l_diag/np.sqrt(2))/2.
        x_diagmode1 = x_diagmode2 - x2m('antenna') # This takes care of transformer or other at antenna
        print 'labyrinth x-lengths: {:1.3f} mm, {:1.3f} mm'.format(x_diagmode1, x_diagmode2)
        push_away = True
        if push_away:
            x_diagmode1 = x_diagmode1 + x_diagmode2
            x_diagmode2 = 0
            print 'CHANGED labyrinth x-lengths: {:1.3f} mm, {:1.3f} mm'.format(x_diagmode1, x_diagmode2)
        layername('MSline')    
        if diagonal:
            # Do turn diagonally:
            msgo(1, x_diagmode1, w_msl, w_sin)
            ms45upgo(1, rturn, w_msl, mesh, w_sin)
            msgo(1+1j, l_diag, w_msl, w_sin)
            ms45downgo(1+1j, rturn, w_msl, mesh, w_sin)        
            msgo(1, x_diagmode2, w_msl, w_sin)
            ltot_laby = x_diagmode1 + x_diagmode2 + l_diag + rturn*np.pi/2.+l_tunnel+l_safety
            print 'labyrinth length : {:1.3f} mm'.format(ltot_laby)
        else:
            # 2*90deg turns (standard)
            wirego(1, x_prelab/2. - rturn, w_msl)
            turnupgo(1, rturn, w_msl, mesh)
            wirego(1j, y_prelab - 2*rturn, w_msl)
            turndowngo(1j, rturn, w_msl, mesh)
            wirego(1, x_prelab/2. - rturn, w_msl)
            ltot_laby = (x_prelab/2. - rturn)*2 + y_prelab - 2*rturn + rturn*np.pi + l_tunnel + l_safety
            print 'labyrinth length : {:1.3f} mm'.format(ltot_laby)
        
    # tunnel indicator
    msgo(1, l_tunnel, w_msl, w_sin)  # line through tunnel   
    msgo(1, l_safety, w_msl, w_sin) # distance from tunnel
 

    # do stuff...


#==============================================================================
#     write SiN Backside
#==============================================================================
    layername('SiNbackside')
    gomark('chip00')
    KOHangle = 54.7
    KOHangle *= spc.degree
    h_wafer = 350.
    cornerspace = 300
        
    # Trenches
    h_trenches = h_wafer * 0.35
    w_draw = h_trenches / np.tan(KOHangle) * 2
    print 'Trenchwidth:', w_draw
    print 'Trenchspacing:', cornerspace
    print 'Poly', makeWire(x2m('chipFF') - 2*cornerspace, w_draw)

#==============================================================================
#     write tantalum
#==============================================================================
    from msloc_tantalum import msloc_tantalum_mesh
    msloc_tantalum_mesh('TantalumFront')
    if rotate_leaky:
        msloc_tantalum_freespace_front_rotate(xy_membrane, 'TantalumFront', 'MSgnd')
    else:
        msloc_tantalum_freespace_front(xy_membrane, 'TantalumFront', 'MSgnd')
    msloc_tantalum_mesh('TantalumBack')
    msloc_tantalum_freespace_back('TantalumBack')
#==============================================================================
# Some markers for the labyrinth : TODO: make actual layer for Tantalum and put in empty spaces
#==============================================================================
    layername('text')
    gomark('tunnelin')
    wirehollow(1, l_tunnel, 0.7e3, 1)    
    wire(1j, dist2mark('chipFF')[1], 1)
    wire(-1j, dist2mark('chip00')[1], 1)
    gomark('tunnelout')
    wire(1j, dist2mark('chipFF')[1], 1)
    wire(-1j, dist2mark('chip00')[1], 1)    
    gomark('labyend')
    
def msloc_base_v2(layers, w_msl, w_sin, mesh, rotate_leaky):
    #    Chip size
    chip_lx = 42e3
    chip_ly = 14e3
    
#    antenna origin    
    origin_antenna = (7200,7000)
    #==============================================================================
    # write chip edge    
    #==============================================================================
    #    write in ?? layer
    layername('text')
    setmark('chip00')
    go(chip_lx, chip_ly)
    setmark('chipFF')
    gomark('chip00')
    go(*origin_antenna)
    setmark('antenna')
    gomark('chip00')
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
    go(chip_lx, 0)
    writecorner(1j)
    go(0, chip_ly)
    writecorner(-1)
    go(-chip_lx, 0)
    writecorner(-1j)
    
#    define coordinates where readout cpws end
    gomark('chip00') 
    go(41e3, 12.1e3)
    setmark('bondpadtop')
    gomark('chip00')    
    go(41e3, 1.9e3)
    setmark('bondpadbot')
    
#==============================================================================
#     define labyrinth layout
#==============================================================================    
    diagonal = True
    rturn = 0.5e3  
#    x_prelab = 2*(2181+1000)
#    y_prelab = 2750 + 2*1000
    x_prelab = 2*(2181+500)
    y_prelab = 2250 + 2*500
    l_tunnel = 4e3
    l_safety = 1e3
    gomark('antenna')
    go(x_prelab, y_prelab)
    setmark('tunnelin')
    go(l_tunnel, 0)
    setmark('tunnelout')
    go(l_safety, 0)
    setmark('labyend')
    x45 = 1./np.sqrt(2)*rturn
    y45 = rturn - x45
#==============================================================================
#     Leaky antenna here
#==============================================================================    
    
    from .leaky_antenna import leaky_300to900_990um
    if rotate_leaky:
        xy_membrane = leaky_300to900_990um(1j, w_sin)   
    else:
        xy_membrane = leaky_300to900_990um(1, w_sin)
    xy_membrane = [3e3, 3e3]
#==============================================================================
#   Draw tunnel
#==============================================================================
    # Path to tunnel
    gomark('antennaOut')
    
    if rotate_leaky:
        x_draw = x2m('tunnelin')
        y_draw = y2m('tunnelin')
        y_straight = xy_membrane[1]/2. - y2m('antenna')
        y_diag = y_draw - y_straight - rturn
        x_diag = y_diag
        l_diag = np.sqrt(2)*y_diag
        x_straight = x_draw - x_diag - rturn
        msgo(1j, y_straight, w_msl, w_sin)
        setmark('diaginit')
        ms45downgo(1j, rturn, w_msl, mesh, w_sin)
        msgo(1+1j, l_diag, w_msl, w_sin)
        ms45downgo(1+1j, rturn, w_msl, mesh, w_sin)
        setmark('diagoutoun')
        msgo(1, x_straight, w_msl, w_sin)
#        Non-diagonal
#        msgo(1j, y_draw - rturn, w_msl, w_sin)
#        msdowngo(1j, rturn, w_msl, mesh, w_sin)
#        msgo(1, x_draw - rturn, w_msl, w_sin)
        ltot_laby = x_straight + y_straight + l_diag + l_tunnel + l_safety + rturn*np.pi/2.
        print 'labyrinth length : {:1.3f} mm'.format(ltot_laby)
    else:
        l_diag = np.sqrt(2)*(y_prelab-2*y45)
        x_diagmode2 = (x_prelab - 2*x45 - l_diag/np.sqrt(2))/2.
        x_diagmode1 = x_diagmode2 - x2m('antenna') # This takes care of transformer or other at antenna
        print 'labyrinth x-lengths: {:1.3f} mm, {:1.3f} mm'.format(x_diagmode1, x_diagmode2)
        push_away = True
        if push_away:
            x_diagmode1 = x_diagmode1 + x_diagmode2
            x_diagmode2 = 0
            print 'CHANGED labyrinth x-lengths: {:1.3f} mm, {:1.3f} mm'.format(x_diagmode1, x_diagmode2)
        layername('MSline')    
        if diagonal:
            # Do turn diagonally:
            msgo(1, x_diagmode1, w_msl, w_sin)
            ms45upgo(1, rturn, w_msl, mesh, w_sin)
            msgo(1+1j, l_diag, w_msl, w_sin)
            ms45downgo(1+1j, rturn, w_msl, mesh, w_sin)        
            msgo(1, x_diagmode2, w_msl, w_sin)
            ltot_laby = x_diagmode1 + x_diagmode2 + l_diag + rturn*np.pi/2.+l_tunnel+l_safety
            print 'labyrinth length : {:1.3f} mm'.format(ltot_laby)
        else:
            # 2*90deg turns (standard)
            wirego(1, x_prelab/2. - rturn, w_msl)
            turnupgo(1, rturn, w_msl, mesh)
            wirego(1j, y_prelab - 2*rturn, w_msl)
            turndowngo(1j, rturn, w_msl, mesh)
            wirego(1, x_prelab/2. - rturn, w_msl)
            ltot_laby = (x_prelab/2. - rturn)*2 + y_prelab - 2*rturn + rturn*np.pi + l_tunnel + l_safety
            print 'labyrinth length : {:1.3f} mm'.format(ltot_laby)
        
    # tunnel indicator
    msgo(1, l_tunnel, w_msl, w_sin)  # line through tunnel   
    msgo(1, l_safety, w_msl, w_sin) # distance from tunnel
 

    # do stuff...


#==============================================================================
#     write SiN Backside
#==============================================================================
    layername('SiNbackside')
    gomark('chip00')
    KOHangle = 54.7
    KOHangle *= spc.degree
    h_wafer = 350.
    cornerspace = 300
        
    # Trenches
    h_trenches = h_wafer * 0.35
    w_draw = h_trenches / np.tan(KOHangle) * 2
    print 'Trenchwidth:', w_draw
    print 'Trenchspacing:', cornerspace
    print 'Poly', makeWire(x2m('chipFF') - 2*cornerspace, w_draw)

#==============================================================================
#     write tantalum
#==============================================================================
    from msloc_tantalum import msloc_tantalum_mesh
    msloc_tantalum_mesh('TantalumFront')
    if rotate_leaky:
        msloc_tantalum_freespace_front_rotate_v2(xy_membrane, 'TantalumFront', 'MSgnd')
    else:
        msloc_tantalum_freespace_front(xy_membrane, 'TantalumFront', 'MSgnd')
    msloc_tantalum_mesh('TantalumBack')
    msloc_tantalum_freespace_back('TantalumBack')
#==============================================================================
# Some markers for the labyrinth : TODO: make actual layer for Tantalum and put in empty spaces
#==============================================================================
    layername('text')
    gomark('tunnelin')
    wirehollow(1, l_tunnel, 0.7e3, 1)    
    wire(1j, dist2mark('chipFF')[1], 1)
    wire(-1j, dist2mark('chip00')[1], 1)
    gomark('tunnelout')
    wire(1j, dist2mark('chipFF')[1], 1)
    wire(-1j, dist2mark('chip00')[1], 1)    
    gomark('labyend')

def msloc_tantalum_freespace_front(xy_mem, layerTa, layerNb, layerSiNdiel = 'SiNdiel'):
    edge_chip = 1.5e3    
    sin = 20 #overlap of SiN over NbTiN to ensure Ta-protection
#    edge_antenna = npa([5e3, 3e3])
#    xy_antenna = npa(xy_mem) + edge_antenna
    xy_antenna = npa([3e3, 3e3])
    # square around antenna --> I
    layername(layerTa)
    gomark('antenna')
    xy_antenna_Ta = xy_antenna + 2*sin
    print xy_antenna
    print xy_antenna_Ta
    bar(1, *xy_antenna_Ta)
    # diagonal around labyrinth --> II
    go(xy_antenna[0]/2., 0)
    setmark('temp')
    go(sin, 0)            
    xy_diag = npa(dist2mark('tunnelin'))
    print xy_diag
    tandiag = np.tan(np.pi/4.)
    poly_diag = npa([[0, xy_diag[0], xy_diag[0], xy_diag[0] - edge_chip/2., 0], [-xy_antenna_Ta[1] /2., xy_diag[1] - edge_chip/2., xy_diag[1] + edge_chip/2., xy_diag[1] + edge_chip/2., xy_antenna_Ta[1] /2.]])
    poly(poly_diag)
    # square around tunnel --> III
    gomark('tunnelin')
    wire(1, x2m('tunnelout'), edge_chip)    
    # square around filterbank --> IV
    gomark('chip00')
    go(x2m('tunnelout'), y2m('chipFF')/2.)
    wire(1, x2m('chipFF'), 2*(y2m('chipFF')))
    
    # Draw NbTiN gnd plane removal
    # start poly drawing at edge between antenna square and diagonal labyrinth --> I/II
    gomark('temp')
    xa = xy_antenna[0]
    ya = xy_antenna[1] /2.
    xd1 = xy_diag[0]
    yd1 = xy_diag[1] 
    dd = edge_chip/2.
    xd2 = x2m('tunnelout')
    yd2 = yd1
    xc = x2m('chip00')
    yc = y2m('chip00')
    layername(layerNb)    
    poly_nbtin = npa([[-xa, -ya], [0, -ya], [xd1, yd1-dd], [xd2, yd2-dd], [xd2, -yc], [-xc, -yc], [-xc, +yc], [xd2, yc], [xd2, yd2+dd], [xd1, yd1+dd], [xd1-dd, yd1+dd], [0, ya], [-xa, ya]]).transpose()
    poly_sin = npa([[-xa, -ya], [0, -ya], [xd1, yd1-dd], [xd2, yd2-dd], [xd2, -yc], [-xc, -yc], [-xc, +yc], [xd2, yc], [xd2, yd2+dd], [xd1, yd1+dd], [xd1-dd, yd1+dd], [0, ya], [-xa, ya]]).transpose()
    poly(poly_nbtin)
    layername(layerSiNdiel)
    poly(poly_sin)
    
def msloc_tantalum_freespace_front_rotate(xy_mem, layerTa, layerNb, layerSiNdiel = 'SiNdiel'):
    edge_chip = 1.5e3
    sin = 20
#    edge_antenna = npa([5e3, 3e3])
    xy_antenna = npa(xy_mem) 
#    xy_antenna = npa([3e3, 3e3])
    # square around antenna --> I
    layername(layerTa)
    gomark('antenna')
    print xy_antenna
    bar(1, *xy_antenna)
    # ward around diag ms line --> II    
    gomark('diaginit')
    poly_diag = [[-edge_chip, x2mSigned('diagoutoun') - edge_chip/2., x2mSigned('diagoutoun'), x2mSigned('diagoutoun'), edge_chip], [0, y2mSigned('diagoutoun')+edge_chip/2., y2mSigned('diagoutoun')+edge_chip/2., y2mSigned('diagoutoun')-edge_chip/2., 0]]
    poly(poly_diag)
    gomark('diagoutoun')
    wire(1, x2m('tunnelin'), edge_chip)
    # square around tunnel --> III
    gomark('tunnelin')
    wire(1, x2m('tunnelout'), edge_chip)    
    # square around filterbank --> IV
    gomark('chip00')
    go(x2m('tunnelout'), y2m('chipFF')/2.)
    wire(1, x2m('chipFF'), 2*(y2m('chipFF')))
    
    # Draw NbTiN gnd plane removal
    # start poly drawing at edge between antenna square and diagonal labyrinth --> I/II
#    gomark('temp')
    gomark('diaginit')
    xa = xy_antenna[0] /2.
    ya = xy_antenna[1] 
    dd = edge_chip/2.
    xd1 = x2mSigned('diagoutoun')
    yd1 = y2mSigned('diagoutoun')
    xd2 = x2mSigned('tunnelout')
    yd2 = yd1
    xc = x2mSigned('chip00')
    yclow = y2mSigned('chip00')
    yctop = y2mSigned('chipFF')
    poly_nbtin = npa([[-xa, 0], [xd1-dd, yd1+dd], [xd1, yd1+dd], [xd2, yd2+dd], [xd2, yctop], [xc, yctop], [xc, yclow], [xd2, yclow], [xd2, yd2-dd], [xd1, yd1-dd], [xa, 0], [xa, -ya], [-xa, -ya]]).transpose()
    poly_sin = npa([[-xa+sin, -sin], [xd1-dd+sin, yd1+dd-sin], [xd1, yd1+dd-sin], [xd2+sin, yd2+dd-sin], [xd2+sin, yctop], [xc, yctop], [xc, yclow], [xd2+sin, yclow], [xd2+sin, yd2-dd+sin], [xd1-sin, yd1-dd+sin], [xa-sin, 0], [xa-sin, -ya+sin], [-xa+sin, -ya+sin]]).transpose()
    layername(layerNb)
    poly(poly_nbtin)
    layername(layerSiNdiel)
    poly(poly_sin)  
    
def msloc_tantalum_freespace_front_rotate_v2(xy_mem, layerTa, layerNb, layerSiNdiel = 'SiNdiel'):
    edge_chip = 1.5e3
    sin = 20
#    edge_antenna = npa([5e3, 3e3])
    xy_antenna = npa(xy_mem) 
#    xy_antenna = npa([3e3, 3e3])
    # square around antenna --> I
    layername(layerTa)
    gomark('antenna')
    print xy_antenna
    bar(1, *xy_antenna)
    # ward around diag ms line --> II    
    gomark('diaginit')
    poly_diag = [[-edge_chip, x2mSigned('diagoutoun') - edge_chip/2., x2mSigned('diagoutoun'), x2mSigned('diagoutoun'), edge_chip], [0, y2mSigned('diagoutoun')+edge_chip/2., y2mSigned('diagoutoun')+edge_chip/2., y2mSigned('diagoutoun')-edge_chip/2., 0]]
    poly(poly_diag)
    gomark('diagoutoun')
    wire(1, x2m('tunnelin'), edge_chip)
    # square around tunnel --> III
    gomark('tunnelin')
    wire(1, x2m('tunnelout'), edge_chip)    
    # square around filterbank --> IV
    gomark('chip00')
    go(x2m('tunnelout'), y2m('chipFF')/2.)
    wire(1, x2m('chipFF'), 2*(y2m('chipFF')))
    
    # Draw NbTiN gnd plane removal
    # start poly drawing at edge between antenna square and diagonal labyrinth --> I/II
#    gomark('temp')
    gomark('diaginit')
    xa = xy_antenna[0] /2.
    ya = xy_antenna[1] 
    dd = edge_chip/2.
    xd1 = x2mSigned('diagoutoun')
    yd1 = y2mSigned('diagoutoun')
    xd2 = x2mSigned('tunnelout')
    yd2 = yd1
    xc = x2mSigned('chip00')
    yclow = y2mSigned('chip00')
    yctop = y2mSigned('chipFF')
    poly_nbtin = npa([[-xa, 0], [xd1-dd, yd1+dd], [xd1, yd1+dd], [xd2, yd2+dd], [xd2, yctop], [xc, yctop], [xc, yclow], [xd2, yclow], [xd2, yd2-dd], [xd1, yd1-dd], [xa, 0], [xa, -ya], [-xa, -ya]]).transpose()
    poly_sin = npa([[-xa+sin, -sin], [xd1-dd+sin, yd1+dd-sin], [xd1, yd1+dd-sin], [xd2+sin, yd2+dd-sin], [xd2+sin, yctop], [xc, yctop], [xc, yclow], [xd2+sin, yclow], [xd2+sin, yd2-dd+sin], [xd1-sin, yd1-dd+sin], [xa-sin, 0], [xa-sin, -ya+sin], [-xa+sin, -ya+sin]]).transpose()
    layername(layerNb)
    poly(poly_sin) # v2 change: add distance between nbtin and Ta so they dont touch
    layername(layerSiNdiel)
    poly(poly_sin)       
    
    
def msloc_tantalum_freespace_back(layer):
    '''
    Membrane is done in antenna function
    Input:
        layername for tantalum backside
        xy lengths for membrane (on backside) -> result of msloc_base_backside
    '''
    edge_chip = 1e3
    layername(layer)
#    gomark('antenna')
#    bar(1, *xy_mem)
    gomark('bondpadtop')
    wire(1, x2m('chipFF'), 2*edge_chip)
    gomark('bondpadbot')
    wire(1, x2m('chipFF'), 2*edge_chip)

def msloc_membrane(layer, xy_mem):
    '''
    Input:
        layername for SiN backside
        xy lengths for membrane (on frontside)
    '''
    layername(layer)
    gomark('chip00')
    KOHangle = 54.7
    KOHangle *= spc.degree
    h_wafer = 350.
    cornerspace = 300
        
#    # Trenches
#    h_trenches = h_wafer * 0.35
#    w_draw = h_trenches / np.tan(KOHangle) * 2
#    go(cornerspace, 0)
#    wirego(1, x2m('chipFF') - cornerspace, w_draw)
#    go(cornerspace, cornerspace)
#    wirego(1j, y2m('chipFF') - cornerspace, w_draw)
#    go(-cornerspace, cornerspace)
#    wirego(-1, x2m('chip00') - cornerspace, w_draw)
#    go(-cornerspace, -cornerspace)
#    wirego(-1j, y2m('chip00') - cornerspace, w_draw)
    
    # Membrane
    h_mem = h_wafer
    add_mem = h_mem / np.tan(KOHangle) * 2
    x_mem = xy_mem[0] + add_mem
    y_mem = xy_mem[1] + add_mem
    print x_mem, y_mem
    gomark('antenna')
    bar(1, x_mem, y_mem)
    return [x_mem, y_mem]
    
if __name__ == '__main__':
    pass