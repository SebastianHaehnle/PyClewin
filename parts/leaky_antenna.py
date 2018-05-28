# -*- coding: utf-8 -*-
"""
Created on Tue Oct 04 17:17:02 2016

@author: sebastian
"""

from clepywin import *

import numpy as np
import scipy.constants as spc

def leaky_300to900(direction, wsin, layer0 = 'MSgnd', layer1 = 'MSline', layer2 = 'SiNdiel', layer3 = 'SiNwafer', layer4 = 'SiNbackside', layer5 = 'TantalumBack', directkid = False):
    gomark('antenna')

    #rotate cosy to direction

    # Microstrip geometry at antenna
    w_msl_ant = 1.65 + manVars.nbtinLine
    # Microstrip geometry for matching transformer
    if directkid:
        w_msl_trans = 1.9 + manVars.nbtinLine
        l_msl_trans = 0.
    else:
        w_msl_trans = 1.55 + manVars.nbtinLine    
        l_msl_trans = 28    
        
    # general geometry from Ozans pdf
    w_total = 2778.
    h_total = 791.
    # Define drawing parameters
    # Membrane size, used also to determine backside pattern
    y_memb_nominal = 3e3    
    x_memb_nominal = 3e3 
    # margin for frontside SiN, only for directkid
    margin_memb_long = 8e3    
    margin_memb_short = 3e3
    long_memb = y_memb_nominal + margin_memb_long# values used for drawing
    short_memb = x_memb_nominal + margin_memb_short
    if not directkid:
        memb_poly = [[x2mSigned('chip00'), x2mSigned('chip00'), x2mSigned('tunnelout'), x2mSigned('tunnelout')], [y2mSigned('chip00'), y2mSigned('chipFF'), y2mSigned('chipFF'), y2mSigned('chip00')]]
    else:
        memb_poly = np.array([[-long_memb, -long_memb, long_memb, long_memb], [-short_memb, long_memb, long_memb, -short_memb]])/2.
    # inner slot
    y_slot = 3.
    x_slot = 2.
    # tapered slot
    l_taper = (w_total - y_slot)/2.
    x_taper = h_total
    
    # short layout
    lpre = 2.
    wshort = w_msl_ant
    
#==============================================================================
# Start drawing sstuff    
#==============================================================================
    gomark('antenna')
    rot(direction)
    setmark('rotated')   
    # DRAW MEMBRANE (Front SiN)
    layername(layer3)
    gomark('antenna')
    poly(memb_poly)
    gomark('rotated')
    # DRAW GND PLANE antenna slot
    layername(layer0)
    bar(1, x_slot, y_slot)
    go(0, y_slot/2.)
    broaden(1j, l_taper, x_slot, x_taper)
    go(0, - y_slot)
    broaden(-1j, l_taper, x_slot, x_taper)
#  DRAW MS SHORT      
    gomark('rotated')
    go(x_slot/2., 0)
    msgo(-1, x_slot, w_msl_ant, wsin)
    from msloc_kid_v1 import short_msl
    short_msl(-1, w_msl_ant, wsin, wshort = wshort, lpre = lpre)
#   Draw impedance transformer    
    gomark('rotated')
    go(x_slot/2., 0)
    msgo(1, l_msl_trans, w_msl_trans, wsin)
    rot(np.conjugate(direction))
    setmark('antennaOut')
    rot(direction)
#   Values for backside SiN for membrane
    gomark('chip00')
    KOHangle = 54.7
    KOHangle *= spc.degree
    h_wafer = 350.
        
#  Draw Membrane
    h_mem = h_wafer
    add_mem = h_mem / np.tan(KOHangle) * 2
    x_mem = x_memb_nominal + add_mem
    y_mem = y_memb_nominal + add_mem   
    gomark('rotated')
    layername(layer4)
    bar(1, x_mem, y_mem)
#   Draw backside Ta for membrane
    layername(layer5)
    bar(1, x_mem + 50, y_mem + 50)
    rot(np.conjugate(direction))
    
    return [x_memb_nominal, y_memb_nominal]
    
