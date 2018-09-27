# -*- coding: utf-8 -*-
"""
Created on Fri Sep 07 10:49:09 2018

@author: sebastian
"""

from PyClewin import *
from PyClewin.base import *
import numpy as np


def mesh850ghz(layer, mark1, mark2):
    d_sq = 3
    l_sq = 50
    l_sq = l_sq-d_sq
    setmark('current')
    gomark(mark1)
    lx, ly = base.dist2markSigned(mark2)
    base.squares_inverse(layer, lx, ly, l_sq, d_sq)
    gomark('current')
    delmark('current')