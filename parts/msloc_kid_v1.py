# -*- coding: utf-8 -*-
"""
Created on Tue Sep 06 16:39:44 2016

@author: sebastian
"""

from clepywin import *
import numpy as np
import collections

# GLOBALS
# Tapering for transition functions
LTAPER = 12
LSIN = 3
LOVERLAP = 7

# define shorts
LSHORT = 10
LPRE = 0
WSHORT = 1.4 + 0.2




def msloc_kid_v2(kid, whyb, shyb, wwide, swide, wmsl, dc, lhoriz, rturn, mesh, wsin, kidid = None, wmsl2 = 1.6):
    '''
    v1 completely outdated, deleted it
    '''
#==============================================================================
# Get parameters from KID    
#==============================================================================
    lal = kid.lal*1e6
    lwide = kid.lwide*1e6    
    if kid.mode == 1:
        lambthz = kid.filt.lamb*1e6
        lres = kid.filt.lres*1e6
        lc = kid.filt.lc*1e6
        
        lmis = 3./4.*lambthz
        lhoriz = lres/2.-lc
    elif kid.mode == 0:
        lmsl_couple = kid.parent.lms_broad_c*1e6
        lmsl_stub = kid.parent.lms_broad_stub*1e6
        lmsl_mismatch = kid.parent.lms_broad_mis*1e6
      
    elif kid.mode == -1:
        lmsl = kid.lms*1e6
#==============================================================================
# Variable definitions for tapering and short lengths   
#==============================================================================
#   length of line on gnd plane
    lshort = LSHORT
    lturn = rturn*np.pi/2.
#    define tapers and all that jazz
    taper_l_almsl = 12. # length of taper
    taper_l_alwide = 21. #length of taper
    delsi = wsin/2.
    wsin_waf = 2*wsin 
    l_siwaf = 21.
#    delsi_trans defined previously, included in transitiontaper length
   
#==============================================================================
#   draw all the things,
#==============================================================================
    
#==============================================================================
#  Microstrip section depends on KID type
#==============================================================================
    layername('MSline')
    # with filter
    if kid.mode == 1:
        setmark('inner')
        go(0, -(wmsl + dc)) 
        setmark('temp') 
#        filtered kid
    #    draw lambda/4 stub and short end of KID
        wirego(-1, lhoriz + lc + rturn, wmsl)
        turnupgo(-1, rturn, wmsl, mesh)
        wirego(-1j, lres - lturn - (rturn + lc + lhoriz) , wmsl)
        short_msl(-1j, wmsl, wsin)
        gomark('temp')
    #    draw msl towards hybrid, adjust length to correct resonance
        wirego(1, lhoriz, wmsl)
        turndowngo(1, rturn, wmsl, mesh)
        wirego(-1j, lmis - (lturn + lhoriz), wmsl)
#        Draw SiN
        layername('SiNdiel')
        delsi_x = dist2mark('short')[0]
        delsi_y2 = dist2mark('thzwire')[1] + wsin/2.
        delsi_y1 = dist2mark('short')[1]
        six = [delsi, delsi, -(delsi_x + delsi), -(delsi_x + delsi), -wsin/2., -wsin/2.] 
        siy = [0, delsi_y2, delsi_y2, delsi_y1, delsi_y1, 0]
        sixy = np.array([six, siy])
        poly(sixy)
        transition_mslhyb(wmsl, whyb, shyb, wsin, taper_l_almsl)
        
    # broadband
    elif kid.mode == 0:
        setmark('inner')
        go(0, -(wmsl + dc)) 
        setmark('temp')
        wirego(-1, lmsl_couple, wmsl)
        turnupgo(-1, rturn, wmsl, mesh)
        wirego(-1j, lmsl_stub, wmsl)
        short_msl(-1j, wmsl, wsin)
        gomark('temp')
        turndowngo(1, rturn, wmsl, mesh)
        wirego(-1j, lmsl_mismatch, wmsl)
        layername('SiNdiel')
        delsi_x = dist2mark('short')[0]
        delsi_y2 = dist2mark('thzwire')[1] - wsin/2.
        delsi_y1 = y2mSigned('short')
#        if lmsl_stub > lmsl_mismatch:
#            delsi_y1 = dist2mark('short')[1]
#        else:
#            delsi_y1 = - dist2mark('short')[1]
        six = [delsi, delsi, -(delsi_x + delsi), -(delsi_x + delsi), -wsin/2., -wsin/2.] 
        siy = [0, delsi_y2, delsi_y2, delsi_y1, delsi_y1, 0]
        sixy = np.array([six, siy])
        poly(sixy)
        transition_mslhyb(wmsl, whyb, shyb, wsin, taper_l_almsl, wmsl2 = wmsl2)
    # blind
    elif kid.mode == -1:
        setmark('inner')
        # for blind kid, outer mark is set outside. A bit weird...
        short_msl(1j, wmsl, wsin)
        layername('MSline')
        msgo(-1j, lmsl, wmsl, wsin)
        transition_mslhyb(wmsl, whyb, shyb, wsin, taper_l_almsl, wmsl2 = wmsl2)
        
