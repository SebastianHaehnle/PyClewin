# -*- coding: utf-8 -*-
"""
Created on Mon Sep 05 11:33:17 2016

@author: sebastian
"""

import pkgutil 

__path__ = pkgutil.extend_path(__path__, __name__)
for importer, modname, ispkg in pkgutil.walk_packages(path=__path__, prefix=__name__+'.'):
      __import__(modname)