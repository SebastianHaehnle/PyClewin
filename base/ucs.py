# -*- coding: utf-8 -*-
"""
Created on Mon Sep 05 11:48:19 2016

@author: sebastian
"""

from ..script import *
import numpy as np
import collections

def setmark(name):
    """
    Generate and save a marker at current UCS location.
    
    Parameters
    --------
    name : str
        Markername, use this string to recall this marker later.
    """
    gg.setmark(name)

def gomark(name):
    """
    Move UCS to marker given by name string.
    """
    gg.gomark(name)

def delmark(name):
    """
    Remove marker given by name string.
    """
    gg.delmark(name)

def xymark(name):
    return gg.mark(name)[0]

def dist2mark(name):
    """
    Returns [abs(x),abs(y)] of given marker relative to current UCS origin
    """
    return gg.dist2mark(name)

def dist2markSigned(name):
    """
    Returns [x,y] of given marker relative to current UCS origin
    """
    return gg.dist2markSigned(name)

def dist2markSigned_complex(name):
    """
    Returns x+1j*y of given marker relative to current UCS origin
    """
    return gg.dist2markSigned_complex(name)

def dist_marktomark(name_1, name_2):
    """
    Returns [x2-x1,y2-y1] for two given markers
    """
    x1, y1 = dist2markSigned(name_1)
    x2, y2 = dist2markSigned(name_2)
    return np.array([x2-x1, y2-y1])

def x2m(name):
    """
    Return x-distance of marker relative to current UCS origin
    """
    return gg.dist2mark(name)[0]

def y2m(name):    
    """
    Return y-distance of marker relative to current UCS origin
    """
    return gg.dist2mark(name)[1]

def x2mSigned(name):
    """
    Return x-location (i.e. including sign) of marker relative to current UCS origin
    """
    return gg.dist2markSigned(name)[0]

def y2mSigned(name):
    """
    Return y-location (i.e. including sign) of marker relative to current UCS origin
    """
    return gg.dist2markSigned(name)[1]


def go(x,y):
    """
    Move UCS origin by (x,y)
    """
    gg.go(x,y)

def movedirection(direction, distance):
    """
    Move UCS origin by distance along direction.
    
    Parameters
    --------
    direction : complex float
        Direction of movement in complex plane. WARNING: IS NOT NORMALIZED INTERNALLY!
    distance : float
        Magnitude of movement in complex plane. WARNING: DIRECTION NOT NECESSARILY UNIT VECTOR
    """
    complex_move = direction*distance
    gg.go(complex_move.real, complex_move.imag)

def moveto(x,y):
    """
    USE ONLY IF YOU KNOW WHAT YOU ARE DOING.
    Moves UCS origin to an arbitrary location in the global coordinate system.
    """
    gg.cle = np.array([float(x),float(y)])

def rot(direction):
    """
    Rotate coordinate system so that the x-axis aligns with the given direction.
    Can be reversed by calling rotback() later.
    """
    gg.angle += np.angle(direction)
    gg.back = -np.angle(direction)
    gg.rotator = gg.rotator.dot(gg.rotation(np.angle(direction)))


def rotback():
    """
    Reverses previous rotation
    """
    gg.angle += gg.back
    gg.rotator = gg.rotator.dot(gg.rotation(gg.back))

def flip(axis):
    """
    """
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

