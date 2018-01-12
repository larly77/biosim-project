# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no'


from landscape import Jungle, Savannah
from animals import Herbivore
import numpy as np
import copy


class BioSim:
    """"""

    def __init__(self, island_map, ini_pop, seed):
        self.map = island_map
        self.pop = ini_pop
        self.island = None
        self.location = None

        self.seed = seed

    def simulate_in_one_place_herbivores(self, num_steps):

        # Make 'one place'
        if self.location is None:
            if self.map == 'J':
                self.location = Jungle()
            if self.map == 'S':
                self.location = Savannah()

        # Populate 'one place'
            for animal in self.pop[0]['pop']:
                if animal['species'] == 'Herbivore':
                    self.location.herbivores.append(
                        Herbivore(weight=animal['weight'], age=animal['age']))

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
