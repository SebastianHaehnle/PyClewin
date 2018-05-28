# -*- coding: utf-8 -*-

from PyClewin import *

def main(standalone = True, filename = '', layers = {}):
    """
    template for FP multiline chip. If this is used in a multichip script (standalone == False), layers must contain a dict defining the names for the following layers:
    """

    filename = filename or 'test.cif'

    if standalone:
        layers = collections.OrderedDict()
        layers['SiN_wafer'] = '0f00ffcb'
        layers['NbTiN_GND'] =  '0ff00ff00'
#        layers['SiNdiel'] = '0f00cbff'
        layers['Aluminum'] = '0fff0000'
        layers['Polyimide'] = '0ff00000'
        layers['NbTiN_line'] = '0ff0000ff'
        layers['text'] = '05000000'
        # Define the base unit for all lengths in the design
        unit_scale = 1e3    # micron
        gg.scale = unit_scale
        # Write script intro
        base.introScript()
        base.introLayers()
        for i, k in enumerate(layers):
            base.addLayer(i, k, layers[k])

        symbols = {1 : 'Main'}
        base.introSymbols()
        base.defineSymbol(*symbols.items()[0])




    parts.Chipbasis.Deshima42x14(layers)




    if standalone:
        base.outroScript(symbols.keys()[-1])
        # write to file
        base.writeScript(filename)


if __name__ == '__main__':
    main(standalone = True)
