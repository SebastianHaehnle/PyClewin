# -*- coding: utf-8 -*-
"""
Created on Fri Jan 06 15:22:42 2017

@author: sebastian
"""

from clepywin import *

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
    def __init__(self, line, gap, mesh, **kwargs):
        self.line = line
        self.gap = gap
        self.mesh = mesh
#        print kwargs
        try:
            self.gndlayer = kwargs.pop('gndlayer')
        except:
            pass    
    
    def wTotal(self):
        return self.line + 2*self.gap
        
    def taper(self, direction, L, newline, newgap):
        xy1 = np.array([[0, 0, L, L], [self.line/2., self.wTotal()/2., newgap + newline/2., newline/2.]])
        rot(direction)
        poly(xy1)
        xy1[1] = -1*xy1[1]
        poly(xy1)
        rotback()
    
    def tapergo(self, direction, L, newline, newgap):
        self.taper(direction, L, newline, newgap)
        rot(direction)
        go(float(L), 0)
        rotback()
        
    def wire(self, direction, L):
        wire(direction, float(L), self.gap, (0,(self.line+self.gap)/2.))
        wire(direction, float(L), self.gap, (0,-(self.line+self.gap)/2.))
        
    def wirego(self, direction, L, *args, **kwargs):
        self.wire(direction, L, *args, **kwargs)
        rot(direction)
        go(float(L), 0)
        rotback()
    
    def up(self, direction, R, *args, **kwargs):
        rot(direction)
    #    inner gap
        go(0, +(self.gap+self.line)/2.)
        poly(makeTurn(R-(self.gap+self.line)/2., self.gap, self.mesh, np.pi/2.))
    #    outer gap
        go(0, -(self.gap+self.line))
        poly(makeTurn(R+(self.gap+self.line)/2., self.gap, self.mesh, np.pi/2.))
        go(0, +(self.gap+self.line)/2.)        
        rotback()
        
    def upgo(self, direction, R, *args, **kwargs):
        self.up(direction, R, *args, **kwargs)
        rot(direction)
        go(R,R)
        rotback()
        
    def down(self, direction, R):
        rot(direction)
    #    inner gap
        go(0, -(self.gap+self.line)/2.)
        poly(makeTurn(R-(self.gap+self.line)/2., self.gap, self.mesh, -np.pi/2.))
    #    outer gap
        go(0, +(self.gap+self.line))
        poly(makeTurn(R+(self.gap+self.line)/2., self.gap, self.mesh, -np.pi/2.))
        go(0, -(self.gap+self.line)/2.)        
        rotback()
        
    def downgo(self, direction, R, *args, **kwargs):
        self.down(direction, R, *args, **kwargs)
        rot(direction)
        go(R,-R)
        rotback()

class CPWhybrid(CPW):
    '''
    Hybrid CPW, standard format for hybrid KIDS. Line material drawn positive in linelayer, gap material drawn negative in gaplayer
    '''
    def __init__(self, line, gap, linelayer, gndlayer, mesh):
        CPW.__init__(self, line, gap, mesh)
        self.linelayer = linelayer
        self.gndlayer = gndlayer
        
    def taper(self, direction, L, newline, newgap):
        rot(direction)
        xyline = np.array([[0,0, L, L], [-self.gap/2., self.gap/2., newgap/2., -newgap/2.]])
        xygap = np.array([[0,0, L, L],[-self.wTotal()/2., self.wTotal()/2., newgap + newline/2., newgap + newline/2.]])
        layername(self.linelayer)
        poly(xyline)
        layername(self.gndlayer)
        poly(xygap)
        rotback()
        
    def wire(self, direction, L):
        layername(self.linelayer)
        wire(direction, float(L), self.line)
        layername(self.gndlayer)
        wire(direction, float(L), self.wTotal())
        
    def up(self, direction, R):
        layername(self.linelayer)
        turnup(direction, R, self.line, self.mesh)
        layername(self.gndlayer)
        turnup(direction, R, self.wTotal(), self.mesh)
        
    def down(self, direction, R):
        layername(self.linelayer)
        turndown(direction, R, self.line, self.mesh)
        layername(self.gndlayer)
        turndown(direction, R, self.wTotal(), self.mesh)
        
        
        
