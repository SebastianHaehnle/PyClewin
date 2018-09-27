# -*- coding: utf-8 -*-
"""
Created on Fri Sep 09 10:08:12 2016

@author: sebastian
"""

from ..script import *
from ..base import *
import numpy as np

def wirehollow(direction, L, w, t_border):
    rot(direction)
    wirego(1j, w/2, t_border)
    wirego(1, L, t_border)
    wirego(-1j, w, t_border)
    wirego(-1, L, t_border)
    wirego(1j, w/2, t_border)
    rot(np.conjugate(direction))

def makebar(L, W):
    xy = np.array([[-L/2., L/2., L/2., -L/2.], [-W/2., -W/2., W/2., W/2.]])
    return xy

def bar(direction, L, W, shift = (0,0)):
    rot(direction)
    poly(makebar(L, W), shift)
    rotback()


def circle(R):
    D = 2*R*gg.scale
    gg.w('R {:6.0f} {:6.0f} {:6.0f} '.format(D, *gg.position))
    gg.nl()

def square(L, shift = (0,0)):
    poly(makebar(L, L), shift)

def squares(layer, polygon, l_sq, d_sq, corner = 1):
    '''
    Fill polygon with squares
    input:
        layer : layername
        poly : polygon to be filled
        l_sq : square size
        d_sq : space between square
        corner : start corner (1: bot left, 2: bot right, 3: top right, 4: top left)
    '''
    polygon = np.array(polygon)
    xybl = np.array([polygon[0].min(), polygon[1].min()])
    xybr= np.array([polygon[0].max(), polygon[1].min()])
    xytl = np.array([polygon[0].max(), polygon[1].max()])
    xytr = np.array([polygon[0].min(), polygon[1].max()])

    lxbot = abs(xybr[0] - xybl[0])
    lxtop = abs(xytr[0] - xytl[0])
    lyleft = abs(xytl[1] - xybl[1])
    lyright = abs(xytr[1] - xybr[1])

    print 'FILLSQUARES\n\n\n\n'
    print lxbot, lxtop, lyleft, lyright
    minspace = 1.5*l_sq + d_sq
    shift0 = [0.5*l_sq, 0.5*l_sq]
    shift = [0.5*l_sq, 0.5*l_sq]
    if corner == 1:
        go(*xybl)
        square(l_sq, shift)
        shift[0] += l_sq + d_sq
        while(shift[1] + l_sq <= lyright):
            while(shift[0] + minspace <= lxtop):
                square(l_sq, shift)
                shift[0] += l_sq + d_sq
                print shift
            shift[1] += l_sq + d_sq
            shift[0] = shift0[0]
            print shift[1]

def squares_inverse(layer, W, H, l_sq, d_sq):
    '''
    draws a grid of inverse squares using current position as bottom left
        W --> extension to right
        H --> extension to top
    '''
    layername(layer)
    lunit = l_sq + d_sq
    Nsq_h = int(H/lunit)
    Nsq_w = int(W/lunit)
    edge_h = (H % lunit) /2. + d_sq/2.
    edge_w = (W % lunit) /2. + d_sq/2.
    for i in range(Nsq_w):
        shift = (0, -(edge_w + i*lunit))
        wire(1j, H, d_sq, shift)
    for i in range(Nsq_h):
        shift = (0, edge_h + i*lunit)
        wire(1, W, d_sq, shift)

### Probably not in use
class clePolygon(object):
    def __init__(self, *args, **kwargs):
        """
        Input: each point in polygon as [x, y, bool], where bool = True for concave position (inner corner) and bool = False for convex position (outer corner)
        """
        self.points = np.array([ip[:2] for ip in args])
        self.is_concave = np.array([ip[2] for ip in args])

        self.xlim = kwargs.pop('xlim', [None, None])
        self.ylim = kwargs.pop('ylim', [None, None])

    @property
    def length(self):
        return len(self.points)

    def draw(self):
        poly(self.points.transpose())

    def scale(self, delta, **kwargs):
        """
        not multiplicative scale but increase whole polygon size
        Returns new Polygon instance
        """
        self.xlim = kwargs.pop('xlim', self.xlim)
        self.ylim = kwargs.pop('ylim', self.ylim)
        newPoints = np.zeros(self.points.shape)
        for i in xrange(self.length):
            newPoints[i] = self.points[i] + delta*self._direction[i]
        # Check for boundarys of drawrange
        newPoints = newPoints.transpose()
        if self.xlim[0] == None:
            self.xlim[0] = min(newPoints[0])
        if self.xlim[1] == None:
            self.xlim[1] = max(newPoints[0])
        newPoints[0] = np.clip(newPoints[0], *self.xlim)
        if self.ylim[0] == None:
            self.ylim[0] = min(newPoints[1])
        if self.ylim[1] == None:
            self.ylim[1] = max(newPoints[1])
        newPoints[1] = np.clip(newPoints[1], *self.ylim)
        newPoints = np.vstack((newPoints, self.is_concave)).transpose()
        return clePolygon(*newPoints)


    @property
    def _direction(self):
        retValue = np.zeros(self.points.shape)
        for i in xrange(self.length):
            if i == 0:
                il = self.length-1
                ir = i+1
            elif i == self.length-1:
                il = i-1
                ir = 0
            else:
                il = i-1
                ir = i+1
            del_l = np.sign(self.points[il] - self.points[i])
            del_r = np.sign(self.points[ir] - self.points[i])
            retValue[i] = np.sign(del_l + del_r)
            if not self.is_concave[i]:
                retValue[i] = retValue[i] * -1
        return retValue


