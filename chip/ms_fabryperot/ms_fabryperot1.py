# -*- coding: utf-8 -*-
"""
Created on Mon Jan 09 16:40:08 2017

@author: sebastian
"""

from clepywin import *

import numpy as np
import scipy.constants as spc
import collections
import mwlib as mw
import KIDdesignNew as KDnew

if __name__ == '__main__':
#==============================================================================
#   Define design output things
#==============================================================================
    
    filename = 'ms_fabryperot1.cif'
    
    layers = collections.OrderedDict()
    layers['SiNwafer'] = '0f00ffcb'
    layers['MSgnd'] =  '0ff00ff00'
    layers['SiNdiel'] = '0f00cbff'
    layers['MSline'] = '0ff0000ff'
#    layers['Circles'] = '0f808080'
    layers['Hybrids'] = '0fff0000'
    layers['TantalumFront'] = '0f888800'
    layers['TantalumBack'] = '0fc0c0c0'
    layers['SiNbackside'] = '0fff00cb'
    layers['text'] = '0f000000'
    
    # Define the base unit for all lengths in the design
    unit_scale = 1e3    # micron
    gg.scale = unit_scale
    
#    Define meshing for corners
    mesh = 36
    
#==============================================================================
# Define lines
#==============================================================================
    #----------- General settings
    kidShortL = 10                      # Length of NbTiN line shorts
    kidTrans1 = transMSHybridM4000      # transition type for KID MS->hybrid
    kidTrans2 = transHybridWideM4000    # transition type for KID hybrid->wide
    rotateLeaky = True                  # Orientation of antenna
    
    #----------- Transmission line
    ms = Microstrip3layer(line = 1.4 + manVars.nbtinLine, 
                          dielwidth = 60., 
                          botwidth = 120.,
                          linelayer = 'MSline',
                          diellayer = 'SiNdiel',
                          botlayer = 'SiNwafer',
                          mesh = mesh)
    
    #----------- KID sections
    kidMS = ms
    
    kidHybrid = CPWhybrid(line = 2.,
                              gap = 2.,
                              linelayer = 'Hybrids',
                              gndlayer = 'MSgnd',
                              mesh = mesh)
    
    kidWide = CPW(line = 6. + manVars.nbtinLine,
                      gap = 16. + manVars.nbtinSlot,
                      mesh = mesh,
                      gndlayer = 'MSgnd')
    
    #----------- Readout 
    roBridgefun = bridgeM4000MSLOC.draw
    
    ro = CPWreadout(line = 19. + manVars.nbtinLine, 
                    gap = 8. + manVars.nbtinSlot, 
                    cpwlayer = 'MSgnd', 
                    diellayer = 'SiNwafer', 
                    bridgefun = roBridgefun, 
                    bridgeDistance = 2e3, 
                    mesh = mesh)

    
#==============================================================================
# Define KIDs
#==============================================================================
    epsms = 20.7 #for w=1.9 msl
    lambda600GHz = mw.f_2_lambda(600e9, epsms)*1e6
    l_transformer = lambda600GHz/4.    
    epsal = 9.78 # for GHz readout signal
    epsw = 7.77 #
    Zcpw = 85.0
    Zms = 82.0
#    filtkid kids
    def kidgenerator(epsms, epsal, epsw):
        # LENGTHS
        lal = 1.6e-3
        lms = 200e-6
        #KID FREQUENCIES
        F0 = 5.5e9
        Fgap = None
        delgap = None
        FN = 5.5e9
        #KID Qc values
        Qc = 20e3
        Qcblind = 100e3
        #NUM KIDS
        Nbb = 0
        Nfilt = 0 
        Npure = 0 #outside readout band, noise with vna
        Nblind = 1      
        N = Nbb + Nfilt + Nblind
        Ffilt  = []
#        kids =  mw.KIDSdesign(F0, FN, N, epsal, lal, epsms, lms, epsw, Ffilt, Nblind, Fgap = Fgap, delgap = delgap)
        kids = KDnew.KIDSdesign(F0, FN, N, epsal, lal, Zcpw, epsms, lms, Zms, epsw, Ffilt, Nblind, Fgap = Fgap, delgap = delgap)
        # generate coupling lengths for kids in original F-position
        path = 'C:\Users\sebastian\ownCloud\Chipdesign\M4000\msloc1\sonnet\msloc1_v1\kidQc.dat'                
        kids.gen_lcouple(path, Qc, Qcblind)
        return kids, Nblind + Npure
    kids, num_blind = kidgenerator(epsms, epsal, epsw)



#==============================================================================
# Define interferometer
#==============================================================================
    fpLength = 15e3
   
    
#==============================================================================
# Define other geometry on chip
#==============================================================================
    roDtoEdge = 2e3

#==============================================================================
#==============================================================================
# #   Start writing clewin file    
#==============================================================================
#==============================================================================    
    # misc stuff at the start
    introScript()
    # define Layers
    introLayers()
    for i, k in enumerate(layers):
        addLayer(i+1, k, layers[k])
    # write actual symbols
    introSymbols()
    defineSymbol(1, 'MAIN')
#==============================================================================
# base chip layout, includes labyrinth
#==============================================================================
    Mosaic42x14_leaky(layers = layers, 
                      mainline = ms, 
                      rotate_leaky = True)
    
#==============================================================================
# Draw THz section
#==============================================================================
    gomark('labyend')
    # Placeholder for proper coupler
    go(100, 0)
    # Interferometer length
    setmark('fpstart')
    ms.wirego(1, fpLength)
    setmark('fpend')
    # Placeholder for coupler to KID
    go(100, -2000)
    # Placeholder for KID
    kidStraight(1, 
                kid = kids[0], 
                ms = kidMS, 
                hybrid = kidHybrid, 
                wide = kidWide, 
                lShort = kidShortL, 
                funcTransMSCPW = kidTrans1, 
                funcTransHybridWide = kidTrans2)
#    kidlineMS.wirego(1, 200)
#    layername(ms.botlayer)
#    wire(1, 1.6e3, ms.botwidth)
#    kidlineHybrid.wirego(1, 1.5e3)
#    kidlineWide.wirego(1, 3e3)
    setmark('KID0')


#==============================================================================
# Draw DC wiring
#==============================================================================
    def bondpadDC(direction):
        wire(direction, 750, 750)
    
    layername('MSline')
    gomark('chip00')
    go(250, 5.5e3)
    for i in xrange(4):
        bondpadDC(1)
        go(0, 1e3)
    
        
#==============================================================================
# Draw readout
#==============================================================================
    gomark('bondpadtop')
    bondpadM4000(ro)
    gomark('bondpadtop')
    ro.wirego(-1, roDtoEdge - x2m('chipFF'))
    ro.upgo(-1, roRadius)
    setmark('readouttop')
    
    gomark('bondpadbot')
    bondpadM4000(ro)
    gomark('bondpadbot')
    ro.wirego(-1, roDtoEdge - x2m('chipFF'))
    ro.downgo(-1, roRadius)
    setmark('readoutbot')
    
#==============================================================================
# Final touches    
#==============================================================================      
    outroScript(1)
    # write to file
    writeScript(filename)