# -*- coding: utf-8 -*-

from PyClewin import *

import numpy as np


def main(standalone = True, filename = '', layers = {}):
    """
    template for FP multiline chip with 4 antennas using 2mm square lens array. If this is used in a multichip script (standalone == False), layers must contain a dict defining the names for the following layers:
    """

    filename = filename or 'Fabryperot_multiline.cif'

    if standalone:
        layers = collections.OrderedDict()
        layers['SiN_wafer'] = '0f00ffcb'
        layers['NbTiN_GND'] =  '0ff00ff00'
        layers['SiN_backside'] = '0f00cbff'
        layers['Aluminum'] = '0fff0000'
        layers['Polyimide'] = '0ff0f000'
        layers['NbTiN_line'] = '0ff0000ff'
        layers['text'] = '05000000'
        layers['dummy'] = '05fefefe'
        # Define the base unit for all lengths in the design
        unit_scale = 1e3    # micron
        mesh = 36
        gg.scale = unit_scale
        # Write script intro
        introScript()
        introLayers()
        for i, k in enumerate(layers):
            addLayer(i, k, layers[k])

        symbols = {1 : 'Main'}
        introSymbols()
        defineSymbol(*symbols.items()[0])
    else:
        assert 'text' in gg.layers
        assert 'NbTiN_GND' in gg.layers
        assert 'Aluminum' in gg.layers

    # Define wafer
    t_wafer = 375

    # Define THz line
    thz_line = parts.CPWs.CPW(2,2, mesh, R = 500, gndlayer = 'NbTiN_GND')
    space_line = 100


    # Define Antenna and Lens
    thz_freq = 350e9
    antenna = parts.Antennas.LeakyM4002(1.1e3, t_wafer, 'SiN_backside', centerline = 10)
    r_lens = 1e3 # Lens size

    # Define Fabry Perots
    l_fp = 10e3
    l_fp_nobridge = 0.5e3
    d_tunnel = 2e3
    space_fp = 1e3 # Distance between FP lines on y-axis
    l_deltabridge = 500 # DUMMY, lambda/4 spacing or other spacing


    d_coupler = 10 # dummy, this is a placeholder for coupler part
    fp_lines = [parts.CPWs.CPW(2,2, mesh, R = 500, gndlayer = 'NbTiN_GND'),
                parts.CPWs.CPWwithBridge(2, 2, mesh, 500, 'NbTiN_GND',
                                         parts.Bridges.Bridge('Polyimide', 'Aluminum', 30.0, 40.0, 65.0, 20.0),
                                         bridgeDistance = l_deltabridge),
                parts.CPWs.CPWwithBridge(2, 2, mesh, 500, 'NbTiN_GND',
                                         parts.Bridges.Bridge('Polyimide', 'NbTiN_line', 30.0, 40.0, 65.0, 20.0),
                                         bridgeDistance = l_deltabridge),
                parts.CPWs.CPWwithBridge(2, 2, mesh, 500, 'NbTiN_GND',
                                         parts.Bridges.Bridge('Polyimide', 'dummy', 30.0, 40.0, 65.0, 20.0),
                                         bridgeDistance = l_deltabridge)
            ]


    # Define KIDs
    l_kid = 5e3 # dummy, Define this dynamically by KID part
    line_hybrid = parts.CPWs.CPWhybrid(2, 2, 'Aluminum', 'NbTiN_GND', mesh, 20)
    line_wide = parts.CPWs.CPW(10, 6,  mesh, 20, gndlayer = 'NbTiN_GND')
    line_coupler = parts.CPWs.CPW(10, 6,  mesh, 20, gndlayer = 'NbTiN_GND')

    kid_full = parts.KIDs.Hybrid(line_hybrid, line_wide, line_coupler,
                                 parts.Transitions.transHybridWideM4000, None,
                                 short_length = 0,
                                 shape = 'straight')

    kid_lengths = np.array([[1e3, 4e3, 0.2e3],
                   [1.1e3, 3.9e3, 0.2e3],
                   [1.2e3, 3.8e3, 0.2e3],
                   [1.3e3, 3.7e3, 0.2e3],])
    kid_lengths_blind = np.array([[1e3, 4e3, 0.2e3],
                   [1.1e3, 3.9e3, 0.2e3],
                   [1.2e3, 3.8e3, 0.2e3],
                   [1.3e3, 3.7e3, 0.2e3],])
    kid_coupler_distance = 10

    # Define Readoutline
    space_chipedge = 5e3
    ro_line = parts.CPWs.CPWreadout(20, 10, mesh, 100, 'NbTiN_GND', 'SiN_wafer',
                                    parts.Bridges.Bridge('Polyimide', 'Aluminum', 30.0, 40.0, 65.0, 20.0),
                                    bridgeDistance = 2e3)
    ro_coupler = parts.Readout.couplerDeshima(kid_coupler_distance, 300, line_coupler, ro_line)


    # Define base chip layout. Draws in 'text' layer, adds markers
    parts.Chipbasis.Deshima42x14(layers)

    # 4 antenna centers
    antenna_marks = ['antenna_1', 'antenna_2', 'antenna_3', 'antenna_4']
    layername('text')
    p = gg.mark['antenna'][0]
    moveto(p[0]-r_lens, p[1]+r_lens)
    circle(r_lens)
    setmark('antenna_1')
    moveto(p[0]+r_lens, p[1]+r_lens)
    circle(r_lens)
    setmark('antenna_2')
    moveto(p[0]-r_lens, p[1]-r_lens)
    circle(r_lens)
    setmark('antenna_3')
    moveto(p[0]+r_lens, p[1]-r_lens)
    circle(r_lens)
    setmark('antenna_4')

    # 4 Tunnel input positions
    tunnel_marks = ['tunnelin_1', 'tunnelin_2', 'tunnelin_3', 'tunnelin_4']
    l_tunnel = 4e3
    p = gg.mark['tunnelin'][0]
    moveto(p[0], p[1] + 0.5*space_line)
    setmark('tunnelin_1')
    moveto(p[0], p[1] - 0.5*space_line)
    setmark('tunnelin_2')
    moveto(p[0], p[1] + 1.5*space_line)
    setmark('tunnelin_3')
    moveto(p[0], p[1] - 1.5*space_line)
    setmark('tunnelin_4')

    fp_marks = ['fpin_1', 'fpin_2', 'fpin_3', 'fpin_4']
    print tunnel_marks
    # 4 FP inputs
    gomark(tunnel_marks[2])
    go(l_tunnel + d_tunnel, 0)
    setmark('fpin_1')
    go(0, - space_fp)
    setmark('fpin_2')
    go(0, - space_fp)
    setmark('fpin_3')
    go(0, - space_fp)
    setmark('fpin_4')


    # Draw stuff
    for ii in xrange(len(antenna_marks)):
        ### Antenna
        gomark(antenna_marks[ii])
        # Check whether antenna is on left or right side of array
        if x2mSigned('antenna') > 0:
            direction = -1
        else:
            direction = 1
        print antenna_marks[ii], direction
        antenna.draw(direction, thz_line)
        # Check whether antenna is on bottom or top side of array
        if y2mSigned('antenna') > 0:
            l_delta = space_line
        else:
            l_delta = 0
        ### Antenna -> Tunnel
        thz_line.wirego(direction, r_lens+l_delta)
        # manual method, check where we are
