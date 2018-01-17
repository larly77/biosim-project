# -*- coding: utf-8 -*-

import textwrap
import matplotlib.pyplot as plt

from biosim.simulation import BioSim
from biosim.landscape import Jungle
from biosim import animals

"""
Compatibility check for BioSim simulations.

This script shall function with biosim packages written for
the INF200 project January 2018.
"""

__author__ = "Hans Ekkehard Plesser, NMBU"
__email__ = "hans.ekkehard.plesser@nmbu.no"


if __name__ == '__main__':
    plt.ion()

    geogr = """OOOOOOOOOOOOOOOOOOOOO
               OOOOOOOOSMMMMJJJJJJJO
               OSSSSSJJJJMMJJJJJJJOO
               OSSSSSSSSSMMJJJJJJOOO
               OSSSSSJJJJJJJJJJJJOOO
               OSSSSSJJJDDJJJSJJJOOO
               OSSJJJJJDDDJJJSSSSOOO
               OOSSSSJJJDDJJJSOOOOOO
               OSSSJJJJJDDJJJJJJJOOO
               OSSSSJJJJDDJJJJOOOOOO
               OOSSSSJJJJJJJJOOOOOOO
               OOOSSSSJJJJJJJOOOOOOO
               OOOOOOOOOOOOOOOOOOOOO"""
    geogr = textwrap.dedent(geogr)

    ini_herbs = [{'loc': (10, 10),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(150)]}]
    ini_carns = [{'loc': (10, 10),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(40)]}]

    animals.Herbivore.set_parameters({'zeta': 3.2, 'xi': 1.8})
    animals.Carnivore.set_parameters({'a_half': 70, 'phi_age': 0.5,
                                      'omega': 0.3, 'F': 65,
                                      'DeltaPhiMax': 9.})
    Jungle.set_parameters({'f_max': 700})

    sim = BioSim(island_map=geogr, ini_pop=ini_herbs,
                 seed=123456)
    sim.simulate(num_steps=100, vis_steps=1, img_steps=2000)

    sim.add_population(population=ini_carns)
    sim.simulate(num_steps=100, vis_steps=1, img_steps=2000)

    input('Press ENTER')