def leaky_300to900_directhybrid(direction, kid, whyb, shyb, wwide, swide, wsin, layer0 = 'MSgnd', layer1 = 'MSline', layer2 = 'SiNdiel', layer3 = 'SiNwafer', layer4 = 'SiNbackside', layer5 = 'TantalumBack', layer6 = 'Hybrids'):
    # Line geometry
    w_line_ant = 2.0 + manVars.alLine
    s_line_ant = 2.4 + (manVars.nbtinSlot - manVars.alLine)/2.
    l_ant = 0
    l_short = 7
     #KID parameters
    lhybrid = kid.lal*1e6
    lwide = kid.lwide*1e6   

    gomark('antenna')
        # general geometry from Ozans pdf
    w_total = 2778.
    h_total = 791.
    # Define drawing parameters
    # Membrane size, used also to determine backside pattern
    y_memb_nominal = 3e3    
    x_memb_nominal = 3e3    
    margin_memb_long = 8e3    
    margin_memb_short = 0.5e3
    long_memb = y_memb_nominal + margin_memb_long # values used for drawing
    short_memb = x_memb_nominal + margin_memb_short
    memb_poly = np.array([[-long_memb, -long_memb, short_memb, short_memb], [-long_memb, long_memb, long_memb, -long_memb]])/2.
    # inner slot
    y_slot = 3.
    x_slot = 2.
    # tapered slot
    l_taper = (w_total - y_slot)/2.
    x_taper = h_total
    

    
    #   length of line on gnd plane
#    define tapers and all that jazz
    taper_l_almsl = 12. # length of taper
    taper_l_alwide = 21. #length of taper
    wsin_waf = 2*wsin 
    l_siwaf = 21.
    # short layout
    
    gomark('antenna')
    #rotate cosy to direction
    rot(direction)
    setmark('temp')
    # DRAW MEMBRANE
    layername(layer3)
    poly(memb_poly)
    # DRAW GND PLANE
    layername(layer0)
    bar(1, x_slot, y_slot)

    gomark('temp')
    go(0, y_slot/2.)
    broaden(1, l_taper, x_slot, x_taper)
    go(0, - y_slot)
    broaden(-1, l_taper, x_slot, x_taper)
    #   Draw backside SiN for membrane
    layername(layer4)
    gomark('chip00')
    KOHangle = 54.7
    KOHangle *= spc.degree
    h_wafer = 350.
        
    # Membrane
    h_mem = h_wafer
    add_mem = h_mem / np.tan(KOHangle) * 2
    x_mem = x_memb_nominal + add_mem
    y_mem = y_memb_nominal + add_mem
    gomark('temp')
    bar(1, x_mem, y_mem)
    #   Draw backside Ta for membrane
    layername(layer5)
    bar(1, x_mem+50, y_mem+50)
    
    
    #KID
    gomark('temp')
    go(x_slot/2., 0)
    layername(layer6)
    wire(-1, l_short, w_line_ant)
    wire(1, l_ant, w_line_ant)
    layername(layer0)
    wirego(1, l_ant, w_line_ant + 2*s_line_ant)
    layername(layer6)
    setmark('antennaout')
    wire(1, lhybrid, whyb)
    layername(layer0)
    wirego(1, lhybrid, whyb + 2*shyb)
    from msloc_kid_v1 import transition_hybwide
    rot(1j)
    transition_hybwide(whyb, shyb, wwide, swide, taper_l_alwide)
    rot(-1j)    
    
    layername('MSgnd')
    cpwgo(1, l_siwaf, wwide, swide)
#    Draw SiNwafer part
    layername('SiNwafer')
    wire(-1, x2m('antennaout') + l_siwaf + wsin_waf/2., wsin_waf)        
    layername('MSgnd')
    cpwgo(1, lwide - l_siwaf, wwide, swide)    
    wirego(1, swide, wwide + 2*swide)        
    layername('SiNwafer')
    setmark('temp')
    go(0, long_memb/4. + 0.5e3)
    wire(-1, x2m('antennaout'), long_memb/2. -1e3)    
    go(0, -2*(long_memb/4. + 0.5e3))
    wire(-1, x2m('antennaout'), long_memb/2. -1e3)
    gomark('temp')
    rot(np.conjugate(direction))
    
    setmark('KIDend0')
    
    
