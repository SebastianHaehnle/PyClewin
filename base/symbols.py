# -*- coding: utf-8 -*-
"""
Created on Mon Sep 05 13:18:13 2016

@author: sebastian
"""

from ..script import *

def introSymbols():
    gg.w('(Symbol definitions:);\n')

def defineSymbol(synumber, syname):
    gg.w('DS{} 1 10'.format(synumber))
    gg.nl()
    gg.w('9 {}'.format(syname))
    gg.nl()
    gg.symbol[syname] = [synumber]

def toplevelSymbol(synumber, syname):
    gg.w('(Top level:);\n')
    defineSymbol(synumber, syname)

def placeSymbol(synumber, position, rotate = 0, mirror = ''):
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
    gg.w('DF')
    gg.nl()
    
def startSymbolWriting():
    """
    Clear Symbol writing capabilities from possibly old junk
    """
    gg.doSymbolWriting = True
    gg._s = ''
    gg.symbol_list = []
    gg.symbol_currentid = None
    gg.symbol_topid = None
    gg.symbol_s = []