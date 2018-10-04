# -*- coding: utf-8 -*-
"""
Created on Fri Jan 06 15:22:42 2017

@author: sebastian
"""

from PyClewin import *
#from PyClewin.base import *

import numpy as np
import scipy.constants as spc

class CPW(object):
    '''
    Simple single layer CPW, drawn in negative.
    Input:
        line    :: width of central line
        gap     :: width of gap between line and gnd
        mesh    :: resolution of polygon used for corners
    Functions:
        wire    :: draws straight CPW
        up      :: draws upward 90degree CPW
        down    :: draws downward 90degree CPW
        taper   :: draws tapered section
        [fct]go :: calls draw function and moves coordinate system to end of line
    '''
    def __init__(self, line, gap, mesh, R, gndlayer, **kwargs):
        self.line = line
        self.gap = gap
        self.mesh = mesh
        self.R = R
        self.direction = 1
        self.used_wires = []
#        print kwargs
        self.gndlayer = gndlayer
        self.bridge = kwargs.pop('bridge', None)
        self.tm_type = 'cpw'

    @property
    def slot(self):
        return self.gap

    @property
    def wTotal(self):
        return self.line + 2*self.gap

    def process_direction(self, direction):
        if direction == None or direction == 0:
            direction = self.direction
        else:
            self.direction = direction
        return direction

    def generate_covered(self, coverlayer, coverwidth):
        return CPWcovered(self.line, self.gap, self.mesh, self.R, self.gndlayer, coverlayer, coverwidth)

    def taper(self, direction, L, newline, newgap):
        """
        info
        """
        if direction == None or direction == 0:
            direction = self.direction
        layername(self.gndlayer)
        xy1 = np.array([[0, 0, L, L], [self.line/2., self.wTotal/2., newgap + newline/2., newline/2.]])
        rot(direction)
        poly(xy1)
        xy1[1] = -1*xy1[1]
        poly(xy1)
        rotback()
        return direction

    def tapergo(self, direction, L, newline, newgap):
        if direction == None or direction == 0:
            direction = self.direction
        else:
            self.direction = direction
        self.taper(direction, L, newline, newgap)
        rot(direction)
        go(float(L), 0)
        rotback()
        return direction

    def wire(self, direction, L, *args, **kwargs):
        if direction == None or direction == 0:
            direction = self.direction
        # set correct layername, but only if really set
#        try:
        layername(self.gndlayer)
