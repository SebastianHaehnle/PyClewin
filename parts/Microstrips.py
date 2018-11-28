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
    def __init__(self, line, dielextension, linelayer, diellayer, mesh, R=0):
        self.type = 'microstrip'
        self.line = line
        self.dielextension = dielextension
        self.dielwidth = 2*dielextension+self.line
        self.linelayer = linelayer
        self.diellayer = diellayer
        self.mesh = mesh
        self.tm_type = 'ms'
        self.direction = 1
        self.R = R


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
        direction = self.process_direction(direction)
        layername(self.linelayer)
        wire(direction, L, self.line)
        layername(self.diellayer)
        wire(direction, L, self.dielwidth)
        return direction

    def wirego(self, direction, L, **kwargs):
        direction = self.process_direction(direction)
        self.wire(direction, L, **kwargs)
        rot(direction)
        go(L, 0)
        rotback()
        return direction

    def up(self, direction, R):
        if R == -1:
            R = self.R
        layername(self.linelayer)
        turnup(direction, R, self.line, self.mesh)
        layername(self.diellayer)
        turnup(direction, R, self.dielwidth, self.mesh)

    def upgo(self, direction, R, **kwargs):
        if R == -1:
            R = self.R
        direction = self.process_direction(direction)
        self.up(direction, R, **kwargs)
        rot(direction)
        go(R, R)
        rotback()
        return direction

    def down(self, direction, R):
        if R == -1:
            R = self.R
        layername(self.linelayer)
        turndown(direction, R, self.line, self.mesh)
        layername(self.diellayer)
        turndown(direction, R, self.dielwidth, self.mesh)

    def downgo(self, direction, R, **kwargs):
        if R == -1:
            R = self.R
        direction = self.process_direction(direction)
        self.down(direction, R, **kwargs)
        rot(direction)
        go(R, -R)
        rotback()
        return direction

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

    def turn(self, direction_in, direction_out, R = -1, *args, **kwargs):
        if base.cornerDirection(direction_in, direction_out) > 0:
            self.up(direction_in, R, *args, **kwargs)
        else:
            self.down(direction_in, R, *args, **kwargs)
        return direction_in

    def turngo(self, direction_in, direction_out, R = -1, *args, **kwargs):
        if direction_in == None or direction_in == 0:
            direction_in = self.direction
        else:
            self.direction = direction_in
        if base.cornerDirection(direction_in, direction_out) > 0:
            self.upgo(direction_in, R, *args, **kwargs)
        else:
            self.downgo(direction_in, R, *args, **kwargs)
        self.direction = direction_out
#        self.used_wires.append([direction_out, self.R, direction_in])
        return direction_out

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
    def __init__(self, line, dielextension, linelayer, diellayer, mesh, coverlayer, coverextension, R = 0):
        """
        This is a class for a microstrip line with a protective layer to avoid etching into surrounding nbtin_gnd.
        WARNING: NOT ALL MICROSTRIP FUNCTIONS HAVE BEEN OVERWRITTEN WITH COVERLAYER
        """
        super(Microstrip_protected, self).__init__(line, dielextension, linelayer, diellayer, mesh, R = R)
        self.type = 'microstrip protected'
        self.coverlayer = coverlayer
        self.coverextension = coverextension
        self.coverwidth = 2*coverextension + self.line

    def wire(self, direction, L, **kwargs):
        direction = self.process_direction(direction)
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

    def coupler(self, line_old, width_overlap):
        """
        WARNING: TRAIL AND ERROR BY KEVIN
        """

        diff_line = (width_overlap-line_old)/2
        die_ext = self.dielextension - diff_line/10
        cover_ext = self.coverextension - diff_line
        return Microstrip_protected(width_overlap, die_ext, self.linelayer, self.diellayer, self.mesh, self.coverlayer, cover_ext)

