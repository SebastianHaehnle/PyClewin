# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 11:38:37 2017

@author: sebastian
"""

from PyClewin import *

import numpy as np

def alignmentCircles(layer):
    rS = 2.5
    rM = 5.
    rL = 20.

    directions = [1, 1j, -1, -1j]
    altpos = [210, -210]

    layername(layer)
    setmark('tempcenter')
    circle(rM)
    def crossline():
        for i in xrange(3):
            go(30, 0)
            circle(rM)
        go(50, 0)
        circle(rL)
        for i in xrange(2):
            go(70, 0)
            circle(rL)
        go(140, 0)
        circle(rL)
        for i in xrange(5):
            go(70, 0)
            circle(rL)
    for dd in directions:
        gomark('tempcenter')
        rot(dd)
        crossline()
        gomark
    gomark('tempcenter')

    def smallcross():
        setmark('temptempcenter')
        circle(rS)
        for dd in directions:
            gomark('temptempcenter')
            rot(dd)
            for i in xrange(3):
                go(10, 0)
                circle(rS)
            go(20, 0)
            circle(rS)
            for i in xrange(2):
                go(10, 0)
                circle(rS)
    for ix in altpos:
        for iy in altpos:
            gomark('tempcenter')
            go(ix, iy)
            smallcross()
    gomark('tempcenter')

def alignmentSquares(layer, name = None):
    dS = 5
    dM = 10
    dL = 40
    directions = [1, 1j, -1, -1j]
    altpos = [210, -210]

    layername(layer)
    setmark('tempcenter')
    square(dM)
    for dd in directions:
        gomark('tempcenter')
        rot(dd)
        go(25, 0)
        wirego(1, 70, dM)
        go(45, 0)
        square(dL)
        for i in xrange(2):
            go(70, 0)
            square(dL)
        go(140, 0)
        square(dL)
        for i in xrange(5):
            go(70, 0)
            square(dL)
    for ix in altpos:
        for iy in altpos:
            gomark('tempcenter')
            go(ix, iy)
            setmark('temptempcenter')
            square(dS)
            for dd in directions:
                gomark('temptempcenter')
                rot(dd)
                go(7.5, 0)
                wirego(1, 65, dS)
    gomark('tempcenter')