#        except:
#            pass
        wire(direction, float(L), self.gap, (0,(self.line+self.gap)/2.))
        wire(direction, float(L), self.gap, (0,-(self.line+self.gap)/2.))
        return direction

    def wirego(self, direction, L, *args, **kwargs):
        if direction == None or direction == 0:
            direction = self.direction
        else:
            self.direction = direction
        self.wire(direction, L, *args, **kwargs)
        rot(direction)
        go(float(L), 0)
        rotback()
        self.used_wires.append([direction, L, self.direction])
        return direction

    def up(self, direction, R = -1, *args, **kwargs):
        if direction == None or direction == 0:
            direction = self.direction
        if R == -1:
            R = self.R
        rot(direction)
    #    inner gap
        go(0, +(self.gap+self.line)/2.)
        poly(makeTurn(R-(self.gap+self.line)/2., self.gap, self.mesh, np.pi/2.))
    #    outer gap
        go(0, -(self.gap+self.line))
        poly(makeTurn(R+(self.gap+self.line)/2., self.gap, self.mesh, np.pi/2.))
        go(0, +(self.gap+self.line)/2.)
        rotback()
        return direction

    def upgo(self, direction, R = -1, *args, **kwargs):
        if direction == None or direction == 0:
            direction = self.direction
        else:
            self.direction = direction
        if R == -1:
            R = self.R
        self.up(direction, R, *args, **kwargs)
        rot(direction)
        go(R,R)
        rotback()
        direction_out = np.exp(1j*(np.angle(direction) + np.pi/2.))
        self.direction = direction_out
        return direction_out

    def down(self, direction, R = -1, *args, **kwargs):
        if direction == None or direction == 0:
            direction = self.direction
        if R == -1:
            R = self.R
        rot(direction)
    #    inner gap
        go(0, -(self.gap+self.line)/2.)
        poly(makeTurn(R-(self.gap+self.line)/2., self.gap, self.mesh, -np.pi/2.))
    #    outer gap
        go(0, +(self.gap+self.line))
        poly(makeTurn(R+(self.gap+self.line)/2., self.gap, self.mesh, -np.pi/2.))
        go(0, -(self.gap+self.line)/2.)
        rotback()
        return direction

    def downgo(self, direction, R = -1, *args, **kwargs):
        if direction == None or direction == 0:
            direction = self.direction
        else:
            self.direction = direction
        if R == -1:
            R = self.R
        self.down(direction, R, *args, **kwargs)
        rot(direction)
        go(R,-R)
        rotback()
        direction_out = np.exp(1j*(np.angle(direction) - np.pi/2.))
        self.direction = direction_out
        return direction_out

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
        self.used_wires.append([direction_out, self.R, direction_in])
        return direction_out


    def open_end(self, direction, *args, **kwargs):
        """
        kwargs:
            l_open : length of gap, default = wTotal
        """
        if direction == None or direction == 0:
            direction = self.direction
        else:
            self.direction = direction
        base.layername(self.gndlayer)
        rot(direction)
        base.wire(direction, kwargs.pop('l_open', self.wTotal), self.wTotal)
        rot(np.conjugate(direction))
        return direction


    def connect(self, connection, *args, **kwargs):
        print "connecting", connection.mark
        distance = base.dist2markSigned(connection.mark)
        direction_in = np.array([self.direction.real, self.direction.imag])
        direction_out = np.array([connection.direction.real, connection.direction.imag])
        dir_in = self.direction
        self.used_wires = []
        if self.direction == connection.direction:
            print 'c1'
            ### Same direction
            l_1 = np.dot(direction_in, distance)
            l_2 = np.dot(direction_in[::-1], distance)
            if l_2 == 0:
                # No turns required (same height)
                self.wirego(0, l_1)
            elif abs(l_2) >= 2*self.R:
                if kwargs.pop('turn_start', True): # Default does the curves immediately, then attaches x-length
                    # Enough y-space for 2 turns to correct for different height
                    self.turngo(0, self.direction*np.sign(l_2)*1j)
                    self.wirego(0, abs(l_2) - 2*self.R)
                    self.turngo(0, -self.direction*np.sign(l_2)*1j)
                    self.wirego(0, abs(l_1) - 2*self.R)
                else:
                    # Non default: pass kwarg "turn_start=False" in fct call
                    self.wirego(0, abs(l_1) - 2*self.R)
                    self.turngo(0, self.direction*np.sign(l_2)*1j)
                    self.wirego(0, abs(l_2) - 2*self.R)
                    self.turngo(0, -self.direction*np.sign(l_2)*1j)

            else:
                # y-space < 2*turn radius --> requires more elaborate s-shape
                self.turngo(0, self.direction*np.sign(l_2)*1j)
                self.wirego(0, abs(l_2))
                self.turngo(0, -self.direction*np.sign(l_2)*1j)
                self.turngo(0, -self.direction*np.sign(l_2)*1j)
#                self.wirego(0, abs(l_2))
                self.turngo(0, self.direction*np.sign(l_2)*1j)
                self.wirego(0, abs(l_1) - 2*self.R)

        elif self.direction == -connection.direction:
            print 'c2'
            ### Opposite direction (needs u-turn)
            l_1 = np.dot(direction_in, distance)
            l_2 = np.dot(direction_in[::-1], distance)
            if abs(l_2) >= 2*self.R:
                if l_1 >= 0:
                    self.wirego(0, abs(l_1))
                    self.turngo(0, self.direction*np.sign(l_2)*1j)
                    self.wirego(0, abs(l_2) - 2*self.R)
                    self.turngo(0, self.direction*np.sign(l_2)*1j)
                else:
                    self.turngo(0, self.direction*np.sign(l_2)*1j)
                    self.wirego(0, abs(l_2) - 2*self.R)
                    self.turngo(0, self.direction*np.sign(l_2)*1j)
                    self.wirego(0, abs(l_1))
            else:
                print "WARNING: INPUT AND OUTPUT CONNECTION TO INCOMPATIBLE FOR AUTOCONNECT"
        else:
            print 'c3'
            ### 90 degree connection
            l_1 =  np.dot(direction_in, distance)
            l_2 =  np.dot(direction_out, distance)
            print l_1, l_2, self.R, self.direction, connection.direction
            if np.sign(l_1) >= 0:
                print 'c31'
                self.wirego(0, np.abs(l_1)-self.R)
                self.turngo(0, connection.direction)
                self.wirego(0, np.abs(l_2) - self.R)
            else:
                print 'c32'
                self.turngo(dir_in, connection.direction)
                self.turngo(0, -dir_in)
                self.wirego(0, np.abs(l_1) - self.R)
                self.turngo(0, connection.direction)
                self.wirego(0, np.abs(l_2) - 3*self.R)

        return self.direction



