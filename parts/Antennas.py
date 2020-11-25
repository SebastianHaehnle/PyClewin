# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 16:02:29 2017

@author: sebastian

Antenna as classes / objects

direction is always towards the shorted end

"""

from PyClewin import *

import numpy as np
import scipy.constants as spc
import collections


class LeakyM4002(object):
    def __init__(self, w_membrane, t_wafer, KOH_layer, **kwargs):
        self.wTotal = kwargs.pop('wTotal', 990)
        self.hTotal = kwargs.pop('hTotal', 282.5)
        self.wSlot = kwargs.pop('wSlot', 3)
        self.hSlot = kwargs.pop('hSlot', 2)
        self.lTaper = (self.wTotal - self.wSlot)/2.
        self.centerline = kwargs.pop('centerline', 0)
        self.KOH_layer = KOH_layer
        self.t_wafer = t_wafer
        self.w_membrane = w_membrane

    def draw(self, direction, cpw, centerline = -1):
        """

        """
        if centerline == -1:
            centerline = self.centerline
        rot(direction)
        layername(self.KOH_layer)
        w_open = KOHopening(self.t_wafer, self.w_membrane)
        bar(1, w_open, w_open)

        layername(cpw.gndlayer)
        if centerline == 0:
            bar(1j, self.wSlot, self.hSlot)
        else:
            go(-self.hSlot/2., 0)
            cpw.wire(1, centerline)
            go(+self.hSlot/2., 0)

        go(0, self.wSlot/2.)
        broaden(1j, self.lTaper, self.hSlot, self.hTotal)
        go(0, -self.wSlot)
        broaden(-1j, self.lTaper, self.hSlot, self.hTotal)
        go(-self.hSlot/2.+ centerline, self.wSlot/2.)
        rot(np.conjugate(direction))
        setmark('antenna_connector')


class Doubleslot(object):
    def __init__(self, w_cpw, s_cpw, l_cpw, l_short, s_slot, s_connect, h_1, h_2, w_2, layer):
        self.w_cpw = w_cpw # width of cpw line
        self.s_cpw = s_cpw # width of cpw slot
        self.l_cpw = l_cpw # length cpw section (use this to adjust impedance transformer)
        self.l_short = l_short # cpw stub length
        self.s_slot = s_slot # width of antenna main slot
        self.s_connect = s_connect # width of slot connecting antenna and cpw
        self.h_1 = h_1 # length of slot connecting antenna and cpw
        self.h_2 = h_2 # length of the four antenna fingers
        self.w_2 = w_2 # total width of the antenna (including slot width)
        self.layer = layer  # metal layer to draw in

    def draw(self, direction, cpw = None):
        """
        direction is towards feed line
        """
        # Move into local coodinates
        rot(direction)
        setmark('temp_antenna')

        # common layer for everything
        base.layername(self.layer)

        # Draw cpw short to GND
        base.cpwgo(-1, self.s_connect/2, self.w_cpw, self.s_cpw)
        base.cpw(-1, self.l_short, self.w_cpw, self.s_cpw)
        gomark('temp_antenna')

        # Draw upper slot
        go(0, self.w_cpw/2+self.s_cpw)
        base.wirego(1j, self.h_1, self.s_connect)
        go(0, self.s_slot/2)
        setmark('temp_antenna_2')
        # draw upper slot, right section
        base.wirego(1, self.w_2/2, self.s_slot)
        go(self.s_slot/2, -self.s_slot/2)
        base.wirego(1j, self.h_2+self.s_slot, self.s_slot)
        # Draw upper slot, left section
        gomark('temp_antenna_2')
        base.wirego(-1, self.w_2/2, self.s_slot)
        go(-self.s_slot/2, -self.s_slot/2)
        base.wirego(1j, self.h_2+self.s_slot, self.s_slot)

        # Draw lower slot
        gomark('temp_antenna')
        go(0, -(self.w_cpw/2+self.s_cpw))
        base.wirego(-1j, self.h_1, self.s_connect)
        go(0, -self.s_slot/2)
        setmark('temp_antenna_2')
        # draw lower slot, right section
        base.wirego(1, self.w_2/2, self.s_slot)
        go(self.s_slot/2, self.s_slot/2)
        base.wirego(-1j, self.h_2+self.s_slot, self.s_slot)
        # Draw lower slot, left section
        gomark('temp_antenna_2')
        base.wirego(-1, self.w_2/2, self.s_slot)
        go(-self.s_slot/2, +self.s_slot/2)
        base.wirego(-1j, self.h_2+self.s_slot, self.s_slot)

        # Draw cpw section towards antenna connector
        gomark('temp_antenna')
        base.cpwgo(1, self.l_cpw, self.w_cpw, self.s_cpw)

        # Move out of local coordinates
        rot(np.conjugate(direction))
        setmark('antenna_connector')
        delmark('temp_antenna')
        delmark('temp_antenna_2')

    @staticmethod
    def gen_from_Juan(w_cpw, s_cpw, l_cpw, l_stub, W1_ant, W2_ant, d_ant, W_ant, L_ant, layer):
        h_1 = (d_ant - w_cpw - 2*s_cpw)/2.
        h_2 = (L_ant - d_ant - 2*W1_ant)/2
        w_2 = (W_ant - W1_ant)
        return Doubleslot(w_cpw, s_cpw, l_cpw, l_stub, W1_ant, W2_ant, h_1, h_2, w_2, layer)
"""
 Kevin: Doubleslot.gen_from_Juan(line_cpw, slot_cpw, L_transformer + 4.843 ,L_stub, W1ant, W2ant, dant, Want, Lant, 'Mat_plane')
