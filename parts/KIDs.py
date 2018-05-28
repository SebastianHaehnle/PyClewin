# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 13:49:01 2017

@author: sebastian
"""

from PyClewin import *

import numpy as np
import scipy.constants as spc
import collections

def kidStraight(direction, kid, ms, hybrid, wide, lShort, funcTransMSCPW, funcTransHybridWide, externalSiN = []):
    """
    auto switch between hybrid, pure wide and microstrip versions of a straight kid
    if no MS line instance is given provide the list externalSin = ['SiN layername', sinwidth]

    """
    # Get relevant values from input
    if ms != None:
        lms = kid.lms * 1e6
    else:
        lms = 0
    lhybrid = kid.lal * 1e6
    lwide = kid.lwide * 1e6

    # Start drawing from short position, draw in x-direction
    rot(direction)
    setmark('shortkidlevel')
    if lms:
        layername(ms.linelayer)
        wire(-1, lShort, ms.line)
        layername(ms.botlayer)
        wire(-1, ms.botwidth, ms.botwidth)
        ms.wirego(1, lms)
        setmark('kidlevel')
        if lhybrid:
            funcTransMSCPW(1, ms, hybrid)
        elif not(lhybrid) and lwide:
            funcTransMSCPW(1, ms, wide)
    if lhybrid:
        if not lms:
            layername(hybrid.linelayer)
            wire(-1, lShort, hybrid.line)
        if len(externalSiN) != 2 and ms == None:
            pass
        else:

            if len(externalSiN) == 2:
                layername(externalSiN[0])
                wire(1, lhybrid + externalSiN[1]/2., externalSiN[1])
                wire(-1, externalSiN[1], externalSiN[1])
            else:
                layername(ms.botlayer)
                wire(1, lhybrid + ms.botwidth/2., ms.botwidth)
                wire(-1, ms.botwidth, ms.botwidth)
        hybrid.wirego(1, lhybrid)
        setmark('KIDsin%d' % kid.index)
        if lwide:
            funcTransHybridWide(1, hybrid, wide)
    if lwide:
        if lms and not lhybrid:
            layername(ms.botlayer)
            wire(1, ms.botwidth/2., ms.botwidth)
            wire(-1, ms.botwidth, ms.botwidth)
        layername(wide.gndlayer)
        wide.wirego(1, lwide)
        wire(1, wide.gap , wide.wTotal())
    rot(np.conjugate(direction))
    setmark('KIDend%d' % kid.index)

def kidM4001membrane(direction, kid, hybrid, wide, lShort, funcTransHybridWide, externalSiN, membraneinfo, rturn):
    """
    Draw direction from shorted end onward. I.e. For a KID straight up with the shorted end on top direction is -1j
    SiNlayer is list [layername, sinwidth]
    membraneinfo: [wanted length on membrane, distance in y-direction on membrane]
    """
    lhybrid = kid.lal * 1e6
    lwide = kid.lwide * 1e6

    lturn = np.pi/2. * rturn # 2*pi*r / 4 for 90deg turn
    yturns = 4*rturn

    lreq = membraneinfo[0]
    yspace = membraneinfo[1]

    ystraight = (yspace - yturns)/2.
    if ystraight <= 0:
        print "WARNING: Not enough space for turns on membrane"
    xmeander = lreq - 2*ystraight - 4*lturn

    lremain = lhybrid - lreq
    print lreq, yspace, ystraight, xmeander, lremain

    rot(direction)
    setmark('shortkidlevel')
    layername(hybrid.linelayer)
    wire(-1, lShort, hybrid.line)
    layername(externalSiN[0])
    wire(1, lhybrid + externalSiN[1]/2., externalSiN[1])
    wire(-1, externalSiN[1], externalSiN[1])
    hybrid.wirego(1, ystraight)
    hybrid.downgo(1, rturn)
    hybrid.wirego(-1j, xmeander)
    hybrid.upgo(-1j, rturn)
    hybrid.upgo(1, rturn)
    hybrid.wirego(1j, xmeander)
    hybrid.downgo(1j, rturn)
    hybrid.wirego(1, ystraight)
    hybrid.wirego(1, lremain)
    setmark('KIDsin%d' % kid.index)
    funcTransHybridWide(1, hybrid, wide)
    layername(wide.gndlayer)
    wide.wirego(1, lwide)
    wire(1, wide.gap , wide.wTotal())
    rot(np.conjugate(direction))
    setmark('KIDend%d' % kid.index)