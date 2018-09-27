# -*- coding: utf-8 -*-
"""
Created on Mon Sep 05 11:48:19 2016

@author: sebastian
"""

from ..script import *
import numpy as np
import collections

def setmark(name):
    gg.setmark(name)

def gomark(name):
    gg.gomark(name)

def delmark(name):
    gg.delmark(name)

def xymark(name):
    return gg.mark(name)[0]

def dist2mark(name):
    return gg.dist2mark(name)

def dist2markSigned(name):
    return gg.dist2markSigned(name)

def dist2markSigned_complex(name):
    return gg.dist2markSigned_complex(name)

def dist_marktomark(name_1, name_2):
    x1, y1 = dist2markSigned(name_1)
    x2, y2 = dist2markSigned(name_2)
    return np.array([x2-x1, y2-y1])

def x2m(name):
    return gg.dist2mark(name)[0]

def y2m(name):
    return gg.dist2mark(name)[1]

def x2mSigned(name):
    return gg.dist2markSigned(name)[0]

def y2mSigned(name):
    return gg.dist2markSigned(name)[1]


def go(x,y):
    gg.go(x,y)

def movedirection(direction, distance):
    complex_move = direction*distance
    gg.go(complex_move.real, complex_move.imag)

def moveto(x,y):
    gg.cle = np.array([x,y])

def rot(direction):
    gg.angle += np.angle(direction)
    gg.back = -np.angle(direction)
    gg.rotator = gg.rotator.dot(gg.rotation(np.angle(direction)))


def rotback():
    gg.angle += gg.back
    gg.rotator = gg.rotator.dot(gg.rotation(gg.back))

def flip(axis):
    gg.flip_axis(axis)

connector = collections.namedtuple('connector', ['direction', 'mark'])

def set_connector(name, connector):
    gg.connectors[name] = connector

def get_connector(name):
    return gg.connectors[name]


def cornerDirection(dir_in, dir_out):
    """
    output:
        positive if left turn
        negative if right turn
    """
#    dir_in = complex(dir_in)
#    dir_out = complex(dir_out)
    return np.sign(np.cross((dir_in.real, dir_in.imag), (dir_out.real, dir_out.imag)))

