# -*- coding: utf-8 -*-
"""
Created on Mon Sep 05 11:20:33 2016

@author: sebastian
"""

import numpy as np
import numpy.linalg as nplin
from copy import *
import collections

npa = np.array

class script():
    def __init__(self):
        self.s = ''
        self.scale = 1e3
        self.cle = np.array([0., 0.])
        self.cle_complex = self.cle[0] + 1j*self.cle[1]
        self.angle = 0.
        self.back = 0.
        self.mark = collections.OrderedDict()
        self.symbol = collections.OrderedDict()
        self._flip = np.array([[1.,0.],[0.,1.]])
        self.flip = np.diag(self._flip)
        self.layers = collections.OrderedDict()
        self.rotator = self.unitmat
        self.current_layer = None

        self.connectors = {}

    @property
    def position(self):
        return self.cle*self.scale

    @property
    def position_complex(self):
        return self.position[0] + 1j*self.position[1]

    @property
    def unitmat(self):
        return npa(([1,0], [0,1]))

    def rotation(self, angle):
        return npa([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])


    @property
    def rotator(self):
        return self.rotator

    @rotator.setter
    def rotator(self, matrix):
        self._rotator = matrix

    @property
    def flipper(self):
        return self._flip

    def w(self, st):
        self.s += st

    def nl(self):
        self.s += ';\n'

    def go(self, x,y):
        '''
        Moves clewin coordinates by amounts x and y
        '''
#        x,y = self.to_clewin(x,y)
#        self.cle[0] += x*self.flip[0]
#        self.cle[1] += y*self.flip[1]
        self.cle += self.rotator.dot(npa([x,y]))

    def moveto(self, x, y):
#        x, y = self.to_clewin(x, y)
#        self.cle[0] = x*self.flip[0]
#        self.cle[1] = y*self.flip[1]
        self.cle = self.rotator.dot(npa([x,y]))

    def flip_axis(self, axis):
        '''
        flips specified axis. e.g. for axis = 'x' all x-values get multiplied by -1
        '''
        if axis == 'x':
            flipper = npa([[-1., 0.],[0., 1.]])
            self._flip = flipper.dot(self._flip)
            self.flip = np.diag(self._flip)
        elif axis == 'y':
            flipper = npa([[1., 0.],[0., -1.]])
            self._flip = flipper.dot(self._flip)
            self.flip = np.diag(self._flip)
        else:
            print 'invalid input for flip command'
        self.rotator = self.rotator.dot(flipper)

    def to_clewin(self, x,y):
        xyvec = npa([x, y])
        newxy = self.rotator.dot(xyvec)
        return newxy[0], newxy[1]

    def proj(self, x, y):
        '''
        get from ucs to clewin coordinates
        '''
        newxy = self.rotator.dot(npa([x, y]))
        return (self.cle[0] + newxy[0])*self.scale, (self.cle[1] + newxy[1])*self.scale


    def to_ucs(self, x, y):
        newxy = nplin.inv(self.rotator).dot(npa([x-self.cle[0],y-self.cle[1]]))
        newx = newxy[0]
        newy = newxy[1]
        return newx, newy

    def setmark(self, name):
        self.mark[name] = (deepcopy(self.cle), deepcopy(self.rotator))


    def delmark(self, name):
        self.mark.pop(name, True)

    def gomark(self, name):
        self.cle, self.rotator = deepcopy(self.mark[name])

    def dist2mark(self, name):
        x, y = gg.mark[name][0]
        newx, newy = self.to_ucs(x, y)
        return abs(newx), abs(newy)

    def dist2markSigned(self, name):
        x, y = gg.mark[name][0]
        newx, newy = self.to_ucs(x, y)
        return newx, newy

    def dist2markSigned_complex(self, name):
        x, y = self.dist2markSigned(name)
        return x + 1j*y

    def reset(self):
        self.s = ''
        self.scale = 1e3
        self.cle = np.array([0., 0.])
        self.cle_complex = self.cle[0] + 1j*self.cle[1]
        self.angle = 0.
        self.back = 0.
        self.mark = collections.OrderedDict()
        self.symbol = collections.OrderedDict()
        self._flip = np.array([[1.,0.],[0.,1.]])
        self.flip = np.diag(self._flip)
        self.layers = collections.OrderedDict()
        self.rotator = self.unitmat
        self.current_layer = None

        self.connectors = {}




global gg
gg = script()