def leaky_300to900_990um(direction, wsin, layer0 = 'MSgnd', layer1 = 'MSline', layer2 = 'SiNdiel', layer3 = 'SiNwafer', layer4 = 'SiNbackside', layer5 = 'TantalumBack', directkid = False):
    gomark('antenna')

    #rotate cosy to direction

    # Microstrip geometry at antenna
    w_msl_ant = 1.65 + manVars.nbtinLine
    # Microstrip geometry for matching transformer
    if directkid:
        w_msl_trans = 1.9 + manVars.nbtinLine
        l_msl_trans = 0.
    else:
        w_msl_trans = 1.55 + manVars.nbtinLine    
        l_msl_trans = 28    
        
    # general geometry from Ozans pdf
    w_total = 990 #2778./3
    h_total = 282.5      #791.*990./2778. # just shorter than the long version, no change in taper
    # Define drawing parameters
    # Membrane size, used also to determine backside pattern
    y_memb_nominal = 1.2e3 #smaller
    x_memb_nominal = 1.2e3 #smaller
    # margin for frontside SiN, only for directkid
    margin_memb_long = 8e3    
    margin_memb_short = 3e3
    long_memb = y_memb_nominal + margin_memb_long# values used for drawing
    short_memb = x_memb_nominal + margin_memb_short
    if not directkid:
        memb_poly = [[x2mSigned('chip00'), x2mSigned('chip00'), x2mSigned('tunnelout'), x2mSigned('tunnelout')], [y2mSigned('chip00'), y2mSigned('chipFF'), y2mSigned('chipFF'), y2mSigned('chip00')]]
    else:
        memb_poly = np.array([[-long_memb, -long_memb, long_memb, long_memb], [-short_memb, long_memb, long_memb, -short_memb]])/2.
    # inner slot
    y_slot = 3.
    x_slot = 2.
    # tapered slot
    l_taper = (w_total - y_slot)/2.
    x_taper = h_total
    
    # short layout
    lpre = 2.
    wshort = w_msl_ant
    
#==============================================================================
# Start drawing sstuff    
#==============================================================================
    gomark('antenna')
    rot(direction)
    setmark('rotated')   
    # DRAW MEMBRANE (Front SiN)
    layername(layer3)
    gomark('antenna')
    poly(memb_poly)
    gomark('rotated')
    # DRAW GND PLANE antenna slot
    layername(layer0)
    bar(1, x_slot, y_slot)
    go(0, y_slot/2.)
    broaden(1j, l_taper, x_slot, x_taper)
    go(0, - y_slot)
    broaden(-1j, l_taper, x_slot, x_taper)
#  DRAW MS SHORT      
    gomark('rotated')
    go(x_slot/2., 0)
    msgo(-1, x_slot, w_msl_ant, wsin)
    from msloc_kid_v1 import short_msl
    short_msl(-1, w_msl_ant, wsin, wshort = wshort, lpre = lpre)
#   Draw impedance transformer    
    gomark('rotated')
    go(x_slot/2., 0)
    msgo(1, l_msl_trans, w_msl_trans, wsin)
    rot(np.conjugate(direction))
    setmark('antennaOut')
    rot(direction)
#   Values for backside SiN for membrane
    gomark('chip00')
    KOHangle = 54.7
    KOHangle *= spc.degree
    h_wafer = 350.
        
#  Draw Membrane
    h_mem = h_wafer
    add_mem = h_mem / np.tan(KOHangle) * 2
    x_mem = x_memb_nominal + add_mem
    y_mem = y_memb_nominal + add_mem   
    gomark('rotated')
    layername(layer4)
    bar(1, x_mem, y_mem)
#   Draw backside Ta for membrane
    layername(layer5)
    Tasize = 3e3 + 2*KOHetchWidth(h_wafer)
    bar(1, Tasize + 50, Tasize + 50)
    rot(np.conjugate(direction))
    layername('text')
    bar(1, x_memb_nominal, y_memb_nominal)
    
    return [x_memb_nominal, y_memb_nominal]

