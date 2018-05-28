# -*- coding: utf-8 -*-
"""
Created on Mon Sep 05 11:20:37 2016

@author: sebastian
"""

from clepywin import *

import numpy as np
import scipy.constants as spc
import collections
import mwlib as mw

if __name__ == '__main__':
    
#==============================================================================
#   Define design output things
#==============================================================================
    
    filename = 'msloc1_v1.cif'
    
    layers = collections.OrderedDict()
    layers['MSgnd'] =  '0ff00ff00'
    layers['SiNdiel'] = '0f00cbff'
    layers['MSline'] = '0ffffff00'
    layers['Circles'] = '0f808080'
    layers['Hybrids'] = '0fff0000'
    layers['text'] = '0f000000'
    
    # Define the base unit for all lengths in the design
    unit_scale = 1e3    # micron
    gg.scale = unit_scale
    
#    Define meshing for corners
    mesh = 36
    
#==============================================================================
#   LINE GEOMETRIES
#==============================================================================
    #MSL
    w_msl = 1.4
#    Readout CPW
    w_ro = 20
    s_ro = 10
    
#    KID wide CPW
    w_wide = 4
    s_wide = 10
    
#    KID hybrid CPW
    w_hybrid = 1.4
    s_hybrid = 4
    
    

#==============================================================================
# KID GEOMETRY
#==============================================================================
#    filtkid kids
    def kidgenerator():
        # LENGTHS AND EPSILI
        lal = 2e-3
        lms = 300e-6
        epsms = 21
        epsal = 9.22
        epsw = 9.81
        
        #KID FREQUENCIES
        F0 = 4.2e9
        Fgap = 5e9
        delgap = 0.2e9
        FN = 5.8e9
        #NUM KIDS
        Nbb = 13
        Nfilt = 9 
#        Npure = 6 outside readout band, noise with vna
        Nblind = 8      
        N = Nbb + Nfilt + Nblind
        Ffilt  = [330e9, 345e9, 365e9, 610e9, 650e9, 690e9, 820e9, 855e9, 910e9]
        kids =  mw.KIDSdesign(F0, FN, N, epsal, lal, epsms, lms, epsw, Ffilt, Nblind, Fgap = Fgap, delgap = delgap)
#        kids.shuffle()
        return kids
    kids = kidgenerator()
    lhoriz = 20 # fixed horizontal length on both sides of coupling length 
#   filtkid filters
    num_filtkid = len(kids.filtered)
    
    l_filtkid_hybrid = np.linspace(1500, 2000, num_filtkid)
    l_filtkid_wide = np.linspace(3500, 5000, num_filtkid)
    lambda_filtkid_thz = np.linspace(100, 200, num_filtkid)
    
#    COUPLING 
    l_kidQ_c = np.linspace(200, 500, kids.N)
    d_kidQ_c = 6
    
#==============================================================================
#     FILTER GEOMETRY
#==============================================================================

#    corner radius
    r_filter = 4.8
#    coupling distance
    l_filter_c = np.linspace(32, 16, num_filtkid)
#    vertical part length of filter 
    l_filter_v = np.linspace(16,0,num_filtkid)
#    coupling distance
    d_filter_c = 0.8
#    space between filtkid structures
    d_filter_spacing = 6e3/(num_filtkid+1)
    kids.filters.set_geometry(l_filter_c, l_filter_v, d_filter_c, r_filter)    
    
#   solo filters (defs see filtkid geometry)
    num_filtsolo = num_filtkid
    F_filtersolo = np.linspace(300, 900, num_filtsolo)
    l_filtersolo_c = np.linspace(40, 20, num_filtsolo)
    l_filtersolo_v = np.linspace(20, 4, num_filtsolo)  
    
    filters = mw.FiltersDesign(F_filtersolo, mw.eps_2_vph(kids.eeff_ms))
    filters.set_geometry(l_filtersolo_c, l_filtersolo_v, d_filter_c, r_filter)

#==============================================================================
#   Meander geometry / KID distances at transmission line
#==============================================================================
#    distances between broadband kids starting from labyrinth
    dx_bb = 1e3 #this is currently set in delayline function
    d_bb = np.array([0.5e3, 3e3, d_filter_spacing, 3e3, 3e3, 3e3, 3e3, 9e3, 9e3, 9e3, 27e3, 27e3, 27e3])
    y_meander_chipend = 1.2e3   

#==============================================================================
#   Readoutline geometry
#==============================================================================
    x_ro_chipend = 0.5e3 #defined from bondpad start
    x_ro_labyend = 24.2e3     #defined from bondpad start
    d_laby = 100    #distance of readoutline from labyrinth
    r_ro = 100  #80 minimum
    y_ro_far = 5.8e3 # top part of vertical readout 
    d_blind = 400 # distance between blind kids
# y_ro_blind define further on by remaining distance
#==============================================================================
# Some console feedback
#==============================================================================
    print 'Some info:'
    print kids
    
    print 'distances between bb-kids [mm]:'
    print '-------'
    print d_bb*1e-3, '\n'
    
    print 'lines: '
    print '-------'
    print 'MSL: w ={:f}'.format(w_msl)
    print 'hybrid: w={:f}, s={:f}'.format(w_hybrid, s_hybrid)
    print 'wide: w={:f}, s={:f}'.format(w_wide, s_wide)
    print 'readout: w={:f}, s={:f}'.format(w_ro, s_ro)
    
    
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
    rot(1)
#==============================================================================
# includebase chip layout
#==============================================================================
    msloc_base(layers, w_msl, mesh)
#==============================================================================
#    write labyrinth, TODO: put into extra part
#==============================================================================
#    write in MSL layer

