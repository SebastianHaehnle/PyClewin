# -*- coding: utf-8 -*-
"""
Created on Mon Sep 05 11:54:55 2016

@author: sebastian
"""

from ..script import *
import sys

def introLayers():
    gg.w('(Layer names:);\n')


def addLayer(num, name, color):
    gg.w('L L{}; (CleWin: {} {}/{} {}));\n'.format(num, num, name, color, color))
    gg.layers[name] = color

def layer(num):
    gg.w('L L{};\n'.format(num))

def layername(name, dictionary = gg.layers):
    if name != gg.current_layer:
        num = layerindex(name, dictionary)
        layer(num)
        gg.current_layer = name

def layerindex(name, dictionary):
    kv = [(k,v) for k, v in dictionary.items()]
    index = 0
    i = 0
    found = False
    for k, v in kv:
        if k == name:
            index = i
            found = True
            break
        i += 1
    if not found:
        sys.exit('layername undefined: %s' % name)
    return index