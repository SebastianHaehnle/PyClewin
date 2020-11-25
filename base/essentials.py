# -*- coding: utf-8 -*-
"""
Created on Mon Sep 05 11:27:58 2016

@author: sebastian
"""

from ..script import *


def introScript():
    """
    DEPRECATED, use writeTotalString instead!
    Intro of a .cle file. This is automatically written now using writeTotalString.
    """
#    gg.doSymbolWriting = True
    gg.s = ''
    gg.w('(CIF written by CleWin 3.1);\n')
    gg.w('(1 unit = 0.001 micron);\n')
    gg.w('(SRON);\n')
    gg.w('(Sorbonnelaan 2);\n')
    gg.w('(3584 CA  Utrecht);\n')
    gg.w('(Nederland);\n')

def outroScript(synumber):    
    """
    DEPRECATED, use writeTotalString instead!
    """
    # synumber is number of the symbol, should be 1 higher than highest symbol # used.
    gg.w('DF;\n')
    if synumber > 0:
        gg.w('C {};\n'.format(synumber))
    gg.w('E\n')

def writeScript(filename):
    """
    DEPRECATED, use writeTotalString instead!
    """
    with open(filename, 'w') as ff:
        ff.write(gg.s)

def writeTotalString(filename):
    """
    This is the final command in a PyClewin chip or wafer script.
    Writes everything to the file with the name given by filename. 
    """
    # Switch to writing global string
    gg.doSymbolWriting = False
    
    # Script Intro
    gg.w('(CIF written by CleWin 3.1);\n')
    gg.w('(1 unit = 0.001 micron);\n')
    gg.w('(SRON);\n')
    gg.w('(Sorbonnelaan 2);\n')
    gg.w('(3584 CA  Utrecht);\n')
    gg.w('(Nederland);\n')

    # Layers    
    gg.w('(Layer names:);\n')    
    for num, name in enumerate(gg.layers.keys()):
        color = gg.layers[name]
        gg.w('L L{}; (CleWin: {} {}/{} {}));\n'.format(num, num, name, color, color))
    
    # All symbols
    gg.w('(Symbol definitions:);\n')
    for ii, name in enumerate(gg.symbol_list):
        if ii == gg.symbol_topid:            
            gg.w('(Top level:);\n')
        gg.w('DS{} 1 10'.format(ii+1))
        gg.nl()
        gg.w('9 {}'.format(name))
        gg.nl()
        gg.w(gg.symbol_s[ii])
        gg.w('DF')
        gg.nl()
    gg.w('C {};\n'.format(gg.symbol_topid+1))
    gg.w('E\n')
    with open(filename, 'w') as ff:
        ff.write(gg.s)
    
    