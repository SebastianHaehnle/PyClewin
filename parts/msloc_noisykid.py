# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 10:11:31 2016

@author: sebastian
"""

from clepywin import *
import scipy.constants as spc
import numpy as np

def msloc_purewide(kid_ID, wwide, swide, Fres, epseff):
    '''
    Give kid_ID values higher than num_kids, start e.g. at 100
    '''
    L = spc.c / (4 * Fres * np.sqrt(epseff))
    layername('MSgnd')
    cpwgo(-1j, L, wwide, swide)
    wirego(-1j, swide, wwide + 2*swide)
    setmark('KIDend'+str(kid_ID))

def msloc_purehyb(kid_ID, wwide, swide, whyb, shyb, Fres, epswide, epshyb):
#==============================================================================
#     TODO: Fres  + Qc => Lc = Lwide => Lal
#==============================================================================
    taper_l_alwide = 20
    # hybrid section
    layername('Hybrids')
    wire(-1j, lal, whyb)
    layername('MSgnd')
    wirego(-1j, lal, whyb + 2*shyb)
    transition_hybwide(whyb, shyb, wwide, swide, taper_l_alwide)
    # Wide section
    cpwgo(-1j, lwide, wwide, swide)    
    wirego(-1j, swide, wwide + 2*swide)
    setmark('KIDend'+str(kid_ID))
    
def msloc_puremsl(kid_ID, wmsl, wwide, swide, whyb, shyb, Fres, epsmsl, epswide, epshyb):
    pass

if __name__ == '__main__':
    pass