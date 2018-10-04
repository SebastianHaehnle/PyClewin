# -*- coding: utf-8 -*-
"""
Created on Mon Jan 09 17:43:25 2017

@author: sebastian
"""

from PyClewin import *
#import numpy as np

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

def bondpad_100nm_Si(direction, rocpw, distToEdge):
    """
    Bondpad geometry for 50ohm on Si/SiN with 100nm NbTiN (1.0 pH)
    """
    wbond = 400.
    sbond = 200.
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


def couplerM4000(kidmark, l_coupler, d_coupler, cpwcoupler, cpwro):
    """
    M4000 kid coupler design, attaches to the right side of a straight kid
    kidmark is end of kid line
    """
    # old backend compatibility
    cpwwide = cpwcoupler
    lc = l_coupler
    dc = d_coupler
    lineDist = (cpwwide.wTotal + cpwro.wTotal)/2. + dc
    setmark('temp')
    gomark(kidmark)
    go(lineDist, 0)
    # draw the inverse U-shaped coupler
    cpwro.wirego(1j, lc)
    cpwro.downgo(1j, bridgeFront = False)
    cpwro.downgo(1,  bridgeFront = False)
    cpwro.wirego(-1j, lc)
    if y2m('temp')-cpwro.R < 200:
        bridgeFront = False
    else:
        bridgeFront = True
    cpwro.wirego(-1j, y2m('temp')-cpwro.R, bridgesOff = True, bridgeDistance = 100, bridgeStart = True)
    cpwro.upgo(-1j,  bridgeFront = bridgeFront)
    # Draw line to starting point on the right
    cpwro.wirego(1, x2m('temp'))
    gomark(kidmark)
    go(lineDist, 0)
    if y2m('temp')-cpwro.R < 200:
        bridgeFront = False
    else:
        bridgeFront = True
    # Draw the part which connects to the left of the readoutline
    cpwro.wirego(-1j, y2m('temp')-cpwro.R, bridgesOff = True, bridgeDistance = 100, bridgeStart = True)

    cpwro.downgo(-1j, bridgeFront = bridgeFront)

def couplerM4000left(direction, kidmark, lc, dc, cpwwide, cpwro, rturn):
    """
    M4000 kid coupler design, attaches to the left side of a straight kid

    """
    setmark('temp')
    lineDist = (cpwwide.wTotal+ cpwro.wTotal)/2. + dc
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


### COUPLERS
class couplerDeshima(object):
    def __init__(self, d_coupler, d_turn, cpw_coupler, cpw_ro,  l_out_min = 0):
        self.cpw_coupler = cpw_coupler
        self.cpw_ro = cpw_ro
        self.d_coupler = d_coupler
        self.d_turn = d_turn
        self.l_out_min = l_out_min


    def draw(self, direction_in, direction_coupler, kidmark, l_coupler, l_out = None, side = 'dynamic', debug = False):
        setmark('couplerlevel_start')
        # Get distance to kid
        if np.isclose(direction_in.real, 0):
            coupler_distance, ro_length = base.dist2mark(kidmark)
        elif np.isclose(direction_in.imag, 0):
            ro_length, coupler_distance = base.dist2mark(kidmark)
        else:
            print "WARNING: STRANGE INPUT FOR DESHIMA COUPLER"

        # Define section lengths:
        l_1 = self.d_turn - 2*self.cpw_ro.R # bottom length of U in U-turn
        d_lines = (self.cpw_coupler.wTotal+ self.cpw_ro.wTotal)/2. + self.d_coupler # width of U-turn
        if l_1 > 0:
            l_2 = ro_length - l_1 - 3*self.cpw_ro.R - d_lines
        else:
            l_2 = ro_length - 3*self.cpw_ro.R - d_lines # distance from start to entrance of U-turn
        # Check which side the coupler should attach to in dynamic case
        if side == 'dynamic':
            if l_2 < 1.5*self.d_turn:
                # attach on far side of readout start-point if start-point is too close to coupler section
                side = 'far'
                l_2 = l_2 + 2*d_lines  + l_1 + 2*self.cpw_ro.R
            else:
                side = 'close'
        l_3_in = coupler_distance - 1*self.cpw_ro.R # Distance from start to beginning of coupler section
        l_3_out = l_out or l_3_in
        if l_3_out < self.l_out_min:
            print "WARNING: COUPLER OUT LENGTH SHORTER THAN MINIMUM"
        if debug:
            print coupler_distance, ro_length
            print l_1, l_2, l_3_in, l_3_out
