# -*- coding: utf-8 -*-
"""
Created on Mon Sep 05 14:09:35 2016

@author: sebastian
"""

from ..script import *
from ..base import *
import numpy as np

#==============================================================================
# Core writing function
#==============================================================================

def poly(xyarray, shift = (0,0)):
    '''
    writes nparray to script-str in UCS with possibility to shift by x,y
    xyarray must be 2D numpy-array [[x positions], [y positions]]
    '''
    xyarray = np.array(xyarray)
    gg.w('P ')
    for i in xyarray.transpose():
        gg.w('{:6.0f} {:6.0f} '.format(*gg.proj(i[0]+shift[0], i[1] + shift[1])))
    gg.nl()


#==============================================================================
# Core coordinate creation functions
#==============================================================================

def makeWire(L, W):
    xy = np.array([[0, L, L, 0], [-W/2., -W/2., W/2., W/2.]])
    return xy

def makeTurn(R, line, mesh, rad):
#    Some stuff to make this function work with different angles (tested with 90 and 180)
    fac = rad/np.pi
    mesh = abs(int(mesh*fac))
#    inner radius x-coord
    x1 = [(R-line/2)*np.sin(np.pi-rad + i*np.pi/float(mesh)*fac) for i in range(mesh+1)]
#    outer radius x-coord
    x2 = [(R+line/2)*np.sin(np.pi - i*np.pi/float(mesh)*fac) for i in range(mesh+1)]
#    inner radis y-coord
    y1 = [(R-line/2)*np.cos(np.pi-rad + i*np.pi/float(mesh)*fac) for i in range(mesh+1)]
#    outer radius y-coord
    y2 = [(R+line/2)*np.cos(np.pi - i*np.pi/float(mesh)*fac) for i in range(mesh+1)]
    if fac > 0:
    #    Combine arrays
        xy = np.array([x1+x2,y1+y2])
    #    Move curve beginning to (0,0) position
        xy[1] = xy[1] + R
    else:
        xy = -np.array([x1+x2, y1+y2])
        xy[1] = xy[1] - R
    return xy

#==============================================================================
# basic line functions incl curves and line+go
#==============================================================================


def wire(direction, L, W, shift = (0,0)):
    rot(direction)
    poly(makeWire(L,W), shift)
    rotback()
    return direction

def wirego(direction, L, W, shift = (0,0)):
    wire(direction, L, W, shift)
    rot(direction)
    go(L, 0)
    rotback()
    return direction

def turn(direction, angle, R, line, mesh, shift = (0,0)):
    rot(direction)
    poly(makeTurn(R, line, mesh, angle), shift)
    rotback()
    return direction

def turnup(direction, R, line, mesh, shift = (0,0)):
    rot(direction)
    poly(makeTurn(R, line, mesh, np.pi/2.), shift)
    rotback()
    return direction

def turndown(direction, R, line, mesh, shift = (0,0)):
    rot(direction)
    poly(makeTurn(R, line, mesh, -np.pi/2.), shift)
    rotback()
    return direction

def turn180(direction, R, line, mesh, shift = (0,0)):
    rot(direction)
    poly(makeTurn(R, line, mesh, np.pi), shift)
    rotback()
    return direction

def turnupgo(direction, R, line, mesh, shift = (0,0)):
    turnup(direction, R, line, mesh, shift)
    rot(direction)
    go(R,R)
    rotback()
    direction_out = np.exp(1j*(np.angle(direction) + np.pi/2.))
    return direction_out

def turndowngo(direction, R, line, mesh, shift = (0,0)):
    turndown(direction, R, line, mesh, shift)
    rot(direction)
    go(R,-R)
    rotback()
    direction_out = np.exp(1j*(np.angle(direction) - np.pi/2.))
    return direction_out

def turn180go(direction, R, line, mesh, shift = (0,0)):
    turn180(direction, R, line, mesh, shift)
    rot(direction)
    go(0, 2*R)
    rotback()
    return -direction


def turn45up(direction, R, line, mesh, shift = (0,0)):
    rot(direction)
    xy45 = makeTurn(R, line, mesh, np.pi/4.)
    poly(xy45, shift)
    rotback()
    return direction

def turn45upgo(direction, R, line, mesh, shift = (0,0)):
    rot(direction)
    xy45 = makeTurn(R, line, mesh, np.pi/4.)
    poly(xy45, shift)
    go((xy45[0][-1]+xy45[0][0])/2., (xy45[1][-1]+xy45[1][0])/2.)
    rotback()
#    return direction

def turn45down(direction, R, line, mesh, shift = (0,0)):
    rot(direction)
    xy45 = makeTurn(R, line, mesh, -np.pi/4)
    poly(xy45, shift)
    rotback()
    return direction

def turn45downgo(direction, R, line, mesh, shift = (0,0)):
    rot(direction)
    xy45 = makeTurn(R, line, mesh, -np.pi/4)
    poly(xy45, shift)
    go((xy45[0][-1]+xy45[0][0])/2., (xy45[1][-1]+xy45[1][0])/2.)
    rotback()
#    return direction

def broaden(direction, L, W_narrow, W_broad, shift = (0,0)):
    rot(direction)
    xy = [[0, L, L, 0], [-W_narrow/2., -W_broad/2., W_broad/2., W_narrow/2.]]
    poly(np.array(xy), shift)
    rotback()
    return direction

def broadengo(direction, L, W_narrow, W_broad, shift = (0,0)):
    broaden(direction, L, W_narrow, W_broad, shift)
    rot(direction)
    go(L, 0)
    rotback()
    return direction

#==============================================================================
#     CPWs (curves and cpw+go)
#==============================================================================

