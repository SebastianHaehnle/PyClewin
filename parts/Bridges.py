# -*- coding: utf-8 -*-
"""
Created on Mon Jan 09 15:19:58 2017

@author: sebastian
"""

from PyClewin import *

import numpy as np

class Bridge():
    '''
    Class for bridges over CPW, contains draw function to be passed to CPW classes.
    Adaptive to absolute CPW size, input parameters only specify,
    how much larger the bridge is in absolute um compared to the cpw
    Input:
        layerDiel   :: layer for dielectric
        layerMetal  :: layer for metal
    '''
    def __init__(self, layerDiel, layerMetal, extendDiel, lDiel, extendMetal, lMetal):
        self.layerDiel = layerDiel
        self.layerMetal = layerMetal
        self.extendDiel = extendDiel
        self.lDiel = lDiel
        self.extendMetal = extendMetal
        self.lMetal = lMetal

    def draw(self, direction, cpwline, cpwgap):
        layername(self.layerDiel)
        bar(direction, self.lDiel, cpwline + 2*cpwgap + self.extendDiel)
        layername(self.layerMetal)
        bar(direction, self.lMetal, cpwline + 2*cpwgap + self.extendDiel + self.extendMetal)

bridgeM4000MSLOC = Bridge('SiNdiel', 'MSline', 30.0, 40.0, 65.0, 20.0)
bridgeM4000MSFB = Bridge('SiNdiel', 'MSline', 20.0, 30.0, 55.0, 10.0)
bridgeM4000CPWleaky = Bridge('SiNdiel', 'Hybrids', 30.0, 40.0, 65.0, 20.0)
