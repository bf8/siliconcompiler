import siliconcompiler

def make_docs():
    '''A flow for running LVS/DRC signoff on a GDS layout.

    Inputs must be passed to this flow as follows::

        chip.set('read', 'gds', 'extspice', '0', '<path-to-layout>.gds')
        chip.set('read', 'netlist', 'lvs', '0', '<path-to-netlist>.vg')
        chip.set('read', 'gds', 'drc', '0', '<path-to-layout>.gds')
    '''
    chip = siliconcompiler.Chip()
    chip.set('flow', 'signoffflow')
    setup(chip)
    return chip

def setup(chip):
    flow = 'signoffflow'

    # nop import since we don't need to pull in any sources
    chip.node(flow, 'import', 'nop')

    chip.node(flow, 'extspice', 'magic')
    chip.node(flow, 'drc', 'magic')
    chip.node(flow, 'lvs', 'netgen')
    chip.node(flow, 'signoff', 'join')

    chip.edge(flow, 'import', 'drc')
    chip.edge(flow, 'import', 'extspice')
    chip.edge(flow, 'extspice', 'lvs')
    chip.edge(flow, 'lvs', 'signoff')
    chip.edge(flow, 'drc', 'signoff')

    chip.set('mode', 'asic')

    chip.set('showtool', 'def', 'klayout')
    chip.set('showtool', 'gds', 'klayout')

    # Set default goal
    for step in chip.getkeys('flowgraph', flow):
        chip.set('metric', step, '0', 'errors', 'goal', 0)

