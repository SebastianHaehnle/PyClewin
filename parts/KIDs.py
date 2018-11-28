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

class KID_mask(object):
    def __init__(self,shape = 'straight', short_length = 10, coupler = None):
        self.shape = shape
        self.short_length = short_length
        self.coupler = coupler
        self.kidids = []
        self.connections_coupler = {}
        self.connections_short = {}


class Hybrid(KID_mask):
    def __init__(self, line_hybrid, line_wide, line_coupler, transition_hybrid, transition_coupler,  short_length = 10, shape = 'straight',  SiN_patchtype = 'full', SiN_layer = 'SiN_wafer', SiN_size = [6, 100]):
        """
        This instance defines the general KID structure to be used (hybrid cpw, wide cpw, coupler cpw).
        Use draw() method to write individual KIDs with defined section lengths.

        SiN_margin is [length_margin, width_margin]
        """
        KID_mask.__init__(self, shape = shape, short_length = short_length)
        self.type = 'hybrid'
        self.line_hybrid = line_hybrid
        self.line_wide = line_wide
        self.line_coupler = line_coupler

        self.transition_hybrid = transition_hybrid
        self.transition_coupler = transition_coupler
        self.SiN_patchtype = SiN_patchtype
        self.SiN_layer = SiN_layer
        self.SiN_size = SiN_size




    def draw(self, direction, l_hybrid, l_wide, l_coupler, kid_id, coupler_included = True, start = 'short'):
        """
        Draws KID with structure as defined by self instance at current point.
        L_tot = l_hybrid + l_wide + l_coupler

        Input:
            start : Defines where the input position is defined. Default is at the short (i.e. the hybrid end)

        Inserts end of coupler position as "KID_coupler_[kid_id]" where kid_id is input parameter
        """
        if coupler_included:
            l_wide = l_wide - l_coupler
        self.kidids.append(kid_id)
        rot(direction)
        setmark('kidlevel_short')
        if 'straight' in self.shape:
            if self.short_length != 0:
                base.layername(self.line_hybrid.linelayer)
                base.wire(-1, self.short_length, self.line_hybrid.line)
            self.connections_short[kid_id] = base.connector(direction, 'KID_short_%d' % kid_id)
            self.line_hybrid.wirego(1, l_hybrid)
            self.transition_hybrid(1, self.line_hybrid, self.line_wide)
            setmark('kidlevel_widestart')
            self.line_wide.wirego(1, l_wide)
            if 'elbow' in self.shape:
                self.transition_coupler(1j, self.line_wide, self.line_coupler, direction_in = 1)
                self.line_coupler.wirego(1j, l_coupler)
                setmark('kidlevel_open')
                self.line_coupler.open_end(1j)
                self.connections_coupler[kid_id] = base.connector(np.exp(1j*(np.angle(direction)+np.pi/2)), 'KID_coupler_%d' % kid_id)
            elif self.transition_coupler == None:
                self.line_coupler.wirego(1, l_coupler)
                setmark('kidlevel_open')
                self.line_coupler.open_end(1)
                self.connections_coupler[kid_id] = base.connector(-direction, 'KID_coupler_%d' % kid_id)
            else:
                self.transition_coupler(1, self.line_wide, self.line_coupler)
                self.line_coupler.wirego(1, l_coupler)
                setmark('kidlevel_open')
                self.line_coupler.open_end(1)
                self.connections_coupler[kid_id] = base.connector(-direction, 'KID_coupler_%d' % kid_id)
            self.draw_SiN(*self.SiN_size)
        gomark('kidlevel_open')
        rot(np.conjugate(direction))
        setmark('KID_coupler_%d' % kid_id)

    def draw_SiN(self, length, width):
        base.layername(self.SiN_layer)
        if self.SiN_patchtype == 'full' and self.shape == 'straight':
            if self.type == 'hybrid_fabryperot':
                gomark('kidlevel_short')
            elif self.type == 'broadband':
                gomark('kidlevel_hybridstart')
            else:
                gomark('kidlevel_short')
            base.wire(-1, length, width)
            base.wire(1, x2m('kidlevel_widestart') + length, width)
        base.layername(self.line_hybrid.gndlayer)

class Hybrid_Fabryperot(Hybrid):
    def __init__(self, line_hybrid, line_wide, line_coupler, transition_hybrid, transition_coupler, line_thz, transition_thz, SiN_layer = 'SiN_wafer', SiN_size = [6, 100]):
        Hybrid.__init__(self, line_hybrid, line_wide, line_coupler, transition_hybrid, transition_coupler,
                     SiN_layer = SiN_layer, SiN_size = SiN_size,
                     SiN_patchtype = 'full', shape = 'straight', short_length = 0)
        self.type = 'hybrid_fabryperot'
        self.line_thz = line_thz
        self.transition_thz = transition_thz

    def draw(self, direction, l_hybrid, l_wide, l_coupler, l_thz, kid_id, coupler_included = True, start = 'short'):
        setmark('kidlevel_fp')
        # Draw thz line and transition to aluminum first
        self.line_thz.wirego(direction, l_thz)
        self.transition_thz(direction, self.line_thz, self.line_hybrid)
        super(Hybrid_Fabryperot, self).draw(direction, l_hybrid, l_wide, l_coupler, kid_id, coupler_included, start)


