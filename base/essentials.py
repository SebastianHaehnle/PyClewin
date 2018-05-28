# -*- coding: utf-8 -*-
"""
Created on Mon Sep 05 11:27:58 2016

@author: sebastian
"""

from script import *


def introScript():
    gg.s = ''
    gg.w('(CIF written by CleWin 3.1);\n')
    gg.w('(1 unit = 0.001 micron);\n')
    gg.w('(SRON);\n')
    gg.w('(Sorbonnelaan 2);\n')
    gg.w('(3584 CA  Utrecht);\n')
    gg.w('(Nederland);\n')

def outroScript(synumber):
    # synumber is number of the symbol, should be 1 higher than highest symbol # used.
    gg.w('DF;\n')
    if synumber > 0:
        gg.w('C {};\n'.format(synumber))
    gg.w('E\n')
    
def writeScript(filename):
    with open(filename, 'w') as ff:
        ff.write(gg.s)
        