def cpw(direction, L, line, gap, shift = (0,0)):
    wire(direction, L, gap, (0+shift[0],(line+gap)/2.+shift[1]))
    wire(direction, L, gap, (0+shift[0],-(line+gap)/2.+shift[1]))
    return direction

def cpwgo(direction, L, line, gap, shift = (0,0)):
    wire(direction, float(L), gap, (0+shift[0],(line+gap)/2.+shift[1]))
    wire(direction, float(L), gap, (0+shift[0],-(line+gap)/2.+shift[1]))
    rot(direction)
    go(float(L), 0)
    rotback()
    return direction

def cpwbroaden(direction, L, line_narrow, gap_narrow, line_wide, gap_wide, shift = (0,0)):
    xy1 = np.array([[0, 0, L, L], [line_narrow/2, gap_narrow + line_narrow/2., gap_wide + line_wide/2., line_wide/2.]])
    rot(direction)
    poly(xy1, shift)
    xy1[1] = -1*xy1[1]
    poly(xy1, shift)
    rotback()
    return direction

def cpwbroadengo(direction, L, line_narrow, gap_narrow, line_wide, gap_wide, shift = (0,0)):
    cpwbroaden(direction, L, line_narrow, gap_narrow, line_wide, gap_wide, shift)
    rot(direction)
    go(L, 0)
    rotback()
    return direction

def cpwup(direction, R, line, gap, mesh, shift = (0,0)):
    rot(direction)
#    inner gap
    go(0, +(gap+line)/2.)
    poly(makeTurn(R-(gap+line)/2., gap, mesh, np.pi/2.), shift)
#    outer gap
    go(0, -(gap+line))
    poly(makeTurn(R+(gap+line)/2., gap, mesh, np.pi/2.), shift)
    go(0, +(gap+line)/2.)
    rotback()
    return direction

def cpwdown(direction, R, line, gap, mesh, shift = (0,0)):
    rot(direction)
#    inner gap
    go(0, -(gap+line)/2.)
    poly(makeTurn(R-(gap+line)/2., gap, mesh, -np.pi/2.), shift)
#    outer gap
    go(0, +(gap+line))
    poly(makeTurn(R+(gap+line)/2., gap, mesh, -np.pi/2.), shift)
    go(0, -(gap+line)/2.)
    rotback()
    return direction

def cpw180(direction, R, line, gap, mesh, shift = (0,0)):
    rot(direction)
#    inner gap
    go(0, +(gap+line)/2.)
    poly(makeTurn(R-(gap+line)/2., gap, mesh, np.pi), shift)
#    outer gap
    go(0, -(gap+line))
    poly(makeTurn(R+(gap+line)/2., gap, mesh, np.pi), shift)
    go(0, +(gap+line)/2.)
    rotback()
    return direction

def cpwupgo(direction, R, line, gap, mesh, shift = (0,0)):
    cpwup(direction, R, line, gap, mesh, shift)
    rot(direction)
    go(R,R)
    rotback()
    return direction

def cpwdowngo(direction, R, line, gap, mesh, shift = (0,0)):
    cpwdown(direction, R, line, gap, mesh, shift)
    rot(direction)
    go(R,-R)
    rotback()
    return direction

def cpw180go(direction, R, line, gap, mesh, shift = (0,0)):
    cpw180(direction, R, line, gap, mesh, shift)
    rot(direction)
    go(0, 2*R)
    rotback()
    return direction

#==============================================================================
# MSL wires
#==============================================================================

def ms(direction, L, W, Wsin, layer1 = 'MSline', layer2 = 'SiNdiel', layer3 = 'SiNwafer', shift = (0,0)):
    layername(layer3)
    wire(direction, L, 2*Wsin)
    layername(layer2)
    wire(direction, L, Wsin)
    layername(layer1)
    wire(direction, L, W)
    return direction

def msgo(direction, L, W, Wsin, layer1 = 'MSline', layer2 = 'SiNdiel',  layer3 = 'SiNwafer', shift = (0,0)):
    layername(layer3)
    wire(direction, L, 2*Wsin)
    layername(layer2)
    wire(direction, L, Wsin)
    layername(layer1)
    wirego(direction, L, W)
    return direction

def msupgo(direction, R, line, mesh, Wsin, layer1 = 'MSline', layer2 = 'SiNdiel', layer3 = 'SiNwafer', shift = (0,0)):
    layername(layer3)
    turnup(direction, R, 2*Wsin, mesh)
    layername(layer2)
    turnup(direction, R, Wsin, mesh)
    layername(layer1)
    turnupgo(direction, R, line, mesh)
    return direction


def msdowngo(direction, R, line, mesh, Wsin, layer1 = 'MSline', layer2 = 'SiNdiel', layer3 = 'SiNwafer', shift = (0,0)):
    layername(layer3)
    turndown(direction, R, 2*Wsin, mesh)
    layername(layer2)
    turndown(direction, R, Wsin, mesh)
    layername(layer1)
    turndowngo(direction, R, line, mesh)

def ms45upgo(direction, R, line, mesh, Wsin, layer1 = 'MSline', layer2 = 'SiNdiel', layer3 = 'SiNwafer', shift = (0,0)):
    layername(layer3)
    turn45up(direction, R, 2*Wsin, mesh)
    layername(layer2)
    turn45up(direction, R, Wsin, mesh)
    layername(layer1)
    turn45upgo(direction, R, line, mesh)
    return direction

def ms45downgo(direction, R, line, mesh, Wsin, layer1 = 'MSline', layer2 = 'SiNdiel', layer3 = 'SiNwafer', shift = (0,0)):
    layername(layer3)
    turn45down(direction, R, 2*Wsin, mesh)
    layername(layer2)
    turn45down(direction, R, Wsin, mesh)
    layername(layer1)
    turn45downgo(direction, R, line, mesh)
    return direction