#            print gg.cle, print base.
        # Draw shit
        self.cpw_ro.wirego(direction_in, l_2)
        self.cpw_ro.turngo(0, direction_coupler, bridgeFront = True, bridgeAfter = True)

#        if self.l_out_min > 0:
        print l_3_in, self.l_out_min, l_3_in - self.l_out_min
        self.cpw_ro.wirego(0, l_3_in - self.l_out_min)
        if self.l_out_min > 0:
            self.cpw_ro.wirego(0, self.l_out_min, bridgePositions = [self.l_out_min/2.])
        self.cpw_ro.wirego(0, l_coupler)
        if side == 'close':
            self.cpw_ro.turngo(0, direction_in, bridgeFront = True, bridgeAfter = False)
        else:
            self.cpw_ro.turngo(0, direction_in, bridgeFront = False, bridgeAfter = False)
        if l_1 > 0:
            self.cpw_ro.wirego(0, l_1)
        if side == 'close':
            self.cpw_ro.turngo(0, -direction_coupler, bridgeFront = False, bridgeAfter = False)
        else:
            self.cpw_ro.turngo(0, -direction_coupler, bridgeFront = False, bridgeAfter = True)
        self.cpw_ro.wirego(0, l_coupler)
        if self.l_out_min > 0:
            self.cpw_ro.wirego(0, self.l_out_min, bridgePositions = [self.l_out_min/2.])
        self.cpw_ro.wirego(0, l_3_out-self.l_out_min)
        self.cpw_ro.turngo(0, +direction_in)
        delmark('couplerlevel_start')
        return self.cpw_ro.direction


    def connect(self, kid_connection, direction_in, l_coupler, next_connection = None, side = 'dynamic', debug = False, **kwargs):
        temp_coupler = self.cpw_coupler
        temp_d_coupler = self.d_coupler
        if 'line_coupler' in kwargs:
            self.cpw_coupler = kwargs['line_coupler']
        if 'd_coupler' in kwargs:
            self.d_coupler = kwargs['d_coupler']

        if next_connection:
            # Distance between the two connectors
            delta_distance = base.dist_marktomark(kid_connection.mark, next_connection.mark)
            # direction of connector in vector form
            dir_vector = np.array([next_connection.direction.real, next_connection.direction.imag])/np.abs(next_connection.direction)
            # distance along direction
            dir_distance = np.dot(delta_distance, -dir_vector)
            l_out = max(self.l_out_min, dir_distance + self.l_out_min)
        else:
            l_out = None
        if kid_connection.direction != direction_in and kid_connection.direction != -direction_in:
            self.draw(direction_in, kid_connection.direction, kid_connection.mark, l_coupler, l_out, side, debug)
        elif kid_connection.direction == -direction_in:
            distance = base.dist2markSigned(kid_connection.mark)
            dir_vector = np.array([direction_in.real, direction_in.imag])/np.abs(direction_in)
            dir_distance = np.dot(dir_vector, distance) # in line distance to kid
            perp_distance = np.dot(-dir_vector[::-1], distance) # perpendicular distance to kid
            perp_vector = -dir_vector[::-1]
            if dir_distance > -self.l_out_min:
                self.cpw_ro.wirego(direction_in, max(0, dir_distance +self.l_out_min))
#                self.cpw_ro.wirego(0, self.l_out_min)
                self.cpw_ro.turngo(0, perp_vector[0] + 1j*perp_vector[1])
                self.draw(self.cpw_ro.direction, kid_connection.direction, kid_connection.mark, l_coupler, l_out, side, debug)
            else:
                self.cpw_ro.turngo(0, perp_vector[0] + 1j*perp_vector[1])
                self.draw(self.cpw_ro.direction, kid_connection.direction, kid_connection.mark, l_coupler, l_out, side, debug)
        self.cpw_coupler = temp_coupler
        self.d_coupler = temp_d_coupler

class coupler_CPWtoMS(object):
    def __init__(self, cpw_readout):
        pass



class ReadoutLine(object):
    def __init__(self, tmline, bondpad):
        """
        Single box readout class. Takes 2 bondpad connections and infinite kid connections and automatically draws readoutline.
        Requires:
            transmissionline class for line (CPW or MS)
            bondbad function/class
        """
        self.tmline = tmline