class KID_NBTIN(KID_mask):
    def __init__(self, line_wide, line_coupler, transition_coupler, shape = 'straight', short_length = 0):
        KID_mask.__init__(self, shape = shape, short_length = short_length)
        self.line_wide = line_wide
        self.line_coupler = line_coupler
        self.transition_coupler = transition_coupler


    def draw(self, direction, l_wide, l_coupler, kid_id, coupler_included = True, start = 'short'):
        if coupler_included:
            l_wide = l_wide - l_coupler
        self.kidids.append(kid_id)

        rot(direction)
        setmark('kidlevel_short')
        if 'straight' in self.shape:
            base.layername(self.line_wide.gndlayer)
            if self.short_length != 0:
                base.wire(-1, self.short_length, self.line_wide.line)
            self.connections_short[kid_id] = base.connector(direction, 'KID_short_%d' % kid_id)
            self.line_wide.wirego(1, l_wide)
            if 'elbow' in self.shape:
                self.transition_coupler(1j, self.line_wide, self.line_coupler, direction_in = 1)
                self.line_coupler.wirego(1j, l_coupler)
                setmark('kidlevel_open')
                self.line_coupler.open_end(1j)
                self.connections_coupler[kid_id] = base.connector(np.exp(1j*(np.angle(direction)+np.pi/2)), 'KID_coupler_%d' % kid_id)
            elif self.transition_coupler == None:
                self.line_coupler.wirego(1, l_coupler)
                setmark('kidlevel_open')
                self.line_coupler.open_end(1)
                self.connections_coupler[kid_id] = base.connector(-direction, 'KID_coupler_%d' % kid_id)
            else:
                self.transition_coupler(1, self.line_wide, self.line_coupler)
                self.line_coupler.wirego(1, l_coupler)
                setmark('kidlevel_open')
                self.line_coupler.open_end(1)
                self.connections_coupler[kid_id] = base.connector(-direction, 'KID_coupler_%d' % kid_id)
        gomark('kidlevel_open')
        rot(np.conjugate(direction))
        setmark('KID_coupler_%d' % kid_id)

class KID_COUPLED_BROADBAND(Hybrid_Fabryperot):
    def __init__(self, line_hybrid, line_wide, line_coupler, transition_hybrid, transition_coupler, line_thz, transition_thz, SiN_layer = 'SiN_wafer', SiN_size = [6, 100]):
        Hybrid_Fabryperot.__init__(self, line_hybrid, line_wide, line_coupler, transition_hybrid, transition_coupler, line_thz, transition_thz, SiN_layer, SiN_size)
        self.type = 'broadband'

    def draw(self, direction_thz, direction_kid, l_hybrid, l_wide, l_coupler, l_thz, kid_id, coupler_included = True, start = 'short'):
        if coupler_included:
            l_wide = l_wide - l_coupler
        self.kidids.append(kid_id)

        l_thz_2 = 24
        r_thz = 4.7
        l_thz_curve = r_thz*np.pi/2
        setmark('kidlevel_short')
        self.line_thz.wirego(direction_thz, l_thz - l_thz_2 - l_thz_curve)
        self.line_thz.turngo(direction_thz, direction_kid, r_thz)
        self.line_thz.wirego(0, l_thz_2/2.)
        # dont draw bridge
#        try:
#            self.line_thz.bridge.draw(self.line_thz.direction, self.line_thz.line, self.line_thz.slot)
#        except:
#            print "WARNING: No bridge defined for thz line in broadband coupled KID."
        self.line_thz.wirego(0, l_thz_2/2.)
        setmark('kidlevel_hybridstart')
        localdir = self.transition_thz(self.line_thz.direction, self.line_thz, self.line_hybrid)
        self.line_hybrid.wirego(localdir, l_hybrid)
        localdir = self.transition_hybrid(self.line_hybrid.direction, self.line_hybrid, self.line_wide)
        setmark('kidlevel_widestart')
        self.line_wide.wirego(localdir, l_wide)
        if self.transition_coupler == None:
            self.line_coupler.wirego(self.line_wide.direction, l_coupler)
            self.line_coupler.open_end(0)
            self.connections_coupler[kid_id] = base.connector(-self.line_coupler.direction, 'KID_coupler_%d' % kid_id)
        setmark('KID_coupler_%d' % kid_id)
        self.draw_SiN(*self.SiN_size)

class KID_MS_pure(KID_mask):
    def __init__(self, line_ms,line_ms_clean, line_coupler, shape = 'straight', short_length = -1):
        KID_mask.__init__(self, shape = shape, short_length = short_length)
        self.type = 'ms'
        self.line_ms = line_ms
        self.line_ms_clean = line_ms_clean
        self.line_coupler = line_coupler

    def draw(self, direction, l_kid, l_coupler, kid_id, coupler_included = True, start = 'short'):
        if coupler_included:
            l_kid = l_kid - l_coupler
        self.kidids.append(kid_id)
        setmark('kidlevel_short')
        if self.short_length < 0:
            self.line_ms.end_open(-direction, 10)
        else:
            self.line_ms.end_short(direction, 10)
        self.line_ms.wirego(direction, l_kid - self.line_coupler.dielextension)
        self.line_ms_clean.wirego(direction, self.line_coupler.dielextension)    
        """ NOTE THIS SECTION WAS MODIFIED TO MAKE SURE THE EXTRA NBTIN SECTION FOR THE ASI COVERED STRIP WOULD NOT RUN UNTO THE READOUT LINE """
        # Go to starting point of elbow, check where the 0 is really defined
        base.movedirection(direction, self.line_coupler.line/2.)
        base.movedirection(direction*(-1j), self.line_ms.line/2.)
        self.line_coupler.end_open(self.line_ms.direction*(-1j))
        self.line_coupler.wirego(self.line_ms.direction*1j, l_coupler + self.line_coupler.line/2.)
        self.line_coupler.end_open(0)
        

#        print "WARNING: COUPLER NOT FULLY IMPLEMENTED"
        self.connections_coupler[kid_id] = base.connector(self.line_coupler.direction, 'KID_coupler_%d' % kid_id)
        setmark('KID_coupler_%d' % kid_id)
