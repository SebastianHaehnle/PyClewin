# -*- coding: utf-8 -*-
"""
Created on Tue Jul 04 14:02:24 2017

@author: sebastian
"""

from clepywin import *

def drawBorders(ldraw, wdraw):
    gomark('chip00')
    go(x2m('chipFF')/2., wdraw/2.)
    bar(1, ldraw[0], wdraw)
    gomark('chip00')
    go(wdraw/2., y2m('chipFF')/2.)
    bar(1j, ldraw[1], wdraw)
    gomark('chipFF')
    go(-x2m('chip00')/2., -wdraw/2.)
    bar(1, ldraw[0], wdraw)
    gomark('chipFF')
    go(-wdraw/2., -y2m('chip00')/2.)
    bar(1j, ldraw[1], wdraw)

def tantalumMesh(chipsize, membraneXYbot, membraneXYtop, ro, kidWide):
    chipsize = np.array(chipsize)
    mr_bondpad = (2e3, 3e3)
    msloc_tantalum_mesh('TantalumBack', d_sq = 14, l_sq = 120)
    layername('TantalumBack')
    # Left bondpad
    gomark('bondpadleft')
    go(-x2m('chip00'), 0)
    wire(1, 2*x2m('bondpadleft'), 2*mr_bondpad[1])
    # Right bondpad
    gomark('bondpadright')
    go(x2m('chipFF'), 0)
    wire(-1, 2*x2m('bondpadright'), 2*mr_bondpad[1])
    # boundary of chip -> thermal coupling
    drawBorders(ldraw = chipsize, wdraw = 1e3)
    # antenna
    gomark('chip00')
    go(*chipsize/2.)
    bar(1, membraneXYbot[0]+20, membraneXYbot[1]+20)
    
    
    msloc_tantalum_mesh('TantalumFront', d_sq = 14, l_sq = 120)
    layername('TantalumFront')
    tol_bp = 3e3
    tol_line = 20*ro.wTotal()
    tol_KID = 20*kidWide.wTotal()
    tol_membrane = tol_KID
    tol_nbtin = 10
#    gomark('bondpadleft')
#    gomark('antenna')
    gomark('chip00')
    go(0, chipsize[1]/2.)
    # define polygon left to right
    taPointsUpper = [[0, tol_bp, 0],
                [x2m('readout_left') + tol_line, tol_bp, 0],
                [x2m('readout_left') + tol_line, -y2m('readout_left') + tol_line, 1],
                [x2m('KIDend2') - tol_KID, -y2m('readout_left') + tol_line, 1],
                [x2m('KIDend2') - tol_KID, membraneXYtop[1]/2. + tol_membrane, 0],
                [x2m('KIDend1') + tol_KID + 200, membraneXYtop[1]/2. + tol_membrane, 0],
                [x2m('KIDend1') + tol_KID + 200, -y2m('readout_left') + tol_line, 1],
                [x2m('readout_right') - tol_line, -y2m('readout_left')+ tol_line, 1],
                [x2m('readout_right') - tol_line, tol_bp, 0],
                [chipsize[0], tol_bp, 0]]
    # define remainder of polygon right to left
    taPointsLower = [[chipsize[0], -tol_bp, 0],
                     [x2m('readout_right') + tol_line, - tol_bp, 1],
                     [x2m('readout_right') + tol_line, -y2m('readout_left') - tol_line, 0],
                     [x2m('readout_left') - tol_line, -y2m('readout_left') - tol_line, 0],
                     [x2m('readout_left') - tol_line, - tol_bp, 1],
                     [0, -tol_bp, 0]]
    
    frontmesh_remove = clePolygon(*(taPointsUpper +  taPointsLower))
    frontmesh_remove.draw()
    
    # ground plane removal where the frontside mesh is
    layername('MSgnd')
    # upper section
    gndPointsUpper = np.array(taPointsUpper + [[chipsize[0], chipsize[1]/2., 0], [0, chipsize[1]/2., 0]])
    gndPointsUpper = gndPointsUpper.transpose()
    gndPointsUpper[2] = [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0]
    gndPointsUpper = gndPointsUpper.transpose()
    
    nbtin_remove_upper = clePolygon(*gndPointsUpper, xlim = [0, chipsize[0]], ylim = [-chipsize[1]/2., chipsize[1]/2.]).scale(-tol_nbtin)
    nbtin_remove_upper.draw()
    
    #lower section
    gndPointsLower = np.array(taPointsLower + [[0, -chipsize[1]/2., 0], [chipsize[0], -chipsize[1]/2., 0]])
    gndPointsLower = gndPointsLower.transpose()
    gndPointsLower[2] = [0, 0, 1, 1, 0, 0, 0, 0]
    gndPointsLower = gndPointsLower.transpose()
    nbtin_remove_lower = clePolygon(*gndPointsLower, xlim = [0, chipsize[0]], ylim = [-chipsize[1]/2., chipsize[1]/2.]).scale(-tol_nbtin)
    nbtin_remove_lower.draw()   