"""
# Silicon doubleslot by Juan for Ls = 1.1 pH @ 350 GHz
doubleSlot_350ghz_Si_NbTiN100nm = Doubleslot.gen_from_Juan(3, 2.1857, 4.843+71, 0, 14.571, 9.686, 29.143, 137.143, 235.714, 'NbTiN_GND')
doubleSlot_650ghz_Si_NbTiN100nm = Doubleslot.gen_from_Juan(2, 2, 0, 4.615, 7.846, 5.215, 15.692, 73.846, 124.615, 'NbTiN_GND')
doubleSlot_850ghz_Si_NbTiN100nm = Doubleslot.gen_from_Juan(2., 2., 0., 4.235, 6.0, 3.988, 12.0, 56.471, 95.294, 'NbTiN_GND')
doubleSlot_1100ghz_Si_NbTiN100nm = Doubleslot.gen_from_Juan(2., 2., 0., 6.818, 4.636, 3.082, 9.273, 43.636, 73.636, 'NbTiN_GND')
# Sapphire doubleslot by Juan for Ls = 1.03 pH @ 350 GHz (April 2020)
doubleSlot_350ghz_Sapphire_NbTiN100nm = Doubleslot.gen_from_Juan(3.5, 1.5, 9.798/2.+216.763, 0, 14.740, 9.798, 24.0, 137.143, 242.775, 'NbTiN_GND')
doubleSlot_650ghz_Sapphire_NbTiN100nm = Doubleslot.gen_from_Juan(3.5, 1.5, 5.060/2.+109.411, 0, 7.612, 5.060, 14.552, 71.642, 125.373, 'NbTiN_GND')
doubleSlot_850ghz_Sapphire_NbTiN100nm = Doubleslot.gen_from_Juan(3.5, 1.5, 3.919/2.+84.746, 0, 5.896, 3.919, 12.0, 55.401, 97.110, 'NbTiN_GND')
doubleSlot_1100ghz_Sapphire_NbTiN100nm = Doubleslot.gen_from_Juan(3.5, 1.5, 3.229/2.+69.815, 0, 4.857, 3.229, 10.571, 45.714, 80.00, 'NbTiN_GND')


if __name__ == '__main__':
    pass
