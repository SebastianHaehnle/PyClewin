# -*- coding: utf-8 -*-
"""
Created on Mon Sep 05 11:48:19 2016

@author: sebastian
"""

from script import *

def setmark(name):
    gg.setmark(name)

def gomark(name):
    gg.gomark(name)

def xymark(name):
    return gg.mark(name)[0]

def dist2mark(name):
    return gg.dist2mark(name)

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
    
def moveto(x,y):
    gg.cle = [x,y]    

def rot(direction):
    gg.angle += np.angle(direction)
    gg.back = -np.angle(direction)
    gg.rotator = gg.rotator.dot(gg.rotation(np.angle(direction)))


def rotback():
    gg.angle += gg.back
    gg.rotator = gg.rotator.dot(gg.rotation(gg.back))

def flip(axis):
    gg.flip_axis(axis)
    
