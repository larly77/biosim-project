# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no'


import random
import matplotlib.pyplot as plt
import numpy as np
import textwrap
from biosim.island import Island


class BioSim:
    """"""

    def __init__(self, island_map, ini_pop=None, seed=12345):
        random.seed(seed)
        np.random.seed(seed)
        self.island_map = island_map
        self.island = Island(island_map)
        if ini_pop is not None:
            self.add_population(ini_pop)
        self.island.animals_on_island()
        self.fig = None
        self.ax1 = None
        self.ax2 = None
        self.ax3 = None
        self.ax4 = None
        self.line_herbivore = None
        self.line_carnivore = None
        self.herbivore_density = None
        self.carnivore_density = None
        self.year = 0

    def add_population(self, population):
        """dum"""

        for index in range(len(population)):
            coordinates = population[index]['loc']
            coordinates = (coordinates[0] - 1, coordinates[1] - 1)
            animals = population[index]['pop']
            self.island.add_animal_island(coordinates, animals)

    def make_rgb_map(self):
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

#        self.ax1 = self.fig.add_axes([0.1, 0.1, 0.7, 0.8])  # llx, lly, w, h
        self.ax1.imshow(map_rgb, interpolation='nearest')
        self.ax1.set_xticks(range(len(map_rgb[0])))
        self.ax1.set_xticklabels(range(1, 1 + len(map_rgb[0])))
        self.ax1.set_yticks(range(len(map_rgb)))
        self.ax1.set_yticklabels(range(1, 1 + len(map_rgb)))
        self.ax1.set_title('Map of Rossumøya')

        axlg = self.fig.add_axes([0.44, 0.525, 0.1, 0.4])  # llx, lly, w, h
        axlg.axis('off')
        for ix, name in enumerate(('Ocean', 'Mountain', 'Jungle',
                                   'Savannah', 'Desert')):
            axlg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                         edgecolor='none',
                                         facecolor=rgb_value[name[0]]))
            axlg.text(0.35, ix * 0.2, name, transform=axlg.transAxes)

    def make_line_plot(self):
        """"""

        self.ax2.set_xlim(0,100)
        self.ax2.set_ylim(0, 15000)

        years_max = 10000
        self.line_herbivore = self.ax2.plot(np.arange(years_max),
                                  np.nan * np.ones(years_max), 'b-')[0]
        self.line_carnivore = self.ax2.plot(np.arange(years_max),
                                  np.nan * np.ones(years_max), 'r-')[0]

    def update_line_plot(self):
        """"""
        ydata = self.line_herbivore.get_ydata()
        ydata[self.year] = self.island.number_of_herbivores_island()
        self.line_herbivore.set_ydata(ydata)

        ydata = self.line_carnivore.get_ydata()
        ydata[self.year] = self.island.number_of_carnivores_island()
        self.line_carnivore.set_ydata(ydata)
        plt.pause(1e-6)

    def make_herbivore_density_map(self):
        """
        Source: Plesser's Repository:
        NMBU_INF200_H17 / Lectures / J05 / Plotting / mapping.py (18.01.2018)"""

        animals = self.island.herbivores_on_island

        

        self.ax3.set_xticks(range(len(animals[0])))
        self.ax3.set_xticklabels(range(1, 1 + len(animals[0])))
        self.ax3.set_yticks(range(len(animals)))
        self.ax3.set_yticklabels(range(1, 1 + len(animals)))
        self.ax3.set_title('Herbivore pop-density')

    def update_herbivore_density_map(self):


    def carnivore_density_map(self):
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

    def make_visualization(self):
        """"""
        self.fig = plt.figure()

        # normal subplots
        self.ax1 = self.fig.add_subplot(2, 2, 1)
        self.ax2 = self.fig.add_subplot(2, 2, 2)
        self.ax3 = self.fig.add_subplot(2, 2, 3)
        self.ax4 = self.fig.add_subplot(2, 2, 4)

        self.make_rgb_map()
        self.make_line_plot()



    def update_visualization(self):
        """"""
        self.update_line_plot()

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
        plt.ion()
        self.make_visualization()
        print(vis_steps)
        print(img_steps)

        # Run through num_steps years
        for year in range(num_steps):
            self.island.cycle()

            self.update_visualization()

            print('Year over:', self.year)
            print('Number of animals: ',
                  self.island.number_of_herbivores_island(),
                  self.island.number_of_carnivores_island())
            self.year += 1

if __name__ == '__main__':

    isle_map = """\
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
    isle_map = textwrap.dedent(isle_map)
    ini_herb = [{'loc': (10, 10),
                 'pop': [{'species': 'Herbivore',
                          'age': 5,
                          'weight': 20}
                         for _ in range(40)]}]
    ini_carn = [{'loc': (10, 3),
                 'pop': [{'species': 'Carnivore',
                          'age': 5,
                          'weight': 20}
                         for _ in range(5)]}]

    sim = BioSim(island_map=isle_map, ini_pop=ini_herb + ini_carn, seed=12345)

    sim.add_population([{'loc': (3, 3),
                         'pop': [{'species': 'Herbivore',
                                  'age': 5,
                                  'weight': 20}
                                 for _ in range(100)]}])
    sim.add_population([{'loc': (3, 3),
                         'pop': [{'species': 'Carnivore',
                                  'age': 5,
                                  'weight': 20}
                                 for _ in range(2)]}])

    sim.simulate(50, 1, 2000)
    #sim.make_visualization()

    #sim.make_rgb_map()

    #sim.simulate_in_one_place_herbivores(num_steps=200, printing=True)

    input('Press ENTER')

