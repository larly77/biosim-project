# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no'


import random
from island import Island


class BioSim:
    """"""

    def __init__(self, island_map, ini_pop=None, seed=12345):
        random.seed(seed)
        self.island = Island(island_map)
        if ini_pop is not None:
            self.add_population(ini_pop)

    def add_population(self, population):
        """dum"""
        coordinates = population[0]['loc']
        coordinates = (coordinates[0] - 1, coordinates[1] - 1)
        animals = population[0]['pop']
        self.island.add_animal_island(coordinates, animals)

    def simulate_in_one_place_herbivores(self, num_steps, printing):

        # Run thru num_steps years
        for year in range(num_steps):
            self.island.cycle()

            if printing:
                print('Year over:', year)
                print('Number of Herbivores: ',
                      len(self.island.cells[1, 1].herbivores))


if __name__ == '__main__':

#   from landscape import Jungle, Savannah
    isle_map = """\
            OOO
            ODO
            OOO"""

    ini_herb = [{'loc': (2, 2),
                 'pop': [{'species': 'Herbivore',
                          'age': 5,
                          'weight': 40}
                         for _ in range(20)]}]

    sim = BioSim(island_map=isle_map, ini_pop=ini_herb, seed=12345)
#    Savannah.set_parameters({'f_max': 800})

    sim.simulate_in_one_place_herbivores(num_steps=200, printing=True)
