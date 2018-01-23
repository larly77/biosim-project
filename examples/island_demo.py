# -*- coding: utf-8 -*-

"""
A demo of a very small island over many years
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen', 'Lars Martin Boe Lied'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no',\
            'lars.martin.boe.lied@nmbu.no'

import biosim.simulation as simu
from biosim.landscape import Jungle
import textwrap

if __name__ == '__main__':

    isle_map = """\
              OOOOOO
              OJJMJO
              OJJSSO
              OSSDDO
              ODDDDO
              OOOOOO"""
    isle_map = textwrap.dedent(isle_map)

    ini_herbs = [{'loc': (3, 3),
                  'pop': [{'species': 'Herbivore',
                           'age': 3,
                           'weight': 14}
                          for _ in range(80)]}]
    ini_carns = [{'loc': (5, 5),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 25}
                          for _ in range(15)]}]

    sim = simu.BioSim(isle_map, ini_pop=ini_herbs+ini_carns, seed=12345)
    sim.set_axis_limits(y_limits=(0, 1200))
    sim.simulate(num_steps=50, vis_steps=1)

    Jungle.set_parameters({'f_max': 3000})   # Adds super fertiliser to jungle
    sim.set_axis_limits(y_limits=(0, 2400))
    sim.simulate(num_steps=500, vis_steps=5)

    input('Press Enter')
