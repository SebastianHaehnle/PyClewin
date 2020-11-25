# -*- coding: utf-8 -*-
"""
Created on Mon Sep 05 13:18:13 2016

@author: sebastian
"""

from ..script import *

def introSymbols():
    """
    DEPRECATED
    """
    gg.w('(Symbol definitions:);\n')

def defineSymbol(synumber, syname):
    """
    DEPRECATED
    """
    gg.w('DS{} 1 10'.format(synumber))
    gg.nl()
    gg.w('9 {}'.format(syname))
    gg.nl()
    gg.symbol[syname] = [synumber]

def toplevelSymbol(synumber, syname):
    """
    DEPRECATED
    """
    gg.w('(Top level:);\n')
    defineSymbol(synumber, syname)

def placeSymbol(synumber, position, rotate = 0, mirror = ''):
    """
    Places symbol in the currently active symbol.
    WARNING: Always check final symbol position when rotation and mirror is active. Might give unexpected results.
    
    Parameters:
    ------
    synumber : int or str
        either the number of the symbol or its namestring
    position : float
        Position of the symbol, this corresponds to the 0/0 position of the defined symbol.
    rotate : 0/90/-90
        Default = 0. Rotates the symbol by given amount. WARNING: At the moment only supports full 90 or -90 degree rotation.
    mirror : 'x' or 'y'
        Mirrors symbol around x or y axis.
    """
    
    if type(synumber) == str:
        synumber = gg.symbol_list.index(synumber)+1
    rotationstring = ''
    if rotate == 90:
        rotationstring = 'R 0 1 '
    elif rotate == -90:
        rotationstring = 'R 0 -1 '
    mirrorstring = ''
    if mirror == 'x':
        mirrorstring = 'MX'
    elif mirror == 'y':
        mirrorstring = 'MY'
    gg.w('C {:d} {:s} {:s}T{:6.0f} {:6.0f}'.format(synumber, mirrorstring, rotationstring, position[0]*gg.scale, position[1]*gg.scale))
    gg.nl()

def endSymbol():
    """
    DEPRECATED
    """
    gg.w('DF')
    gg.nl()
    
def startSymbolWriting():
    """
    This goes at the start of ever script. Think about joining this with the essentials.py file
    Clear Symbol writing capabilities from possibly old junk
    """
    gg.doSymbolWriting = True
    gg._s = ''
    gg.symbol_list = []
    gg.symbol_currentid = None
    gg.symbol_topid = None
    gg.symbol_s = []