# -*- coding: utf-8 -*-
"""
Created on Mon Jan 09 15:19:48 2017

@author: sebastian
"""

from PyClewin import *

import numpy as np

class Microstrip(object):
    '''
    Base microstrip class. Only draws central line and dielectric layer (both positive).
    Input:
        line        :: line width
        dielwidth   :: width of dielectric layer
        linelayer   :: metal layer for line
        diellayer   :: diel layer
        mesh        :: polygon resolution for corners
    '''
    def __init__(self, line, dielextension, linelayer, diellayer, mesh):
        self.line = line
        self.dielextension = dielextension
        self.dielwidth = 2*dielextension+self.line
        self.linelayer = linelayer
        self.diellayer = diellayer
        self.mesh = mesh
        self.tm_type = 'ms'
        self.direction = 1


    def process_direction(self, direction):
        if direction == None or direction == 0:
            direction = self.direction
        else:
            self.direction = direction
        return direction

    def taper(self, direction, L, newline):
        '''
        tapers only the central wire, do not care about dielectric width
        '''
        rot(direction)
        layername(self.linelayer)
        xyline = np.array([[0, 0, L, L], [-line/2., line/2., newline/2., -newline/2.]])
        poly(xyline)
        rotback()
        return direction

    def tapergo(self, direction, L, newline):
        self.taper(direction, L, newline)
        rot(direction)
        go(L, 0)
        rotback()
        return direction

    def wire(self, direction, L):
        layername(self.linelayer)
        wire(direction, L, self.line)
        layername(self.diellayer)
        wire(direction, L, self.dielwidth)
        self.direction = direction
        return direction

    def wirego(self, direction, L, **kwargs):
        self.wire(direction, L, **kwargs)
        rot(direction)
        go(L, 0)
        rotback()
        return direction

    def up(self, direction, R):
        layername(self.linelayer)
        turnup(direction, R, self.line, self.mesh)
        layername(self.diellayer)
        turnup(direction, R, self.dielwidth, self.mesh)

    def upgo(self, direction, R, **kwargs):
        self.up(direction, R, **kwargs)
        rot(direction)
        go(R, R)
        rotback()

    def down(self, direction, R):
        layername(self.linelayer)
        turndown(direction, R, self.line, self.mesh)
        layername(self.diellayer)
        turndown(direction, R, self.dielwidth, self.mesh)

    def downgo(self, direction, R, **kwargs):
        self.down(direction, R, **kwargs)
        rot(direction)
        go(R, -R)
        rotback()

    def up45(self, direction, R):
        layername(self.linelayer)
        turn45up(direction, R, self.line, self.mesh)
        layername(self.diellayer)
        turn45up(direction, R, self.dielwidth, self.mesh)

    def up45go(self, direction, R, **kwargs):
        self.up45(direction, R, **kwargs)
        rot(direction)
        xy45 = makeTurn(R, self.line, self.mesh, np.pi/4.)
        go((xy45[0][-1]+xy45[0][0])/2., (xy45[1][-1]+xy45[1][0])/2.)
        rotback()

    def down45(self, direction, R):
        layername(self.linelayer)
        turn45down(direction, R, self.line, self.mesh)
        layername(self.diellayer)
        turn45down(direction, R, self.dielwidth, self.mesh)

    def down45go(self, direction, R, **kwargs):
        self.down45(direction, R, **kwargs)
        rot(direction)
        xy45 = makeTurn(R, self.line, self.mesh, -np.pi/4)
        go((xy45[0][-1]+xy45[0][0])/2., (xy45[1][-1]+xy45[1][0])/2.)
        rotback()

    def end_open(self, direction, dielectric_length = -1):
        direction = self.process_direction(direction)
        if dielectric_length == -1 :
            dielectric_length = self.dielextension
        layername(self.diellayer)
        wire(direction, dielectric_length, self.dielwidth)
        return direction

    def end_short(self, direction, short_length):
        layername(self.linelayer)
        wire(direction, short_length, self.line)
        return direction



class Microstrip_protected(Microstrip):
    def __init__(self, line, dielextension, linelayer, diellayer, mesh, coverlayer, coverextension):
        """
        This is a class for a microstrip line with a protective layer to avoid etching into surrounding nbtin_gnd.
        WARNING: NOT ALL MICROSTRIP FUNCTIONS HAVE BEEN OVERWRITTEN WITH COVERLAYER
        """
        super(Microstrip_protected, self).__init__(line, dielextension, linelayer, diellayer, mesh)
        self.coverlayer = coverlayer
        self.coverextension = coverextension
        self.coverwidth = 2*coverextension + self.line

    def wire(self, direction, L, **kwargs):
        layername(self.coverlayer)
        wire(direction, L, self.coverwidth)
        super(Microstrip_protected, self).wire(direction, L, **kwargs)
        return direction

    def end_open(self, direction, dielectric_length = -1):
        direction = self.process_direction(direction)
        if dielectric_length == -1:
            dielectric_length = self.dielextension
        layername(self.coverlayer)
        wire(direction, self.coverextension, self.coverwidth)
        super(Microstrip_protected, self).end_open(direction, dielectric_length)

    def copy(self, **kwargs):
        """
        WARNING: NOT FULLY IMPLEMENTED
        """
        line = kwargs.pop('line' , self.line)
        return Microstrip_protected(line, self.dielextension, self.linelayer, self.diellayer, self.mesh, self.coverlayer, self.coverextension)


class Microstrip3layer(Microstrip):
    '''
    Microstrip with another diel layer below, MSLOC1-type
    '''
    def __init__(self, line, dielwidth, botwidth, linelayer, diellayer, botlayer, mesh):
        Microstrip.__init__(self, line, dielwidth, linelayer, diellayer, mesh)
        self.botwidth = botwidth
        self.botlayer = botlayer

    def taper(self, direction, L, newline):
        layername(self.botlayer)
        wire(direction, L, self.botwidth)
        super(Microstrip3layer, self).taper(direction, L, newline)

    def wire(self, direction, L):
        layername(self.botlayer)
        wire(direction, L, self.botwidth)
        super(Microstrip3layer, self).wire(direction, L)

    def up(self, direction, R):
        layername(self.botlayer)
        turnup(direction, R, self.botwidth, self.mesh)
        super(Microstrip3layer, self).wire(direction, R)

    def down(self, direction, R):
        layername(self.botlayer)
        turndown(direction, R, self.botwidth, self.mesh)
        super(Microstrip3layer, self).wire(direction, R)