class Microstrip_burried(Microstrip):
    def __init__(self, line, dielextension, widthextension, widthoverlap, linelayer, diellayer, mesh, coverlayer, coverextension, R = 0):
        """
        This is a class for a burried microstrip line with an extra section of NbTiN for better adhesion of the aSi layer.
        WARNING: NOT ALL MICROSTRIP FUNCTIONS HAVE BEEN OVERWRITTEN WITH COVERLAYER
        """
        super(Microstrip_burried, self).__init__(line, dielextension, linelayer, diellayer, mesh, R = R)
        self.type = 'microstrip buried'
        self.widthoverlap = widthoverlap
        self.widthextension = widthextension
        self.coverlayer = coverlayer
        self.coverextension = coverextension
        self.coverwidth = 2*coverextension + self.line
        self.jumpdistance = dielextension + widthextension - widthoverlap/2 + self.line/2

    def wire(self, direction, L, **kwargs):
        direction = self.process_direction(direction)
        #layername(self.coverlayer)
        #wire(direction, L, self.coverwidth)
        layername(self.linelayer)
        movedirection(1j*direction,self.jumpdistance)
        wire(direction, L, self.widthoverlap)
        movedirection(-1j*direction,self.jumpdistance*2,)
        wire(direction, L, self.widthoverlap)
        movedirection(1j*direction,self.jumpdistance)
        super(Microstrip_burried, self).wire(direction, L, **kwargs)
        return direction

    def up(self, direction, R):
        if R == -1:
            R = self.R
        layername(self.linelayer)
        turnup(direction, R, self.line, self.mesh)
        layername(self.diellayer)
        wire(direction, R+self.dielextension+self.line/2,self.dielwidth)
        setmark('up_start')
        movedirection(direction*-1j,self.jumpdistance)
        layername(self.linelayer)
        wirego(direction, R+self.dielextension+self.line/2+self.widthextension,self.widthoverlap)
        movedirection(-direction, self.widthoverlap/2)
        wirego(direction*1j, R+self.dielextension+self.line/2+self.widthextension,self.widthoverlap)
        gomark('up_start')

    def down(self, direction, R):
        if R == -1:
            R = self.R
        layername(self.linelayer)
        turndown(direction, R, self.line, self.mesh)
        layername(self.diellayer)
        wire(direction, R+self.dielextension+self.line/2,self.dielwidth)
        setmark('down_start')
        movedirection(direction*1j,self.jumpdistance)
        layername(self.linelayer)
        wirego(direction, R+self.dielextension+self.line/2+self.widthextension,self.widthoverlap)
        movedirection(-direction, self.widthoverlap/2)
        wirego(direction*-1j, R+self.dielextension+self.line/2+self.widthextension,self.widthoverlap)
        gomark('down_start')


    def end_open(self, direction, dielectric_length = -1):
        direction = self.process_direction(direction)
        if dielectric_length == -1:
            dielectric_length = self.dielextension
        super(Microstrip_burried, self).end_open(direction, self.coverextension)

    def copy(self, **kwargs):
        """
        WARNING: NOT FULLY IMPLEMENTED
        """
        line = kwargs.pop('line' , self.line)
        return Microstrip_burried(line, self.dielextension, self.widthextension, self.widthoverlap, self.linelayer, self.diellayer, self.mesh, self.coverlayer, self.coverextension)

    def coupler(self, line_old, width_overlap):
        """
        WARNING: TRAIL AND ERROR BY KEVIN
        """

        diff_line = (width_overlap-line_old)/2
        die_ext = (self.dielextension - diff_line)
        cover_ext = self.coverextension - diff_line
        return Microstrip_burried(width_overlap, die_ext, self.widthextension, self.widthoverlap, self.linelayer, self.diellayer, self.mesh, self.coverlayer, cover_ext)


class Microstrip_burried_KID(Microstrip):
    def __init__(self, line, dielextension, widthextension, widthoverlap, linelayer, diellayer, mesh, coverlayer, coverextension, R = 0):
        """
        This is a class for a burried microstrip line with an extra section of NbTiN for better adhesion of the aSi layer.
        WARNING: NOT ALL MICROSTRIP FUNCTIONS HAVE BEEN OVERWRITTEN WITH COVERLAYER
        """
        super(Microstrip_burried_KID, self).__init__(line, dielextension, linelayer, diellayer, mesh, R = R)
        self.type = 'microstrip buried kid'
        self.widthoverlap = widthoverlap
        self.widthextension = widthextension
        self.coverlayer = coverlayer
        self.coverextension = coverextension
        self.coverwidth = 2*coverextension + self.line
        self.jumpdistance = dielextension + widthextension - widthoverlap/2 + self.line/2

    def wire(self, direction, L, **kwargs):
        direction = self.process_direction(direction)
        #layername(self.coverlayer)
        #wire(direction, L, self.coverwidth)
        setmark('MS_KID_ad')
        layername(self.linelayer)
        movedirection(-1j*direction,self.jumpdistance)
        movedirection(-1*direction,self.dielextension+self.widthoverlap/2)
        wire(direction, L + 2*self.dielextension+self.widthoverlap, self.widthoverlap)
        gomark('MS_KID_ad')
        super(Microstrip_burried_KID, self).wire(direction, L, **kwargs)
        return direction

    def end_open(self, direction, dielectric_length = -1):
        direction = self.process_direction(direction)
        if dielectric_length == -1:
            dielectric_length = self.dielextension
        super(Microstrip_burried_KID, self).end_open(direction, dielectric_length)

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