class CPWhybrid(CPW):
    '''
    Hybrid CPW, standard format for hybrid KIDS. Line material drawn positive in linelayer, gap material drawn negative in gaplayer
    '''
    def __init__(self, line, gap, linelayer, gndlayer, mesh, R):
        CPW.__init__(self, line, gap, mesh, R, gndlayer)
        self.linelayer = linelayer
        self.gndlayer = gndlayer

    def taper(self, direction, L, newline, newgap):
        if direction == None or direction == 0:
            direction = self.direction
        rot(direction)
        xyline = np.array([[0,0, L, L], [-self.gap/2., self.gap/2., newgap/2., -newgap/2.]])
        xygap = np.array([[0,0, L, L],[-self.wTotal()/2., self.wTotal()/2., newgap + newline/2., newgap + newline/2.]])
        layername(self.linelayer)
        poly(xyline)
        layername(self.gndlayer)
        poly(xygap)
        rotback()
        return direction

    def wire(self, direction, L):
        if direction == None or direction == 0:
            direction = self.direction
        layername(self.linelayer)
        wire(direction, float(L), self.line)
        layername(self.gndlayer)
        wire(direction, float(L), self.wTotal)
        return direction

    def up(self, direction, R = -1):
        if direction == None or direction == 0:
            direction = self.direction
        else:
            self.direction = direction
        if R == -1:
            R = self.R
        layername(self.linelayer)
        turnup(direction, R, self.line, self.mesh)
        layername(self.gndlayer)
        turnup(direction, R, self.wTotal, self.mesh)
        return direction

    def down(self, direction, R = -1):
        if direction == None or direction == 0:
            direction = self.direction
        else:
            self.direction = direction
        if R == -1:
            R = self.R
        layername(self.linelayer)
        turndown(direction, R, self.line, self.mesh)
        layername(self.gndlayer)
        turndown(direction, R, self.wTotal, self.mesh)
        return direction

class CPWwithBridge(CPW):
    def __init__(self, line, gap, mesh, R, cpwlayer, bridgeClass, bridgeDistance):
        CPW.__init__(self, line, gap, mesh, R, cpwlayer)
        self.cpwlayer = cpwlayer                # layer of cpw
        self.bridgeClass = bridgeClass              # Instance of parts.Bridges.Bridge
        self.bridgeDistance = bridgeDistance    # Distance between bridges

    def wire(self, direction, L, bridgeDistance = None, bridgesOff = False, bridgeStart = False, **kwargs):
        if direction == None or direction == 0:
            direction = self.direction
        bridgePositions = kwargs.pop('bridgePositions', [])
        # no manual bridge Positions and bridges are on
        if bridgePositions == [] and not bridgesOff:
            # manual distance given?
            if not bridgeDistance:
                bridgeDistance = self.bridgeDistance
            # bridge at start?
            if bridgeStart:
                bridgePositions.append(0)
            newPos = bridgeDistance
            while newPos <= L:
                bridgePositions.append(newPos)
                newPos += bridgeDistance
        setmark('cpwlevel')
        # draw bridges first:
        for pos in bridgePositions:
            gomark('cpwlevel')
            base.movedirection(direction, pos)
            self.bridgeClass.draw(direction, self.line, self.gap)
        gomark('cpwlevel')
        layername(self.cpwlayer)
        super(CPWwithBridge, self).wire(direction, L)
        delmark('cpwlevel')
        return direction

    def up(self, direction, R = -1, bridgeFront = True, bridgeAfter = True, **kwargs):
        if direction == None or direction == 0:
            direction = self.direction
        else:
            self.direction = direction
        if R == -1:
            R = self.R
        setmark('cpwlevel')
        rot(direction)
        if bridgeFront:
            self.bridgeClass.draw(1, self.line, self.gap)
        layername(self.cpwlayer)
        super(CPWwithBridge, self).up(1, R)
        if bridgeAfter:
            go(R,R)
            self.bridgeClass.draw(1j, self.line, self.gap)
        gomark('cpwlevel')
        delmark('cpwlevel')
        return direction

    def down(self, direction, R = -1, bridgeFront = True, bridgeAfter = True, **kwargs):
        if direction == None or direction == 0:
            direction = self.direction
        else:
            self.direction = direction
        if R == -1:
            R = self.R
        setmark('cpwlevel')
        rot(direction)
        if bridgeFront:
            self.bridgeClass.draw(1, self.line, self.gap)
        layername(self.cpwlayer)
        super(CPWwithBridge, self).down(1, R)
        if bridgeAfter:
            go(R,-R)
            self.bridgeClass.draw(-1j, self.line, self.gap)
        gomark('cpwlevel')
        delmark('cpwlevel')
        return direction

