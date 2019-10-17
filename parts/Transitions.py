# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 14:15:43 2017

@author: sebastian
"""

from PyClewin import *

import numpy as np

def transMSHybridM4000(direction, ms, hybrid, **kwargs):
    '''
    Microstrip to Hybrid transition where the MS line drops down from the dielectric and the Aluminum of the hybrid creates a galvanic connection on top. The MS gnd continues after a taper as the CPW gnd
    '''
    ltaper = 5.
    ldiel = 3.
    lmsonly = 2.
    loverlap = 7.
    woverlap = 2.

    rot(direction)
    # Draw continuing GND plane
    setmark('transitionlevel')
    layername(hybrid.gndlayer)
    broadengo(1, ltaper, ms.line, hybrid.wTotal)
    wire(1, loverlap, hybrid.wTotal)
    # Draw MS line
    gomark('transitionlevel')
    layername(ms.linelayer)
    broadengo(1, ldiel + lmsonly, ms.line, woverlap)
    wire(1, loverlap, woverlap)
    gomark('transitionlevel')
    # Draw Dielectric
    layername(ms.diellayer)
    wirego(1, ldiel, ms.dielwidth)
    go(lmsonly, 0)
    # Draw Aluminum
    layername(hybrid.linelayer)
    wirego(1, loverlap, woverlap)
    rotback()

def transMSWideM4000(direction, ms, wide, **kwargs):
    ltrans = 21.
    ldiel = 4.
    lmsonly = 3.
    loverlap = 7.

    rot(direction)
    setmark('transitionlevel')
    layername(ms.linelayer)
    wire(1, ldiel + lmsonly + loverlap, ms.line)
    layername(ms.diellayer)
    wire(1, ldiel, ms.dielwidth)
    layername(wide.gndlayer)
    broaden(1, ldiel + lmsonly, ms.line, wide.line/2.)
    cpwbroadengo(1, ltrans, 0, ms.line, wide.line, wide.gap)
    rotback()


def transHybridWideM4000(direction, hybrid, wide, invert = False, **kwargs):
    ltrans = kwargs.pop('ltrans', 21)
    if not invert:
        rot(direction)
        layername(hybrid.linelayer)
        wire(1, 2/3.*ltrans, hybrid.line)
        layername(hybrid.gndlayer)
        broaden(1, 1/3.*ltrans, hybrid.line, wide.line/2.)
        cpwbroadengo(1, ltrans, 0, hybrid.gap+hybrid.line/2., wide.line, wide.gap)
        rotback()
    else:
        layername(hybrid.gndlayer)
        cpwbroadengo(direction, ltrans, wide.line, wide.gap, 0, hybrid.gap+hybrid.line/2.)
        broaden(-direction, 1/3.*ltrans, hybrid.line, wide.line/2.)
        layername(hybrid.linelayer)
        wire(-direction, 2/3.*ltrans, hybrid.line)

def transTHzHybrid(direction, line_thz, line_hybrid, invert = False):
    """
    Values from Nuri_FP_v2.4.cif, Mask for D1006
    """
    # Shape definitions
    l_taper1 = 3
    l_wide = 3
    s_wide = 4.8
    w_wide = 3.0
    l_taper2 = 3.3
    l_overlap = 3

    # Drawing
    if not invert:
        rot(direction)
    
        line_thz.tapergo(1, l_taper1, w_wide, s_wide) # taper
        base.cpwgo(1, l_wide, w_wide, s_wide) # wide part
        base.broaden(1, l_taper2, w_wide + 2*s_wide, line_hybrid.wTotal) # reverse taper
        layername(line_hybrid.linelayer) # aluminum layer
        base.wire(-1, l_overlap, line_hybrid.line) # draw aluminum line overlap
    
        rot(np.conjugate(direction))
    else:
        layername(line_hybrid.linelayer) # aluminum layer
        base.wire(direction, l_overlap, line_hybrid.line) # draw aluminum line overlap
        layername(line_hybrid.gndlayer) # aluminum layer
        base.broaden(-direction, l_taper2, w_wide + 2*s_wide, line_hybrid.wTotal) # reverse taper
        base.cpwgo(direction, l_wide, w_wide, s_wide) # wide part
        base.movedirection(direction, l_taper1)
        line_thz.taper(-direction, l_taper1, w_wide, s_wide) # taper
        
    return direction


def transElbowcouplerCurved(direction_out, line_wide, line_coupler, **kwargs):
    direction_in = kwargs.pop('direction_in', 1)
    # Check how long taper of cpw should be, depending on tapering angle
    angle = kwargs.pop('angle', np.pi/6.)
    l1 = np.tan(angle)*np.abs(line_wide.line - line_coupler.line)
    l2 = np.tan(angle)*np.abs(line_wide.wTotal - line_coupler.wTotal)
    # Taper from wide section to coupler section, if necessary
    if np.isclose(l1, 0) and np.isclose(l1, 0):
        pass
    else:
        print l1, l2
        l_taper = max(l1, l2)
        rot(direction_in)
        layername(line_wide.gndlayer)
        line_wide.tapergo(direction_in, l_taper, line_coupler.line, line_coupler.gap)
    # Draw curve depending on output direction, currently only supports direction_in == 1
    if (direction_in == 1 and direction_out == 1j):
        line_coupler.upgo(direction_in)
    else:
        line_coupler.downgo(direction_in)
    rot(np.conjugate(direction_in))

def coupler_Fabryperot(direction, side, cpw_thz, cpw_fp, param_1, param_2):
    """
    side == 'fp' or 'thz' # selects which side of the coupler the starting position is located
    param_1 and param_2 correspond to p1 and p2 in Nuris coupler in the sonnet file, with p2 being the driving factor to change Qc
    param_1 == length of broad coupler part
    param_2 == starting distance of fp_line from end of taper
    """
    l_taper = np.sqrt(3)*(1.5*cpw_fp.line + 1)
    w_taper = 3*cpw_fp.line + 2*2
    s_taper = cpw_thz.gap

    rot(direction)

    if side == 'thz':
        cpw_thz.tapergo(direction, l_taper, w_taper, s_taper)
        try:
            layername(cpw_thz.gndlayer)
        except:
            pass
        base.cpw(direction, param_1, w_taper, s_taper)
        go(param_2, 0)
    elif side == 'fp':
        go(param_2 + l_taper, 0)
        cpw_thz.tapergo(-direction, l_taper, w_taper, s_taper)
        try:
            layername(cpw_thz.gndlayer)
        except:
            pass
        base.cpw(-direction, param_1, w_taper, s_taper)
        go(l_taper, 0)
    else:
        print 'WARNING: INVALID SIDE'
    rot(np.conjugate(direction))
    return direction

def coupler_Fabryperot_covered(direction, side, cpw_thz, cpw_fp, param_1, param_2, cover_length):
    """
    side == 'fp' or 'thz' # selects which side of the coupler the starting position is located
    param_1 and param_2 correspond to p1 and p2 in Nuris coupler in the sonnet file, with p2 being the driving factor to change Qc
    param_1 == length of broad coupler part
    param_2 == starting distance of fp_line from end of taper
    """
    l_taper = np.sqrt(3)*(1.5*cpw_fp.line + 1)
    w_taper = 3*cpw_fp.line + 2*2
    s_taper = cpw_thz.gap
    l1 = cover_length
    l2 = cpw_fp.coverextension
    e1 = cpw_fp.coverextension
    e2 = cpw_fp.coverwidth

#    old w_taper + 2*s_taper + 2*e1
#    rot(direction)

    if side == 'thz':
        layername(cpw_fp.coverlayer)
        base.wire(-direction, l1, e2)
        base.wire(direction, l_taper + param_1 + l2, e2)
        cpw_thz.tapergo(direction, l_taper, w_taper, s_taper)
        try:
            layername(cpw_thz.gndlayer)
        except:
            pass
        base.cpw(direction, param_1, w_taper, s_taper)
        movedirection(direction, param_2)
#        go(param_2, 0)
    elif side == 'fp':
        movedirection(direction,param_2 + l_taper)
        layername(cpw_fp.coverlayer)
        base.wire(direction, l1, e2)
        base.wire(-direction, l_taper + param_1 + l2, e2)
        cpw_thz.tapergo(-direction, l_taper, w_taper, s_taper)
        try:
            layername(cpw_thz.gndlayer)
        except:
            pass
        base.cpw(-direction, param_1, w_taper, s_taper)
        movedirection(direction,l_taper)
    else:
        print 'WARNING: INVALID SIDE'
#    rot(np.conjugate(direction))
    return direction

def coupler_Fabryperot_ms_cpw(direction,side,ms,width_overlap,l_overlap):
    line_w = 2 
    ms_coupler = ms.coupler(line_w,width_overlap)
    if side == 'thz':
        ms_coupler.wirego(-direction,l_overlap)
        ms_coupler.end_open(0)
        movedirection(direction,l_overlap)
        ms_coupler.wirego(direction,1)
        ms_coupler.end_open(direction)
        movedirection(-direction,1)
    elif side == 'fp':
        ms_coupler.wirego(direction,l_overlap)
        ms_coupler.end_open(0)
        movedirection(-direction,l_overlap)
        ms_coupler.wirego(-direction,1)
        ms_coupler.end_open(-direction)
        movedirection(direction,1)
    else:
        print 'Warning: INVALID SIDE'
    return direction

def coupler_Fabryperot_gap(direction, side, gap_length):
    movedirection(direction, gap_length)
    return direction