class CPWwithBridge(CPW):
    def __init__(self, line, gap, cpwlayer, bridgefun, bridgeDistance, mesh):
        CPW.__init__(self, line, gap, mesh)
        self.cpwlayer = cpwlayer                # layer of cpw
        self.bridgefun = bridgefun              # function for bridge drawing
        self.bridgeDistance = bridgeDistance    # Distance between bridges
        
    def wire(self, direction, L, bridgeDistance = None, bridgesOff = False, bridgeStart = False, **kwargs):
        setmark('cpwlevel')
        rot(direction)
        layername(self.cpwlayer)
        if bridgeStart:
            if bridgesOff and bridgeDistance != None:
                go(bridgeDistance, 0)
                self.bridgefun(1, self.line, self.gap)
                layername(self.cpwlayer)
                go(-bridgeDistance, 0)
            else:
                self.bridgefun(1, self.line, self.gap)
                layername(self.cpwlayer)
        if not bridgeDistance:
            bridgeDistance = self.bridgeDistance
        if bridgesOff:
            pass
        else:
            for times in xrange(int(L/bridgeDistance)):
                super(CPWwithBridge, self).wire(1, bridgeDistance)
                go(bridgeDistance, 0)
                self.bridgefun(1, self.line, self.gap)
                layername(self.cpwlayer)
                L -= bridgeDistance
            layername(self.cpwlayer)
        super(CPWwithBridge, self).wire(1, L)
        gomark('cpwlevel')
        
    def up(self, direction, R, bridgeFront = True, bridgeAfter = True, **kwargs):
        setmark('cpwlevel')
        rot(direction)
        if bridgeFront:
            self.bridgefun(1, self.line, self.gap)
        layername(self.cpwlayer)
        super(CPWwithBridge, self).up(1, R)
        if bridgeAfter:
            go(R,R)
            self.bridgefun(1j, self.line, self.gap)
        gomark('cpwlevel')
        
    def down(self, direction, R, bridgeFront = True, bridgeAfter = True, **kwargs):
        setmark('cpwlevel')
        rot(direction)
        if bridgeFront:
            self.bridgefun(1, self.line, self.gap)
        layername(self.cpwlayer)
        super(CPWwithBridge, self).down(1, R)
        if bridgeAfter:
            go(R,-R)
            self.bridgefun(-1j, self.line, self.gap)
        gomark('cpwlevel')

class CPWreadout(CPWwithBridge):
    """
    CPW with bridges and SiN below central line. Standardformat for MSLOC type.
    Default width of SiN: sinwidth = line + gap (until center of gap)
    """
    def __init__(self, line, gap, cpwlayer, diellayer, bridgefun, bridgeDistance, mesh):
        CPWwithBridge.__init__(self, line, gap, cpwlayer, bridgefun, bridgeDistance, mesh)
        self.diellayer = diellayer
        self.sinwidth = self.line + self.gap
    
    def taper(self, direction, L, newline, newgap):
        layername(self.cpwlayer)
        super(CPWreadout, self).taper(direction, L, newline, newgap)
        
    def wire(self, direction, L, bridgeDistance = None, bridgesOff = False, **kwargs):
        layername(self.diellayer)
        wire(direction, L, self.sinwidth)
        super(CPWreadout, self).wire(direction, L, bridgeDistance, bridgesOff, **kwargs)
        
    def up(self, direction, R, bridgeFront = True, bridgeAfter = True, **kwargs):
        layername(self.diellayer)
        turnup(direction, R, self.sinwidth, self.mesh)
        super(CPWreadout, self).up(direction, R, bridgeFront, bridgeAfter, **kwargs)

    def down(self, direction, R, bridgeFront = True, bridgeAfter = True, **kwargs):
        layername(self.diellayer)
        turndown(direction, R, self.sinwidth, self.mesh)
        super(CPWreadout, self).down(direction, R, bridgeFront, bridgeAfter, **kwargs)
        
        

    
        