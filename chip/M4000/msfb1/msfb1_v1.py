# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 15:17:35 2016

@author: sebastian
"""

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
import KIDdesignNew as newKD

   



#def main():
if __name__ == '__main__':
#==============================================================================
#   Define design output things
#==============================================================================
    
    filename = 'msfb1_v1.cif'
    
    layers = collections.OrderedDict()
    layers['SiNwafer'] = '0f00ffcb'
    layers['MSgnd'] =  '0ff00ff00'
    layers['SiNdiel'] = '0f00cbff'
    layers['MSline'] = '0ff0000ff'
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
#   LINE GEOMETRIES TODO: correct transformer / terminator geometry
#==============================================================================
    #MSL
    w_msl = 1.4 + manVars.nbtinLine        #width of line
    w_sin = 60.                     #width of dielectric
    r_msl = 100.                    #turn radius of MSL
    r_turn = 4.7

#    Readout CPW
    w_ro = 9.5 + manVars.nbtinLine         #width of line
    s_ro = 3 + manVars.nbtinSlot          #width of slot
    
    x_ro_chipend = 1.0e3            #offset of bondpad start from chip end (includes taper)
    d_laby = 100.                   #distance of readoutline from labyrinth
    r_ro = 30                     #30 minimum
    y_ro_far = 6.8e3                #offset of readoutline from thz line  
    
#    KID wide CPW
    w_wide = 6. +  manVars.nbtinLine       #width of line
    s_wide = 16. + manVars.nbtinSlot       #width of slot
    
#    KID hybrid CPW
    w_hybrid = 1.4  + manVars.alLine        #width of line
    s_hybrid = 2.4  + (manVars.nbtinSlot - manVars.alLine)/2.    #width of slot
    
#    lambda/4 transformer (terminator)
    w_transformer = 2.6 + manVars.nbtinLine
    s_transformer = 3 + manVars.nbtinSlot
    l_transformer = None #dummy, define after epseff definition

#    Terminator CPW
    w_terminator = 1.4 + manVars.alLine
    s_terminator = 4 + (manVars.nbtinSlot - manVars.alLine)/2.
    l_terminator = 5e3
    # Hasta la vista, baby!

#   Bridge geometry
    bridgefun = msfb_bridge


#==============================================================================
# KID GEOMETRY TODO: correct epseff
#==============================================================================
#    Epsilon effective
    epsms = 21.89
    lambda600GHz = mw.f_2_lambda(600e9, epsms)*1e6
    l_transformer = lambda600GHz/4.    
    epsal = 9.78 # for GHz readout signal
    epsw = 7.77 #
    Zcpw = 85.0
    Zms = 102.0
    # Qc created by kidQc.py
    path_Qc = r'C:\Users\sebastian\Documents\deshima\pycad\clepywin\chip\msfb1\kidQc.dat'  
    # filters created by kidfilter.py
    path_filtergeometry = r'C:\Users\sebastian\Documents\deshima\pycad\clepywin\chip\msfb1\filter_geometry_final.dat'
#    filtkid kids
    F0 = 317e9
    FN = 377e9
    Ql = 500.
    def Fnext(Fi, Q):
        return Fi * (1 + 1/(2*Q)) / (1 - 1/(2*Q))
    Ffilt = [F0]
    Fi = F0
    while Fi < FN:
        Fi = Fnext(Fi, Ql)
        Ffilt.append(Fi)
    def kidgenerator(epsms, epsal, epsw, Ffilt):
        # LENGTHS
        lal = 1.4e-3
        lms = 110e-6
        lms_bb_c = 24e-6
        lms_bb_stub = 37e-6
        lms_bb_mis = 34e-6
        #KID FREQUENCIES
        F0 = 4.1e9
        Fgap = 5e9
        delgap = 0.1e9
        FN = 5.9e9
        #KID Qc values
        Qc = 100e3
        Qcblind = 100e3
        #NUM KIDS
        Nbb = 2
        Nfilt = len(Ffilt)
        Npure = 6 #outside readout band, noise with vna
        Nblind = 2      
        N = Nbb + Nfilt + Nblind
        Ffilt.reverse()
#        kids =  mw.KIDSdesign(F0, FN, N, epsal, lal, epsms, lms, epsw, Ffilt, Nblind, Fgap = Fgap, delgap = delgap, lms_broad_c = lms_bb_c, lms_broad_stub = lms_bb_stub, lms_broad_mis = lms_bb_mis)
        kids = newKD.KIDSdesign(F0, FN, N, epsal, lal, Zcpw, epsms, lms, Zms, epsw, Ffilt, Nblind, Fgap = Fgap, delgap = delgap, lms_broad_c = lms_bb_c, lms_broad_stub = lms_bb_stub, lms_broad_mis = lms_bb_mis, lms_rturn = r_turn*1e-6)
        kids.shuffle(mode = 2)
        # Qc to Lc calc
        # generate coupling lengths for kids in original F-position
        kids.gen_lcouple(path_Qc, Qc, Qcblind)
        return kids, Nblind + Npure
    kids, num_blind = kidgenerator(epsms, epsal, epsw, Ffilt)

    
#    PURE KIDS
    #Wide    
    def purekid_generator(epsms, epsal, epsw):
        lal = 0
        lms = 0        
        #KID FREQUENCIES
        F0 = 6.5e9
        FN = 7.5e9
        #KID Qc values
        Qc = 20e3
        Qcblind = 100e3
        #NUM KIDS
        Nbb = 0
        Nfilt = 0 
        Nblind = 6     
        N = Nbb + Nfilt + Nblind
        Ffilt = []
#        pureNbTiN =  mw.KIDSdesign(F0, FN, N, epsal, lal, epsms, lms, epsw, Ffilt, Nblind)    
        pureNbTiN =  newKD.KIDSdesign(F0, FN, N, epsal, lal, Zcpw, epsms, lms, Zms, epsw, Ffilt, Nblind)
        pureNbTiN.gen_lcouple(path_Qc, Qc, Qcblind)
        return pureNbTiN
    purekids = purekid_generator(epsms, epsal, epsw)

    
    purekids.add_custom(kids.blind[0])
    purekids.add_custom(mw.pureWide(purekids.F[0], purekids.eeff_wide))
    purekids.add_custom(mw.pureHybrid(purekids.F[1], purekids.eeff_al, purekids.eeff_wide, 2*purekids.lcouple[1]*1e-6))    
    purekids.add_custom(mw.pureMS(purekids.F[2], purekids.eeff_wide, purekids.eeff_ms, 2*purekids.lcouple[2]*1e-6))  
    purekids.add_custom(kids.blind[1])    
    purekids.add_custom(mw.pureWide(purekids.F[3], purekids.eeff_wide))
    purekids.add_custom(mw.pureHybrid(purekids.F[4], purekids.eeff_al, purekids.eeff_wide, 2*purekids.lcouple[4]*1e-6))
    purekids.add_custom(mw.pureMS(purekids.F[5], purekids.eeff_wide, purekids.eeff_ms, 2*purekids.lcouple[5]*1e-6))
  
#    COUPLING 
    l_kidQ_c = kids.lcouple
    l_pureQ_c = np.concatenate(([kids.blind[0].lcouple], purekids.lcouple[0:3], [kids.blind[1].lcouple], purekids.lcouple[3:6]))
#    l_pureQ_c = np.array([kids.blind[0].lcouple, purekids.lcouple[0:3], kids.blind[0].lcouple, purekids.lcouple[3:6]]).flatten()
    d_kidQ_c = 6 
#%%
    
#==============================================================================
# Filtergeometry
#==============================================================================
# fixed horizontal length on both sides of coupling length 
#   filtkid filters
    num_filtkid = len(kids.filtered)
    
    # Load data from sonnet simulations for filter geometry
    fdat_filters = np.loadtxt(path_filtergeometry).transpose()
    # get header info (specifically lc_frac)
    with open(path_filtergeometry, 'r') as readfile:
        header = readfile.readlines()
    # corner radius
    r_filter = r_turn
    if not r_filter ==  float(header[5].split()[1]):
        print 'WARNING: different microstrip radii are defined'
    lr_filter = r_filter*np.pi/2 
    # Get filterkid lc and lv from filedata
    # TODO : THESE ARE TEMP VALUES
    lc_frac = float(header[1].split()[1])
    lres_shift = float(header[4].split()[1])
    lstub_shift = float(header[7].split()[1])
#    lc_frac = 0.3
#    l_filter_c = np.array([kf.lambThz*1e6/2. * lc_frac for kf in kids.filtered])
#    l_filter_v = np.array([kf.lambThz*1e6/2. * (1 - lc_frac) - 2*lr_filter for kf in kids.filtered])
#    lc_frac = float(header[1].split()[1])
#    l_filter_c = np.array([fdat_filters[1][np.where(fdat_filters[0] == f)] for f in kids.filters.F]).flatten()
#    l_filter_v = np.array([fdat_filters[2][np.where(fdat_filters[0] == f)] for f in kids.filters.F]).flatten()

#    coupling distances
    d_filter_c = 1.1
    d_broadband_c = 0.8
    
#    space between filters
    d_filter_space = 5/4.*kids.lambThz[np.where(kids.lambThz > 0)]*1e6
    kids.filters.set_geometry_fractions(lres_shift,
                                        lc_frac,
                                        lstub_shift,
                                        d_filter_c,
                                        r_filter)  
    

#==============================================================================
#   Meander geometry / KID distances at transmission line
#==============================================================================
#    distances between broadband kids starting from labyrinth
    dx_bb = 0.2e3 #this is currently set in delayline function
    d_bb = np.array([0.3e3, 0.3e3])
    y_meander_chipend = 1.2e3   


    
#==============================================================================
# Some console feedback
#==============================================================================
    print 'Some info:'
    print kids
    print kids.filters
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
# Write logfiles
#==============================================================================
    filename_kids = filename[:-4] + '_kids.txt'
    filename_geometry = filename[:-4] + '_geo.txt'
    filename_filters = filename[-4:] + '_filters.txt'
    
    with open(filename_kids, 'w') as writefile:
        writefile.write(str(kids))
        writefile.write(str(purekids))
        
    with open(filename_geometry, 'w') as writefile:
        pass
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
#    rot(1j)
#    flip('x')
#==============================================================================
# includebase chip layout, everything that is common between chips of this layout
#==============================================================================
    msloc_base(layers, w_msl, w_sin, mesh, True)
    
    layername('Hybrids')
    gomark('chip00')
    go(0, 2e3)
    text(1, 'MSCPWFB1', height = 0.5e3)
    go(0, -1e3)
    text(1, 'Sebastian Haehnle 10.2016', height = 0.25e3)
#    
##==============================================================================
##   draw filterbank    
##==============================================================================
    gomark('labyend')
    lhoriz = 1  
# first BB-KID
    layername('MSline')   
    jj = 0
    msl_sCurve(w_msl, d_bb[jj], 1.5e3, mesh, w_sin, r_msl)
    msloc_kid_v2(kids.broadband[jj], w_hybrid, s_hybrid, w_wide, s_wide, w_msl, d_broadband_c, lhoriz, r_filter, mesh, w_sin)
    jj+=1
#    possible to draw upward section entering meander section
    msl_delayline_up(w_msl, d_bb[jj-1], 0, mesh, w_sin, r_msl)
#    msloc_kid_v2(kids.broadband[jj], w_hybrid, s_hybrid, w_wide, s_wide, w_msl, d_broadband_c, lhoriz, r_filter, mesh, w_sin)
#    jj += 1
#
#    
    for i, i_kid in enumerate(kids.filtered):
        setmark('filtkid'+str(i))
        setmark('thzwire')
#        end of transmission line section is x-position of top-right KID corner!!! Filter + KID is drawn downward
        lhoriz = (i_kid.filt.lres/2.-i_kid.filt.lc)*1e6
        xoffset = lhoriz + r_filter + 0
        layername('MSline') 
        wirego(1, d_filter_space[i], w_msl)
#        move by coupling distance and offset filter from vertical KID CPW
        go(-xoffset, -(w_msl + d_filter_c))
#        draw filter and KID
        c_filter_msl_v1(w_msl, r_filter, i_kid.filt.lc*1e6, i_kid.filt.lv*1e6, mesh, w_sin)
        msloc_kid_v2(i_kid, w_hybrid, s_hybrid, w_wide, s_wide, w_msl, d_filter_c, lhoriz, r_filter, mesh, w_sin)
#        Draw SiN layers taking KID geometry into account
        layername('SiNdiel')
        gomark('filtkid'+str(i))
        wire(1, dist2mark('short')[0]-w_sin/2., w_sin)
        layername('SiNwafer')
        gomark('filtkid'+str(i))
        wire(1, d_filter_space[i], 2*(w_sin))
#        Move to end of this section
        gomark('filtkid'+str(i))
        go(d_filter_space[i], 0)
#
#    Draw bb-KID directly after filterbank
    msl_delayline_up(w_msl, d_bb[jj], 0, mesh, w_sin, r_msl)
    msloc_kid_v2(kids.broadband[jj], w_hybrid, s_hybrid, w_wide, s_wide, w_msl, d_broadband_c, lhoriz, r_filter, mesh, w_sin)
    jj+=1
    setmark('lastKID')
##    draw upward section entering meander section
#    msl_delayline_up(w_msl, d_bb[jj], 0, mesh, w_sin, r_msl)
#    msloc_kid_v2(kids.broadband[jj], w_hybrid, s_hybrid, w_wide, s_wide, w_msl, d_broadband_c, lhoriz, r_filter, mesh, w_sin)
#    jj += 1
#        
#    
#==============================================================================
#   Readoutline section
#==============================================================================
    if True:
        def endpos_kids():
            ocd = []
            for k, v in gg.mark.items():
                if 'KIDend' in k:
                    ocd.append([v[0][0], v[0][1], k, int(k.strip('KIDend'))])
    #        ocd = sorted(ocd, key = lambda x: x[0])
            ocd.reverse()
            return ocd
        kidpos = endpos_kids()
            
        layername('MSgnd', layers)
        gomark('bondpadtop')
        msloc_bondpad(w_ro, s_ro, w_sin)
        ro_go(-1, x_ro_chipend - r_ro, w_ro, s_ro, bridgefun)
    #    cpwupgo(-1, r_ro, w_ro, s_ro, mesh)
        ro_upgo(-1, r_ro, w_ro, s_ro, mesh, bridgefun)
        ro_go(-1j, y_ro_far, w_ro, s_ro, bridgefun)
        ro_downgo(-1j, r_ro, w_ro, s_ro, mesh, bridgefun)
        setmark('ro_topright')
        
        # here is the section with automatic readout connection to KID instead of the go() command
        for pos in kidpos:
            msloc_readout_attachright(pos[2], l_kidQ_c[pos[3]], d_kidQ_c, w_wide, s_wide, w_ro, s_ro, r_ro, mesh, bridgefun, False)
        setmark('ro_topleft')
#
#
##==============================================================================
## Termination of THZ line    
##==============================================================================
    if True:
        gomark('lastKID')
        distkeeper = 0.5e3
        msgo(1, dx_bb, w_msl, w_sin)
        msdowngo(1, r_msl, w_msl, mesh, w_sin)
        msgo(-1j, r_msl, w_msl, w_sin)
        
        
        term_space = np.array([dist2mark('ro_topright')[0], dist2mark('ro_topright')[1]]) - distkeeper
        msloc_linetermination(w_msl, w_sin, w_transformer, s_transformer, l_transformer, w_terminator, s_terminator, l_terminator, r_msl, term_space, mesh)
        print 'You are terminated'
#
#==============================================================================
# Blind KID section 
#==============================================================================
    if True:
        gomark('bondpadbot')
        msloc_bondpad(w_ro, s_ro, w_sin)
        # Space for blind kids  
        dist_blind_ro = 500
        dy_blind = dist2mark('ro_topleft')[1] - 2*r_ro - dist_blind_ro
        dx_blind1 = (dist2mark('labyend')[0] - d_laby - r_ro)        
        num_blind = len(purekids.custom)
        multisect = True
        if multisect:    
            dx_blind1 = dx_blind1/2. -(4*r_ro)/2.
            dx_blind2 = dx_blind1
            num_blind /= 2
    #bondpad to first blind section
        ro_go(-1, dx_blind1, w_ro, s_ro, bridgefun)
        ro_downgo(-1, r_ro, w_ro, s_ro, mesh, bridgefun)    
        for i, pp in enumerate(purekids.custom[:num_blind]):
            i = i - len(kids.blind)
            if pp.mode == -1:
                ii = pp.i
            else:
                ii = len(kids.notblind) + i
            ii = len(kids.notblind) + i
            setmark('outer')
            offset_x = 4*r_ro+pp.ltot*1e6 + l_pureQ_c[i]
            go(offset_x, dy_blind/num_blind)
            rot(-1j)
            if pp.mode == -1:
                msloc_kid_v2(pp, w_hybrid, s_hybrid, w_wide, s_wide, w_msl, 0, lhoriz, r_filter, mesh, w_sin, kidid = ii)
            elif pp.mode == -2:
                msloc_pureWide(pp, ii, pp.lwide*1e6, w_wide, s_wide)
            elif pp.mode == -3:
                msloc_pureHyb(pp, ii, pp.lwide*1e6, pp.lhyb*1e6, w_wide, s_wide, w_hybrid, s_hybrid, w_sin)
            elif pp.mode == -4:
                msloc_pureMS(pp, ii, pp.lwide*1e6, pp.lms*1e6, w_wide, s_wide, w_msl, w_sin)
            layername('MSgnd')
            gomark('outer')
            rot(-1j)
            msloc_readout_attachright('KIDend'+str(ii), l_pureQ_c[i], d_kidQ_c, w_wide, s_wide, w_ro, s_ro, r_ro, mesh, bridgefun, False)
            rot(1j)
        if multisect:
    #first section 180 structure
    #        cpwgo(1j, dist2mark('ro_topleft')[1] - dist_blind_ro - r_ro, w_ro, s_ro)
            ro_upgo(1j, r_ro, w_ro, s_ro, mesh, bridgefun, bridge = False)
            ro_upgo(-1, r_ro, w_ro, s_ro, mesh, bridgefun)    
            ro_go(-1j, dist2mark('bondpadbot')[1]-r_ro, w_ro, s_ro, bridgefun)
            ro_downgo(-1j, r_ro, w_ro, s_ro, mesh, bridgefun)
            ro_go(-1, dx_blind2, w_ro, s_ro, bridgefun)
            ro_downgo(-1, r_ro, w_ro, s_ro, mesh, bridgefun) 
            for i, pp in enumerate(purekids.custom[num_blind:]):
                i = i - len(kids.blind) + num_blind
                if pp.mode == -1:
                    ii = pp.i
                else:
                    ii = len(kids.notblind) + i
                ii = len(kids.notblind) + i
                setmark('outer')
                offset_x = 4*r_ro+pp.ltot*1e6 + l_pureQ_c[i]
                go(offset_x, dy_blind/num_blind)
                rot(-1j)
                if pp.mode == -1:
                    msloc_kid_v2(pp, w_hybrid, s_hybrid, w_wide, s_wide, w_msl, 0, lhoriz, r_filter, mesh, w_sin, kidid = ii)
                elif pp.mode == -2:
                    msloc_pureWide(pp, ii, pp.lwide*1e6, w_wide, s_wide)
                elif pp.mode == -3:
                    msloc_pureHyb(pp, ii, pp.lwide*1e6, pp.lhyb*1e6, w_wide, s_wide, w_hybrid, s_hybrid, w_sin)
                elif pp.mode == -4:
                    msloc_pureMS(pp, ii, pp.lwide*1e6, pp.lms*1e6, w_wide, s_wide, w_msl, w_sin)
                layername('MSgnd')
                gomark('outer')
                rot(-1j)
                msloc_readout_attachright('KIDend'+str(ii), l_pureQ_c[i], d_kidQ_c, w_wide, s_wide, w_ro, s_ro, r_ro, mesh, bridgefun, False)
                rot(1j)
    # connect to filterbank readout
        ro_go(1j, dist2mark('ro_topleft')[1]-r_ro, w_ro, s_ro, bridgefun)
        ro_downgo(1j, r_ro, w_ro, s_ro, mesh, bridgefun)
        ro_go(1, dist2mark('ro_topleft')[0], w_ro, s_ro, bridgefun)
        
#==============================================================================
# Final touches    
#==============================================================================
    outroScript(1)
    # write to file
    writeScript(filename)
    
#    print gg.cle
#    print gg.s
    

#if __name__ == '__main__':
#    main()