# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no'


from landscape import Jungle, Savannah
from animals import Herbivore
import numpy as np
import copy
from island import Island


class BioSim:
    """"""

    def __init__(self, island_map, ini_pop, seed):
        self.map = island_map
        self.pop = ini_pop
        self.island = Island(self.map, self.pop)

        self.seed = seed

    def add_population(self, population):
        """dum"""
        coordinates = population[0]['loc']
        coordinates = (coordinates[0] - 1, coordinates[1] - 1)
        animals = population[0]['pop']
        self.island.add_animal_island(coordinates, animals)

    def simulate_in_one_place_herbivores(self, num_steps):



        # Run thru num_steps years
        for year in range(num_steps):

            for animal in self.location.get_herbivores():
                print(animal.age, animal.weight)
            print('Year over:', year)
            print('Number of Herbivores: ', len(self.location.get_herbivores()))


if __name__ == '__main__':

    ini_herb = [{'loc': (10, 10),
                 'pop': [{'species': 'Herbivore',
                          'age': 5,
                          'weight': 20}
                         for _ in range(20)]}]

    sim = BioSim(island_map="""J""", ini_pop=ini_herb, seed=123)
    #sim.array_to_island()
    #sim.simulate_in_one_place_herbivores(200)