#==============================================================================
#     Hybrid section
#==============================================================================
    layername('Hybrids')
    setmark('temp')
    wire(-1j, lal, whyb)
    layername('MSgnd')
    wirego(-1j, lal, whyb + 2*shyb)
    transition_hybwide(whyb, shyb, wwide, swide, taper_l_alwide)
    
#==============================================================================
#     wide section    
#==============================================================================
    layername('MSgnd')
    cpwgo(-1j, l_siwaf, wwide, swide)
#    Draw SiNwafer part
    layername('SiNwafer')
    if kid.mode == -1:
        wire(1j, dist2mark('inner')[1] + l_siwaf + wsin_waf/2., wsin_waf)        
    else:
        six = [wsin_waf/2., wsin_waf/2., -(dist2mark('short')[0] + wsin_waf/2.), -(dist2mark('short')[0] + wsin_waf/2.)]
        siy = [0, dist2mark('thzwire')[1] - wsin_waf/2., dist2mark('thzwire')[1] - wsin_waf/2., 0]
        poly(np.array([six, siy]))
    layername('MSgnd')
    cpwgo(-1j, lwide - l_siwaf, wwide, swide)    
    wirego(-1j, swide, wwide + 2*swide)
    if kidid:
        setmark('KIDend'+str(kidid))
    else:
        setmark('KIDend'+str(kid.i))
    layername('MSline') 
    gomark('inner')

def short_msl(direction, wmsl, wsin, wshort = None, lshort = None, lpre = None, layer1 = 'MSline', layer2 = 'SiNdiel'):
    if not wshort:
        wshort = WSHORT
    if not lshort:
        lshort = LSHORT
    if not lpre:
        lpre = LPRE
#    rot(direction)
    if lpre:
        msgo(direction, lpre, wmsl, wsin)
#        layername(layer2)
#        wire(1, lpre, wsin)
#        print lpre, wsin
#        layername(layer1)
#        broadengo(1, lpre, wmsl, wshort)
    setmark('short')
    layername(layer1)
    wire(direction, lshort, wshort)
#    rot(np.conjugate(direction))

def transition_mslhyb(wmsl, whyb, shyb, wsin, ltaper = None, lsin = None, loverlap = None,wmsl2 = 1.6, layer0 = 'MSgnd', layer1 = 'MSline', layer2 = 'SiNdiel', layer3 = 'Hybrids'):
    '''
    drawn downward
    '''
    if not ltaper:
        ltaper = LTAPER
    if not lsin:
        lsin = LSIN
    if not loverlap:
        loverlap = LOVERLAP
    if not wmsl == wmsl2:
        wmsl2 = wmsl2 + manVars.nbtinLine
    woverlap = 2 # more room for processing uncertainties
    lmslonly = ltaper - lsin - loverlap
    if lmslonly < 1:
        print 'WARNING: short connection in mslhyb transition'
    setmark('temp')
    layername(layer0)
    broadengo(-1j, ltaper-loverlap, wmsl, whyb + 2*shyb)
    wire(-1j, loverlap, whyb + 2*shyb)
    gomark('temp')
    layername(layer1)
    broadengo(-1j, lsin+lmslonly, wmsl, wmsl2)
    wire(-1j, loverlap, woverlap) 
    gomark('temp')       
    layername(layer2)
    wire(-1j, lsin, wsin)
    go(0, -(lsin+lmslonly))
    layername(layer3)
    wirego(-1j, loverlap, woverlap)
    
def transition_mslwide(wmsl, wwide, swide, wsin, layer0 = 'MSgnd', layer1 = 'MSline', layer2 = 'SiNdiel'):
    setmark('temp')
    lsin = 4
    loverlap = 7
    ltrans = 21
    lmslonly = 3
    layername(layer1)
    wirego(-1j, lsin + lmslonly + loverlap, wmsl)
    gomark('temp')
    layername(layer0)
    go(0, lsin )
    broaden(-1j, lsin + lmslonly, wmsl, wwide/2.)
    cpwbroadengo(-1j, ltrans, 0, wmsl, wwide, swide)
    
