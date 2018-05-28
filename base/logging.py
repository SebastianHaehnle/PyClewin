# -*- coding: utf-8 -*-
"""
Created on Tue Dec 06 15:57:05 2016

@author: sebastian
"""

import numpy as np
import scipy.constants as spc
import os
import matplotlib.pyplot as plt

class MasterKidlist():
    typeDict = {-1 : 'blind',
                0 : 'filtered',
                1 : 'broadband',
                2 : 'nbtin',
                3 : 'al',
                4 : 'ms'}    
    
    def __init__(self, filepath = None):
        if filepath:
            self.loadFile(filepath)
            return None
    
    def loadFile(self, filepath):
        self.id, self.type, self.F, self.Qc, self.al_area, self.filtF, self.filtQc, self.lwide, self.lal, self.lms = np.loadtxt(filepath, unpack = True)
        
    def calcFfromEps(self, epswide, epsal, epsms):
        self.Fnew =  spc.c/4/(self.lwide*np.sqrt(epswide) + self.lms*np.sqrt(epsms) + self.lal*np.sqrt(epsal))
        return self.Fnew
        
if __name__ == '__main__':
    folder = r'C:\Users\sebastian\ownCloud\p27lib\clepywin\chip\M4000\msloc1\upgrade'
    filename = r'msloc_v2_masterlist.txt'
    master = MasterKidlist(os.path.join(folder, filename))
    
    epswide = 7.77
    epsal = 9.78
    epsms = 21.89
    epsmsnew = 38.8
    
    print master.calcFfromEps(epswide, epsal, epsmsnew) - master.F
                             