#        if direction == 1:
#            thz_line.upgo(1)
#        elif direction == -1:
#            pass
#            thz_line.downgo(-1)
#        thz_line.wirego(1j, y2m(tunnel_marks[ii]) - thz_line.R)
#        thz_line.downgo(1j)
        # auto connector
        thz_line.connect(base.connector(1, tunnel_marks[ii]))
        # Path through tannel
        thz_line.wirego(1, x2m(tunnel_marks[ii])+l_tunnel)
        setmark('tunnelout_%d' % ii)

    ### Safety if antenna and fp numbering are not 1-1
    y_positions = []
    for k, v in gg.mark.items():
        if 'tunnelout_' in k:
            y_positions.append(v[0][1])
    sorted_ids = np.argsort(y_positions)[::-1]

    for ii, id in enumerate(sorted_ids):
        ### Tunnel -> FP
        gomark('tunnelout_%d' % id)
        print ii, id
        thz_line.wirego(1, (len(antenna_marks)-ii)*space_line)
        if not np.isclose(y2m(fp_marks[ii]), 0):
            # Draw S-shape to get to FP level, only if tunnel output height is not equal to fp input height
            thz_line.downgo(1)
            thz_line.wirego(-1j, y2m(fp_marks[ii])-thz_line.R)
            thz_line.upgo(-1j)
        thz_line.wirego(1, x2m(fp_marks[ii]))
        ### Coupler 1
        base.layername('text')
        base.wirego(1, d_coupler, 20)
        ### FP Section
        base.layername('NbTiN_GND')
        fp_lines[ii].wirego(1, l_fp_nobridge, bridgesOff = True)
        fp_lines[ii].wirego(1, l_fp - 2*l_fp_nobridge, bridgeStart = True)
        fp_lines[ii].wirego(1, l_fp_nobridge, bridgesOff = True)
        ### Coupler 2
        base.layername('text')
        base.wirego(1, d_coupler, 20)
        ### KIDs
        base.layername('NbTiN_GND')
        kid_full.draw(1, *kid_lengths[ii], kid_id = ii)

    ### Blind KIDS custom position
    gomark('fpin_4')
    go(l_fp, -1*space_fp)
    for ii in xrange(len(kid_lengths_blind)):
        base.layername('NbTiN_GND')
        setmark('chiplevel local')
        kid_full.draw(1, *kid_lengths_blind[ii], kid_id = len(kid_lengths) + ii)
        gomark('chiplevel local')
        go(0, -1e3)

    ### Readoutline
    gomark('bondpadtop')
    parts.Readout.bondpadM4001(1, ro_line, x2m('chipFF'))
    gomark('bondpadtop')
    ro_line.wirego(-1, space_chipedge)
    ro_line.direction
    ro_line.turngo(0, -1j)

    for kid_id in xrange(len(sorted_ids)):
#        ro_coupler.draw(-1j, -1, 'KID_coupler_%d' % kid_id, kid_lengths[:,2][kid_id])
        ro_coupler.connect(kid_full, kid_id, ro_line.direction, kid_lengths[:,2][kid_id])
    for kid_id in xrange(len(kid_lengths_blind)):
        kid_id_full = kid_id + len(kid_lengths)
        ro_coupler.connect(kid_full, kid_id_full, ro_line.direction, kid_lengths_blind[:,2][kid_id])
#        ro_coupler.draw(-1j, -1, 'KID_coupler_%d' %kid_id_full, kid_lengths_blind[:,2][kid_id], debug = True)

    ro_line.connect(base.connector(1, 'bondpadbot'))
#    ro_line.wirego(0, y2m('bondpadbot')-ro_line.R)
#    ro_line.turngo(0, 1)
#    ro_line.wirego(0, x2m('bondpadbot'))
    parts.Readout.bondpadM4001(1, ro_line, x2m('chipFF'))


    if standalone:
        base.outroScript(symbols.keys()[-1])
        # write to file
        base.writeScript(filename)
    return kid_full


if __name__ == '__main__':
#    rot(1j)
    foo = main(standalone = True)