class CPWreadout(CPWwithBridge):
    """
    CPW with bridges and SiN below central line. Standardformat for MSLOC type.
    Default width of SiN: sinwidth = line + gap (until center of gap)
    """
    def __init__(self, line, gap, mesh, R, cpwlayer, diellayer, bridgeClass, bridgeDistance ):
        CPWwithBridge.__init__(self, line, gap, mesh, R, cpwlayer, bridgeClass, bridgeDistance )
        self.diellayer = diellayer
        self.sinwidth = self.line + self.gap

    def taper(self, direction, L, newline, newgap):
        if direction == None or direction == 0:
            direction = self.direction
        else:
            self.direction = direction
        layername(self.cpwlayer)
        super(CPWreadout, self).taper(direction, L, newline, newgap)
        return direction


    def wire(self, direction, L, bridgeDistance = None, bridgesOff = False, **kwargs):
        if direction == None or direction == 0:
            direction = self.direction
        else:
            self.direction = direction
        layername(self.diellayer)
        wire(direction, L, self.sinwidth)
        super(CPWreadout, self).wire(direction, L, bridgeDistance, bridgesOff, **kwargs)
        return direction

    def up(self, direction, R = -1, bridgeFront = True, bridgeAfter = True, **kwargs):
        if direction == None or direction == 0:
            direction = self.direction
        else:
            self.direction = direction
        if R == -1:
            R = self.R
        layername(self.diellayer)
        turnup(direction, R, self.sinwidth, self.mesh)
        super(CPWreadout, self).up(direction, R, bridgeFront, bridgeAfter, **kwargs)
        return direction

    def down(self, direction, R = -1, bridgeFront = True, bridgeAfter = True, **kwargs):
        if direction == None or direction == 0:
            direction = self.direction
        else:
            self.direction = direction
        if R == -1:
            R = self.R
        layername(self.diellayer)
        turndown(direction, R, self.sinwidth, self.mesh)
        super(CPWreadout, self).down(direction, R, bridgeFront, bridgeAfter, **kwargs)
        return direction

#    def turn(self, direction_in, direction_out, R = -1, bridgeFront = True, bridgeAfter = True, **kwargs):
#        if direction_in == None or direction_in == 0:
#            direction_in = self.direction
#        if R == -1:
#            R = self.R

class CPWcovered(CPW):
    def __init__(self, line, gap, mesh, R, gndlayer, coverlayer, coverextension):
        CPW.__init__(self, line, gap, mesh, R, gndlayer)
        self.coverlayer = coverlayer
        self.coverextension = coverextension
        self.coverwidth = self.line + 2*self.slot + 2*coverextension



    def wire(self, direction, L, *args, **kwargs):
        self.process_direction(direction)
        layername(self.coverlayer)
        wire(direction, L, self.coverwidth)
        super(CPWcovered, self).wire(direction, L, *args, **kwargs)
        return direction

    def up(self, direction, R = -1, *args, **kwargs):
        self.process_direction(direction)
        if R == -1:
            R = self.R
        layername(self.coverlayer)
        wire(direction, R + self.coverwidth, self.coverwidth)
        super(CPWcovered, self).up(direction, R, *args, **kwargs)
        return direction

    def down(self, direction, R = -1, *args, **kwargs):
        self.process_direction(direction)
        if R == -1:
            R = self.R
        layername(self.coverlayer)
        wire(direction, R + self.coverwidth, self.coverwidth)
        super(CPWcovered, self).down(direction, R, *args, **kwargs)
        return direction