def leaky_300to900_990um_directhybrid(direction, kid, whyb, shyb, wwide, swide, wsin, layer0 = 'MSgnd', layer1 = 'MSline', layer2 = 'SiNdiel', layer3 = 'SiNwafer', layer4 = 'SiNbackside', layer5 = 'TantalumBack', layer6 = 'Hybrids'):
    # Line geometry
    w_line_ant = 2.0 + manVars.alLine
    s_line_ant = 2.4 + (manVars.nbtinSlot - manVars.alLine)/2.
    l_ant = 0
    l_short = 7
     #KID parameters
    lhybrid = kid.lal*1e6
    lwide = kid.lwide*1e6   

    gomark('antenna')
        # general geometry from Ozans pdf
    w_total = 990 #2778./3
    h_total = 282.5      #791.*990./2778. # just shorter than the long version, no change in taper
    # Define drawing parameters
    # Membrane size, used also to determine backside pattern
    y_memb_nominal = 1.2e3 #smaller
    x_memb_nominal = 1.2e3 #smaller 
    margin_memb_long = 8e3    
    margin_memb_short = 0.5e3
    long_memb = y_memb_nominal + margin_memb_long # values used for drawing
    short_memb = x_memb_nominal + margin_memb_short
    memb_poly = np.array([[-long_memb, -long_memb, short_memb, short_memb], [-long_memb, long_memb, long_memb, -long_memb]])/2.
    # inner slot
    y_slot = 3.
    x_slot = 2.
    # tapered slot
    l_taper = (w_total - y_slot)/2.
    x_taper = h_total
    

    
    #   length of line on gnd plane
#    define tapers and all that jazz
    taper_l_almsl = 12. # length of taper
    taper_l_alwide = 21. #length of taper
    wsin_waf = 2*wsin 
    l_siwaf = 21.
    # short layout
    
    gomark('antenna')
    #rotate cosy to direction
    rot(direction)
    setmark('temp')
    # DRAW MEMBRANE
    layername(layer3)
    poly(memb_poly)
    # DRAW GND PLANE
    layername(layer0)
    bar(1j, y_slot, x_slot)

    gomark('temp')
    go(0, y_slot/2.)
    broaden(1j, l_taper, x_slot, x_taper)
    go(0, - y_slot)
    broaden(-1j, l_taper, x_slot, x_taper)
    #   Draw backside SiN for membrane
    layername(layer4)
    gomark('chip00')
    KOHangle = 54.7
    KOHangle *= spc.degree
    h_wafer = 350.
        
    # Membrane
    h_mem = h_wafer
    add_mem = h_mem / np.tan(KOHangle) * 2
    x_mem = x_memb_nominal + add_mem
    y_mem = y_memb_nominal + add_mem
    gomark('temp')
    bar(1, x_mem, y_mem)
    #   Draw backside Ta for membrane
    Tasize = 3e3 + 2*KOHetchWidth(h_wafer)
    layername(layer5)
    bar(1, Tasize + 50, Tasize + 50)
    layername('text')
    bar(1, x_memb_nominal, y_memb_nominal)
    
#    rot(np.conjugate(direction))
    
    #KID
    gomark('temp')
    go(x_slot/2., 0)
    layername(layer6)
    wire(-1, l_short, w_line_ant)
    wire(1, l_ant, w_line_ant)
    layername(layer0)
    wirego(1, l_ant, w_line_ant + 2*s_line_ant)
    layername(layer6)
    setmark('antennaout')
    wire(1, lhybrid, whyb)
    layername(layer0)
    wirego(1, lhybrid, whyb + 2*shyb)
    from msloc_kid_v1 import transition_hybwide
    rot(1j)
    transition_hybwide(whyb, shyb, wwide, swide, taper_l_alwide)
    rot(-1j)    
    
    layername('MSgnd')
    cpwgo(1, l_siwaf, wwide, swide)
#    Draw SiNwafer part
    layername('SiNwafer')
    wire(-1, x2m('antennaout') + l_siwaf + wsin_waf/2., wsin_waf)        
    layername('MSgnd')
    cpwgo(1, lwide - l_siwaf, wwide, swide)    
    wirego(1, swide, wwide + 2*swide)        
    layername('SiNwafer')
    setmark('temp')
    go(0, long_memb/4. + 0.5e3)
    wire(-1, x2m('antennaout'), long_memb/2. -1e3)    
    go(0, -2*(long_memb/4. + 0.5e3))
    wire(-1, x2m('antennaout'), long_memb/2. -1e3)
    gomark('temp')
    rot(np.conjugate(direction))
    
    setmark('KIDend0')
