# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 17:05:16 2016

@author: sebastian
"""

from clepywin import *

def rieEndpoint():
    setmark('inner')
    gomark('chip00')
    #circle center
    go(31500, 400)
    #go to startpoint draw 2* 180 degree for 1 circle
    go(-150, 0)
    R = 150
    w = 25
    mesh = 64
    def fullcircle(R, w, mesh):
        turn180go(-1j, R, w, mesh)
        turn180go(1j, R, w, mesh)
    layername('SiNwafer')
    fullcircle(R, w, mesh)
    layername('SiNdiel')    
    fullcircle(R, w, mesh)
    layername('MSline')
    fullcircle(R, w, mesh)
    layername('Hybrids')
    fullcircle(R, w, mesh)
    go(150-(150-25./2.)/2., 0)
    w = 150-25/2.
    R = (150-25./2.)/2.
    layername('MSgnd')
    fullcircle(R, w, mesh)
    layername('text')
    fullcircle(R, w, mesh)
    gomark('inner')