def transition_mslcpw(wmsl, wline, sslot, wsin, ltaper = None, lsin = None, layer0 = 'MSgnd', layer1 = 'MSline', layer2 = 'SiNdiel'):
    '''
    drawn downward
    '''
    if not lsin:
        lsin = LSIN
    if not ltaper:
        ltaper = LTAPER
    setmark('temp')
    layername(layer0)
    broaden(-1j, ltaper, wmsl, wline + 2*sslot)
    layername(layer2)
    wire(-1j, lsin, wsin)
    layername(layer1)
    broadengo(-1j, ltaper, wmsl, wline)
 
   
def transition_hybwide(whyb, shyb, wwide, swide, ltrans, layer0 = 'MSgnd', layer1 = 'Hybrids'):
    setmark('temp')
    layername(layer1)
    wire(-1j, 2./3.*ltrans, whyb)
    layername(layer0)
    broaden(-1j, 1./3.*ltrans, whyb, wwide/2.)
    cpwbroadengo(-1j, ltrans, 0, whyb/2. + shyb, wwide, swide)


def msloc_pureWide(kid, kidid, lwide, wwide, swide, layer0 = 'MSgnd'):
    setmark('inner')
    layername(layer0)
    cpwgo(-1j, lwide, wwide, swide)
    wirego(-1j, swide, wwide + 2*swide)
    setmark('KIDend'+str(kidid))
    gomark('inner')
   
def msloc_pureHyb(kid, kidid, lwide, lhyb, wwide, swide, whyb, shyb, wsin, layer0 = 'MSgnd', layer1 = 'Hybrids', layer2 = 'SiNwafer'):
#    COPY PASTE sin section FROM msloc_kid_v2 !!!!!!!!!!!!!!!!
    wsin_waf = 2*wsin 
    l_siwaf = 21
    taper_l_alwide = 21
#    hybrid section
    setmark('inner')
    layername(layer1)
    setmark('temp')
    wire(1j, LSHORT, whyb)
    wire(-1j, lhyb, whyb)
    layername(layer0)
    wirego(-1j, lhyb, whyb + 2*shyb)
    transition_hybwide(whyb, shyb, wwide, swide, taper_l_alwide)    
#    start wide section
    cpwgo(-1j, l_siwaf, wwide, swide)
#    Draw SiN Wafer part
    layername(layer2)
    wire(1j, dist2mark('inner')[1] + l_siwaf + wsin_waf/2., wsin_waf)    
#    continue wide section    
    layername(layer0)
    cpwgo(-1j, lwide - l_siwaf, wwide, swide)    
    wirego(-1j, swide, wwide + 2*swide)
    setmark('KIDend'+str(kidid))
    gomark('inner')

def msloc_pureMS(kid, kidid, lwide, lmsl, wwide, swide, wmsl, wsin, layer0 = 'MSgnd', layer1 = 'Hybrids', layer2 = 'SiNwafer', layer3 = 'SiNdiel', layer4 = 'MSline'):
#   COPY PASTE sin section FROM msloc_kid_v2 !!!!!!!!!!!!!!!!
    taper_l_alwide = 21 #length of taper
    lshort = 2
    wshort = wmsl     
    delsi = wsin/2.
    wsin_waf = 2*wsin 
    l_siwaf = 21
#    MS section    
    setmark('inner')
    short_msl(1j, wmsl, wsin)
    layername(layer3)
#    go(0, -lshort)
    wire(-1j, lmsl , wsin)
#    go(0, lshort)
    layername(layer4)
#    wirego(-1j, lshort, wshort)
    wirego(-1j, lmsl, wmsl)
#    transition_mslhyb(wmsl, whyb, shyb, wsin, taper_l_almsl)
    transition_mslwide(wmsl, wwide, swide, wsin)
##     Hybrid section
#    layername('Hybrids')
#    setmark('temp')
#    wire(-1j, lhyb, whyb)
#    layername('MSgnd')
#    wirego(-1j, lhyb, whyb + 2*shyb)
#    transition_hybwide(whyb, shyb, wwide, swide, taper_l_alwide)
#    
#     wide section    
    cpwgo(-1j, l_siwaf, wwide, swide)
#    Draw SiN Wafer part
    layername(layer2)
    wire(1j, dist2mark('inner')[1] + l_siwaf + wsin_waf/2., wsin_waf)    
#    continue wide section    
    layername(layer0)
    cpwgo(-1j, lwide - l_siwaf, wwide, swide)    
    wirego(-1j, swide, wwide + 2*swide)
    setmark('KIDend'+str(kidid))
    gomark('inner')

if __name__ == '__main__':
    layers = collections.OrderedDict()
    layers['MSgnd'] =  '0ff00ff00'
    layers['SiNdiel'] = '0f00cbff'
    layers['MSline'] = '0ffffff00'
    layers['Circles'] = '0f808080'
    layers['Hybrids'] = '0fff0000'
    layers['text'] = '0f000000'
