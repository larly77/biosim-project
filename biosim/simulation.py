# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no'


import random
from biosim.island import Island


class BioSim:
    """"""

    def __init__(self, island_map, ini_pop=None, seed=12345):
        random.seed(seed)
        self.island = Island(island_map)
        if ini_pop is not None:
            self.add_population(ini_pop)

    def add_population(self, population):
        """dum"""

        for index in range(len(population)):
            coordinates = population[index]['loc']
            coordinates = (coordinates[0] - 1, coordinates[1] - 1)
            animals = population[index]['pop']
            self.island.add_animal_island(coordinates, animals)

    def simulate_in_one_place_herbivores(self, num_steps, printing):

        # Run through num_steps years
        for year in range(num_steps):
            self.island.cycle()

            if printing:
                print('Year over:', year)
                print('Number of Herbivores: ',
                      len(self.island.cells[1, 1].herbivores))
                print('Number of Carnivores: ',
                      len(self.island.cells[1, 1].carnivores))

    def simulate(self, num_steps, vis_steps, img_steps):
        """"""

        print(vis_steps)
        print(img_steps)

        # Run through num_steps years
        for year in range(num_steps):
            self.island.cycle()

            print('Year over:', year)
            print('Number of Herbivores: ',
                  len(self.island.cells[9, 9].herbivores),
                  len(self.island.cells[8, 8].herbivores))
            print('Number of Carnivores: ',
                  len(self.island.cells[9, 9].carnivores),
                  len(self.island.cells[8, 8].carnivores))


if __name__ == '__main__':

    isle_map = """\
            OOO
            OJO
            OOO"""

    ini_herb = [{'loc': (2, 2),
                 'pop': [{'species': 'Herbivore',
                          'age': 5,
                          'weight': 20}
                         for _ in range(40)]}]

    ini_carn = [{'loc': (2, 2),
                 'pop': [{'species': 'Carnivore',
                          'age': 5,
                          'weight': 20}
                         for _ in range(5)]}]

    sim = BioSim(island_map=isle_map, ini_pop=ini_herb + ini_carn, seed=12345)

#    Savannah.set_parameters({'f_max': 800})

    sim.simulate_in_one_place_herbivores(num_steps=200, printing=True)
