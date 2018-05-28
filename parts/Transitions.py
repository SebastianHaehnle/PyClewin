# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 14:15:43 2017

@author: sebastian
"""

from clepywin import *

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
    broadengo(1, ltaper, ms.line, hybrid.wTotal())
    wire(1, loverlap, hybrid.wTotal())
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
    

def transHybridWideM4000(direction, hybrid, wide, **kwargs):
    ltrans = 21.
    rot(direction)
    layername(hybrid.linelayer)
    wire(1, 2/3.*ltrans, hybrid.line)
    layername(hybrid.gndlayer)
    broaden(1, 1/3.*ltrans, hybrid.line, wide.line/2.)
    cpwbroadengo(1, ltrans, 0, hybrid.wTotal(), wide.line, wide.gap)
    rotback()