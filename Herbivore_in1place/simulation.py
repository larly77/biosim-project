# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no'


from landscape import Jungle
from animals import Herbivore, Savannah


class BioSim:
    """"""

    def __init__(self, island_map, ini_pop, seed):
        self.map = island_map
        self.pop = ini_pop
        self.island = None

        self.seed = seed

    def create_map(self):
        """"""

    def simulate_in_one_place_herbivores(self, num_steps):
        # Make 'one place'
        if self.map == 'J':
            self.island = Jungle()
        if self.map == 'S':
            self.island = Savannah()

        # Populate 'one place'
        for animal in self.pop['pop']:
            if animal['species'] == 'Herbivore':
                self.island.herbivore_list.append(
                    Herbivore(weight=animal['weight'], age=animal['age']))

        # Run thru num_steps years
        for year in num_steps:





