# -*- coding: utf-8 -*-
"""
Created on Mon Sep 05 13:18:13 2016

@author: sebastian
"""

from script import *

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
    
def placeSymbol(synumber, position):
    gg.w('C {:d} T{:6.0f} {:6.0f}'.format(synumber, position[0]*gg.scale, position[1]*gg.scale))
    gg.nl()
    
def endSymbol():
    gg.w('DF')
    gg.nl()