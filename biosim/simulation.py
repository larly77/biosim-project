# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no'


import random
import matplotlib.pyplot as plt
import textwrap
from biosim.island import Island


class BioSim:
    """"""

    def __init__(self, island_map, ini_pop=None, seed=12345):
        random.seed(seed)
        self.island_map = island_map
        self.island = Island(island_map)
        if ini_pop is not None:
            self.add_population(ini_pop)
        self.island.animals_on_island()
        self.fig = None

    def add_population(self, population):
        """dum"""

        for index in range(len(population)):
            coordinates = population[index]['loc']
            coordinates = (coordinates[0] - 1, coordinates[1] - 1)
            animals = population[index]['pop']
            self.island.add_animal_island(coordinates, animals)

    def make_rgb_map(self, show=False):
        """Function to make RGB map from island-string.
        Source: Plesser's Repository:
        NMBU_INF200_H17 / Lectures / J05 / Plotting / mapping.py (18.01.2018)"""

        rgb_value = {'O': (0.0, 0.0, 1.0),  # blue
                     'M': (0.5, 0.5, 0.5),  # grey
                     'J': (0.0, 0.6, 0.0),  # dark green
                     'S': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        map_rgb = [[rgb_value[column] for column in row]
                   for row in self.island_map.splitlines()]

        fig = plt.figure('RGB Map')

        axim = fig.add_axes([0.1, 0.1, 0.7, 0.8])  # llx, lly, w, h
        axim.imshow(map_rgb, interpolation='nearest')
        axim.set_xticks(range(len(map_rgb[0])))
        axim.set_xticklabels(range(1, 1 + len(map_rgb[0])))
        axim.set_yticks(range(len(map_rgb)))
        axim.set_yticklabels(range(1, 1 + len(map_rgb)))

        axlg = fig.add_axes([0.85, 0.1, 0.1, 0.8])  # llx, lly, w, h
        axlg.axis('off')
        for ix, name in enumerate(('Ocean', 'Mountain', 'Jungle',
                                   'Savannah', 'Desert')):
            axlg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                         edgecolor='none',
                                         facecolor=rgb_value[name[0]]))
            axlg.text(0.35, ix * 0.2, name, transform=axlg.transAxes)

        if show:
            plt.show()

    def herbivore_density_map(self, show=False):
        """
        Source: Plesser's Repository:
        NMBU_INF200_H17 / Lectures / J05 / Plotting / mapping.py (18.01.2018)"""

        fig = plt.figure('Herbivore density map')
        animals = self.island.herbivores_on_island

        axim = fig.add_axes([0.1, 0.1, 0.7, 0.8])  # llx, lly, w, h
        axim.imshow(animals, interpolation='nearest')
        axim.set_xticks(range(len(animals[0])))
        axim.set_xticklabels(range(1, 1 + len(animals[0])))
        axim.set_yticks(range(len(animals)))
        axim.set_yticklabels(range(1, 1 + len(animals)))

        if show:
            plt.show()

    def carnivore_density_map(self, show=False):
        """
        Source: Plesser's Repository:
        NMBU_INF200_H17 / Lectures / J05 / Plotting / mapping.py (18.01.2018)"""

        fig = plt.figure('Carnivore density map')
        animals = self.island.carnivores_on_island

        axim = fig.add_axes([0.1, 0.1, 0.7, 0.8])  # llx, lly, w, h
        axim.imshow(animals, interpolation='nearest')
        axim.set_xticks(range(len(animals[0])))
        axim.set_xticklabels(range(1, 1 + len(animals[0])))
        axim.set_yticks(range(len(animals)))
        axim.set_yticklabels(range(1, 1 + len(animals)))

        if show:
            plt.show()

    def make_visualization(self):
        """"""
        fig = plt.figure()

        # normal subplots
        ax1 = fig.add_subplot(2, 2, 1)
        ax2 = fig.add_subplot(2, 2, 2)
        ax3 = fig.add_subplot(2, 2, 3)
        ax4 = fig.add_subplot(2, 2, 4)

        (self.herbivore_density_map())

        self.fig = fig

    def update_visualization(self):
        """"""

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
            OOOO
            OJDO
            OOOO"""
    isle_map = textwrap.dedent(isle_map)
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

    sim.add_population([{'loc': (2, 3),
                         'pop': [{'species': 'Herbivore',
                                  'age': 5,
                                  'weight': 20}
                                 for _ in range(100)]}])
    sim.add_population([{'loc': (2, 3),
                         'pop': [{'species': 'Carnivore',
                                  'age': 5,
                                  'weight': 20}
                                 for _ in range(2)]}])

    sim.herbivore_density_map(show=True)
    sim.carnivore_density_map(show=True)

    #sim.make_rgb_map(show=True)

    #sim.simulate_in_one_place_herbivores(num_steps=200, printing=True)