#==============================================================================
#   draw filterbank    
#==============================================================================    
# first BB-KID
    jj = 0
    wirego(1, d_bb[jj], w_msl)
    msloc_kid_v2(kids.broadband[jj], w_hybrid, s_hybrid, w_wide, s_wide, w_msl, d_filter_c, lhoriz, r_filter, mesh, layers)
    jj+=1
#    draw upward section entering meander section
    msl_delayline_up(w_msl, d_bb[jj], dist2mark('chipyend')[1]-y_meander_chipend, mesh)
    msloc_kid_v2(kids.broadband[jj], w_hybrid, s_hybrid, w_wide, s_wide, w_msl, d_filter_c, lhoriz, r_filter, mesh, layers)
    jj += 1

    
    for i, i_kid in enumerate(kids.filtered):
        setmark('filtkid'+str(i))
        lhoriz = i_kid.filter.lamb*1e6/8
#        end of transmission line section is x-position of top-right KID corner!!! Filter + KID is drawn downward
        xoffset = lhoriz + r_filter + 0
        wirego(1, d_filter_spacing, w_msl)
#        move by coupling distance and offset filter from vertical KID CPW
        go(-xoffset, -(w_msl + d_filter_c))
#        draw filter
        c_filter_msl_v1(w_msl, r_filter, l_filter_c[i], l_filter_v[i], mesh)
#        move by coupling distance and go back to top right corner of KID
#        draw KID
        msloc_kid_v2(i_kid, w_hybrid, s_hybrid, w_wide, s_wide, w_msl, d_filter_c, lhoriz, r_filter, mesh, layers)
#        filter w/o kid              
        gomark('filtkid'+str(i))
        go(d_filter_spacing/2, 0)
#        solo filter is equal to filt+kid, but on upper side of transmission line (done by flipping cosy)        
        flip('y')
        go(-xoffset, -(w_msl+d_filter_c))
        c_filter_msl_v1(w_msl, r_filter, l_filtersolo_c[i], l_filtersolo_v[i], mesh)
        flip('y')
        gomark('filtkid'+str(i))
        go(d_filter_spacing, 0)

#    Draw bb-KID directly after filterbank
    wirego(1, d_bb[jj], w_msl)
    msloc_kid_v2(kids.broadband[jj], w_hybrid, s_hybrid, w_wide, s_wide, w_msl, d_filter_c, lhoriz, r_filter, mesh, layers)
    jj+=1
#    draw upward section entering meander section
    msl_delayline_up(w_msl, d_bb[jj], 0, mesh)
    msloc_kid_v2(kids.broadband[jj], w_hybrid, s_hybrid, w_wide, s_wide, w_msl, d_filter_c, lhoriz, r_filter, mesh, layers)
    jj += 1
        
    for i, d in enumerate(d_bb[jj:]):
        msl_delayline(w_msl, d, mesh)
        msloc_kid_v2(kids.broadband[i+jj], w_hybrid, s_hybrid, w_wide, s_wide, w_msl, d_filter_c, lhoriz, r_filter, mesh, layers)
    
#    TODO: DRAW absorption section

#==============================================================================
#   draw Readoutline
#==============================================================================
    def endpos_kids():
        ocd = []
        for k, v in gg.mark.items():
            if 'KIDend' in k:
                ocd.append([v[0][0], v[0][1], k, int(k.strip('KIDend'))])
        ocd = sorted(ocd, key = lambda x: x[0])
        ocd.reverse()
        return ocd
    kidpos = endpos_kids()
        
    layername('MSgnd', layers)
    gomark('bondpadtop')
    cpwgo(-1, x_ro_chipend - r_ro, w_ro, s_ro)
    cpwupgo(-1, r_ro, w_ro, s_ro, mesh)
    cpwgo(-1j, y_ro_far, w_ro, s_ro)
    cpwdowngo(-1j, r_ro, w_ro, s_ro, mesh)
    setmark('ro_topright')
    
    
    # here is the section with automatic readout connection to KID instead of the go() command
    for blabla in kidpos:
        msloc_readout_attachright(blabla[2], l_kidQ_c[blabla[3]], d_kidQ_c, w_wide, s_wide, w_ro, s_ro, r_ro, mesh)
    setmark('ro_topleft')
    
#==============================================================================
# Blind KID section of readout
#==============================================================================
    
    gomark('bondpadbot')
#    cpwgo(-1, x_ro_labyend - r_ro, w_ro, s_ro)
    cpwgo(-1, dist2mark('labyend')[0] - d_laby - r_ro, w_ro, s_ro)
    cpwdowngo(-1, r_ro, w_ro, s_ro, mesh)
    for bb in kids.blind:
        ii = bb.i0
        setmark('outer')
        
        go(2*r_ro+bb.ltot*1e6, d_blind)
        rot(-1j)        
        msloc_kid_v2(bb, w_hybrid, s_hybrid, w_wide, s_wide, w_msl, 0, lhoriz, r_filter, mesh, layers)
        layername('MSgnd', layers)
        gomark('outer')
        rot(-1j)
        msloc_readout_attachright('KIDend'+str(ii), l_kidQ_c[ii], d_kidQ_c, w_wide, s_wide, w_ro, s_ro, r_ro, mesh)
        rot(1j)
# Other blind stuff and pure stuff. Simple line as filler
    cpwgo(1j, dist2mark('ro_topleft')[1]-r_ro, w_ro, s_ro)
    cpwdowngo(1j, r_ro, w_ro, s_ro, mesh)
    cpwgo(1, dist2mark('ro_topleft')[0], w_ro, s_ro)   
    
#==============================================================================
# Final touches    
#==============================================================================
    outroScript(1)
    # write to file
    writeScript(filename)
    
#    print gg.cle
#    print gg.s
    
#if __name__ == '__main__':
#    msloc1_v1()
