# -*- coding: utf-8 -*-

"""
A demo of the simulation, using the movie making functionality.

The situation is very similar to the check_sim case, just added movie making.
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen', 'Lars Martin Boe Lied'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no',\
            'lars.martin.boe.lied@nmbu.no'


import biosim.simulation
from biosim.animals import Herbivore, Carnivore
from biosim import landscape
import textwrap


if __name__ == '__main__':

    geogr = """\
               OOOOOOOOOOOOOOOOOOOOO
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

    Herbivore.set_parameters({'zeta': 3.2, 'xi': 1.8})
    Carnivore.set_parameters({'a_half': 70, 'phi_age': 0.5,
                              'omega': 0.3, 'F': 65,
                              'DeltaPhiMax': 9.})
    landscape.Jungle.set_parameters({'f_max': 700})

    sim = biosim.simulation.\
        BioSim(island_map=geogr, ini_pop=ini_herbs, seed=123456,
               img_dir=biosim.simulation.DEFAULT_GRAPHICS_DIR)

    sim.simulate(num_steps=100, vis_steps=1, img_steps=1)
    sim.add_population(population=ini_carns)
    sim.simulate(num_steps=100, vis_steps=1, img_steps=1)

    sim.make_movie()

    input('Press ENTER')
