# -*- coding: utf-8 -*-
"""
Created on Mon Jan 09 17:43:25 2017

@author: sebastian
"""

from clepywin import *

def bondpadM4000(direction, rocpw):
    '''
    bondpad geometry from sonnet for 50 Ohm, crosschecked with Svens tool
    THIS IS WRONG. RECHECK GIVES 44 Ohm
    '''
    wbond = 600.
    sbond = 225.
    extenddiel = 100
    ltaper = 500.
    lbond = 400.
    lisolation = 50.
    setmark('temp')
    rot(direction)
    layername(rocpw.diellayer)
    # draw underlying dielectric layer
    wire(1, (ltaper + lbond), wbond + 2*sbond + extenddiel)
    # Draw bondpad as extension of readoutline
    rocpw.tapergo(1, ltaper, wbond, sbond)
    cpwgo(1, lbond, wbond, sbond)
    # Add isolation from ground
    wire(-1, lisolation, wbond + 2*sbond)
    gomark('temp')    

def bondpadM4001(direction, rocpw, distToEdge):
    """
    Bondpad geometry copied from amkid
    """
    wbond = 400.
    sbond = 220.
    ltaper = 500.
    lbond = 400.
    lisolation = 60.
    totallength = lbond+ltaper+lisolation
    setmark('temp')
    rot(direction)
    rocpw.wirego(1, distToEdge-totallength)
    setmark('tempbondstart')
    layername(rocpw.diellayer)
    # draw underlying dielectric layer
#    broadengo(1, (ltaper + lbond), wbond + 2*sbond + extenddiel)
    broadengo(1, ltaper, rocpw.line + rocpw.gap, wbond + rocpw.gap)
    wirego(1, lbond +rocpw.gap, wbond + rocpw.gap)
    gomark('tempbondstart')
    # Draw bondpad as extension of readoutline
    rocpw.tapergo(1, ltaper, wbond, sbond)
    cpwgo(1, lbond, wbond, sbond)
    # Add isolation from ground
    wire(1, lisolation, wbond + 2*sbond)
    gomark('temp')    

def couplerM4000(kidmark, lc, dc, cpwwide, cpwro, rturn):
    """
    M4000 kid coupler design, attaches to the right side of a straight kid

    """
    lineDist = (cpwwide.wTotal() + cpwro.wTotal())/2. + dc + manVars.nbtinLine
    setmark('temp')
    gomark(kidmark)
    go(lineDist, 0)
    # draw the inverse U-shaped coupler
    cpwro.wirego(1j, lc)
    cpwro.downgo(1j, rturn, bridgeFront = False)
    cpwro.downgo(1, rturn, bridgeFront = False)
    cpwro.wirego(-1j, lc)
    if y2m('temp')-rturn < 200:
        bridgeFront = False
    else:
        bridgeFront = True
    cpwro.wirego(-1j, y2m('temp')-rturn, bridgesOff = True, bridgeDistance = 100, bridgeStart = True)
    cpwro.upgo(-1j, rturn, bridgeFront = bridgeFront)
    # Draw line to starting point on the right
    cpwro.wirego(1, x2m('temp'))
    gomark(kidmark)
    go(lineDist, 0)    
    if y2m('temp')-rturn < 200:
        bridgeFront = False
    else:
        bridgeFront = True
    # Draw the part which connects to the left of the readoutline
    cpwro.wirego(-1j, y2m('temp')-rturn, bridgesOff = True, bridgeDistance = 100, bridgeStart = True)

    cpwro.downgo(-1j, rturn, bridgeFront = bridgeFront)
    
def couplerM4000left(direction, kidmark, lc, dc, cpwwide, cpwro, rturn):
    """
    M4000 kid coupler design, attaches to the left side of a straight kid

    """
    setmark('temp')
    lineDist = (cpwwide.wTotal() + cpwro.wTotal())/2. + dc + manVars.nbtinLine
    gomark(kidmark)
#    rot(direction)
#    go(-lineDist, 0)
    go(lineDist, 0)
    # draw the inverse U-shaped coupler
    cpwro.wirego(-1j, lc)
    cpwro.upgo(-1j, rturn, bridgeFront = False)
    cpwro.upgo(1, rturn, bridgeFront = False)
    cpwro.wirego(1j, lc)
    if y2m('temp')-rturn < 200:
        bridgeFront = False
    else:
        bridgeFront = True
    cpwro.wirego(1j, y2m('temp')-rturn, bridgesOff = True, bridgeDistance = 100, bridgeStart = True)
    cpwro.downgo(1j, rturn, bridgeFront = bridgeFront)
    print x2m('temp')
    # Draw line to starting point on the right
    cpwro.wirego(1, x2m('temp'))
    gomark(kidmark)
#    rot(direction)
    go(lineDist, 0)
    # Draw the part which connects to the left of the readoutline
    if y2m('temp')-rturn < 200:
        bridgeFront = False
    else:
        bridgeFront = True
    cpwro.wirego(1j, y2m('temp')-rturn, bridgesOff = True, bridgeDistance = 100, bridgeStart = True)
    cpwro.upgo(1j, rturn, bridgeFront = bridgeFront)
