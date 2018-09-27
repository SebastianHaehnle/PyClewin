# -*- coding: utf-8 -*-
"""
Created on Mon Jan 09 16:56:47 2017

@author: sebastian
"""

from PyClewin import *
from PyClewin.base import *
import numpy as np
import scipy.constants as spc


def Deshima42x14(layers, chipname = ''):
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
    # Write chipname
    layername('Aluminum')
    if chipname != '':
        go(1e3, 1e3)
        base.text(1, chipname, 500)
    gomark('chip00')
    layername('text')

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
#
    # define coordinates where readout cpws end
    gomark('chip00')
    go(41e3, 12.1e3)
    setmark('bondpadtop')
    gomark('chip00')
    go(41e3, 1.9e3)
    setmark('bondpadbot')

    # Define tunnel position
    gomark('chip00')
    go(12560, 9900)
    setmark('tunnelin')
    layername('text')
    wirehollow(1, 4e3, 0.7e3, 1)
    wire(1j, dist2mark('chipFF')[1], 1)
    wire(-1j, dist2mark('chip00')[1], 1)
    go(4000, 0)
    setmark('tunnelout')
    wire(1j, dist2mark('chipFF')[1], 1)
    wire(-1j, dist2mark('chip00')[1], 1)



def Mosaic42x14_leaky(layers, mainline, rotate_leaky):
    """
    DEPRECATED, DO NOT USE
    """
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
        xy_membrane = leaky_300to900(1j, mainline.line)
    else:
        xy_membrane = leaky_300to900(1, mainline.line)
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

#        msgo(1j, y_straight, w_msl, w_sin)
        mainline.wirego(1j, y_straight)
        setmark('diaginit')
#        ms45downgo(1j, rturn, w_msl, mesh, w_sin)
        mainline.down45go(1j, rturn)
#        msgo(1+1j, l_diag, w_msl, w_sin)
        mainline.wirego(1+1j, l_diag)
#        ms45downgo(1+1j, rturn, w_msl, mesh, w_sin)
        mainline.down45go(1+1j, rturn)
        setmark('diagoutoun')
#        msgo(1, x_straight, w_msl, w_sin)
        mainline.wirego(1, x_straight)
#        Non-diagonal
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
        # Do turn diagonally:
#            msgo(1, x_diagmode1, w_msl, w_sin)
#            ms45upgo(1, rturn, w_msl, mesh, w_sin)
#            msgo(1+1j, l_diag, w_msl, w_sin)
#            ms45downgo(1+1j, rturn, w_msl, mesh, w_sin)
#            msgo(1, x_diagmode2, w_msl, w_sin)
        mainline.wirego(1, x_diagmode1)
        mainline.up45go(1, rturn)
        mainline.wirego(1+1j, l_diag)
        mainline.down45go(1+1j, rturn)
        mainline.wirego(1, x_diagmode2)
        ltot_laby = x_diagmode1 + x_diagmode2 + l_diag + rturn*np.pi/2.+l_tunnel+l_safety
        print 'labyrinth length : {:1.3f} mm'.format(ltot_laby)

    # tunnel indicator
#    msgo(1, l_tunnel, w_msl, w_sin)  # line through tunnel
#    msgo(1, l_safety, w_msl, w_sin) # distance from tunnel
    mainline.wirego(1, l_tunnel)
    mainline.wirego(1, l_safety)


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
    from msloc_base import msloc_tantalum_freespace_front_rotate, msloc_tantalum_freespace_front, msloc_tantalum_freespace_back
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

def testchip20x20(layers):
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
    return (lx_chip, ly_chip)

def testchip20x20_small(layers):
    lx_chip = 19.9e3
    ly_chip = 19.9e3
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
    return (lx_chip, ly_chip)

#del b
#del base