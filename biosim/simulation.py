# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no'


import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import textwrap
import random
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
        self.year_ax = None
        self.year_txt = None
        self.vis_index = 0
        self.last_step = 0
        self.year = 0
        self.x_lim = (0, 100)  # line graph ordinate limits, default values
        self.y_lim = (0, 15000)  # line graph abscissa limits, default values
        self.user_limits = False
        self.herbivore_color_code = (0, 300)  # population map color code limits
        self.carnivore_color_code = (0, 300)  # population map color code limits

    def add_population(self, population):
        """
        method for adding a population to the island
        Parameters
        ----------
        population : list
            A list of animals, containing dictionaries for each animal

        Returns
        -------

        """

        island_shape = np.shape(self.island.cells)  # type: tuple
        points_on_island = []
        for i in range(1, island_shape[0] + 1):
            for j in range(1, island_shape[1] + 1):
                points_on_island.append((i, j))

        for index in range(len(population)):

            if type(population[index]['loc']) is tuple:
                if population[index]['loc'] in points_on_island:
                    coordinates = population[index]['loc']
                else:
                    raise IndexError('The coordinates must exist on the island'
                                     ': (x, y). (1,1) is the upper left corner')
            else:
                raise TypeError("'loc' must be tuple with coordinates: (x, y)")

            coordinates = (coordinates[0] - 1, coordinates[1] - 1)
            animals = population[index]['pop']
            self.island.add_animal_island(coordinates, animals)

    def status_year(self):
        """
        method for getting the current year on screen
        Returns
        -------
        self.year : int
            the current year

        """
        print('Number of years simulated: ', self.year)
        return self.year

    def status_number_of_animals_total(self):
        """
        method for getting the total amount of animals on screen
        Returns
        -------

        """
        total_animals = int(self.island.number_of_herbivores_island()
                            + self.island.number_of_carnivores_island())

        print('Total number of animals: ', total_animals)
        return total_animals

    def status_number_of_animals_by_species(self):
        """
        method for getting number of herbivores and carnivores on screen
        Returns
        -------
        dictionary : dict
            A dictionary containing number herbivores and carnivores on island

        """
        return {'herbivores': int(self.island.number_of_herbivores_island()),
                'carnivores': int(self.island.number_of_carnivores_island())}

    def status_per_cell_animal_count(self):
        """
        Method for getting number of each species in each cell, using pandas
        Returns
        -------
        df : pandas.DataFrame
            A table containing each cell and the number of each species on
            each cell

        """

        shape = np.shape(self.island.herbivores_on_island)  # type: tuple
        coordinates = []
        for i in range(1, shape[0] + 1):
            for j in range(1, shape[1] + 1):
                coordinates.append((i, j))
        coordinates = np.array(coordinates)

        col1 = coordinates[:, 0]
        col2 = coordinates[:, 1]
        col3 = self.island.herbivores_on_island.ravel().astype(np.int)
        col4 = self.island.carnivores_on_island.ravel().astype(np.int)

        df = pd.DataFrame({'x':col1, 'y':col2, 'herbivores': col3,
                           'carnivores': col4}, index=zip(col1, col2))
        df = df[['x', 'y', 'herbivores', 'carnivores']]
        return df

    def set_axis_limits(self, x_limits, y_limits):
        """
        Method for setting the x and y-limits on the line graph
        Parameters
        ----------
        x_limits : tuple, list
            tuple or list containing the lower and upper boundaries for the
            x axis

        y_limits : tuple, list
            tuple or list containing the lower and upper boundaries for the
            y axis

        Returns
        -------

        """
        if type(x_limits) is tuple or type(x_limits) is list:
            self.x_lim = x_limits
        else:
            raise TypeError('x_limits must be a tuple or list of 2 numbers')
        if type(y_limits) is tuple or type(y_limits) is list:
            self.y_lim = y_limits
        else:
            raise TypeError('y_limits must be a tuple or list of 2 numbers')
        self.user_limits = True

    def reset_axis_limits(self):
        """
        Method for resetting the axis limits for both x and y axis
        Returns
        -------

        """
        self.user_limits = False
        self.y_lim = (0, 15000)  # default values

    def set_color_code_limits(self, herbivore_colors, carnivore_colors):
        """
        Method for setting the color code limits for each species
        Parameters
        ----------
        herbivore_colors : tuple
            boundaries for the color representation for number of herbivores
        carnivore_colors : tuple
            boundaries for the color representation for number of herbivores


        Returns
        -------

        """
        if type(herbivore_colors) is tuple or type(herbivore_colors) is list:
            self.herbivore_color_code = herbivore_colors
        else:
            raise TypeError('herbivore_colors must be a tuple or list of 2 int')
        if type(carnivore_colors) is tuple or type(carnivore_colors) is list:
            self.carnivore_color_code = carnivore_colors
        else:
            raise TypeError('carnivore_colors must be a tuple or list of 2 int')

    def reset_color_code_limits(self):
        """
        Method for resetting the color code to default values
        Returns
        -------

        """
        self.herbivore_color_code = (0, 300)  # default values
        self.carnivore_color_code = (0, 300)  # default values

    def year_counter(self):
        """
        Method for updating the counter on screen
        Returns
        -------

        """
        """
        Source: Plesser's Repository: (18.01.2018)
        NMBU_INF200_H17 / Lectures / J05 / Plotting / time_counter.py"""

        if self.year_ax is None:
            self.year_ax = self.fig.add_axes([0.4, 0.83, 0.2, 0.2])
            self.year_ax.axis('off')

            self.year_txt = \
                self.year_ax.text(0.5, 0.5, 'Year: {:5}'.format(self.year),
                                  horizontalalignment='center',
                                  verticalalignment='center',
                                  transform=self.year_ax.transAxes, fontsize=16)

        self.year_txt.set_text('Year: {:5}'.format(self.year))

    def make_rgb_map(self):
        """
        Function to make RGB map from island-string
        Returns
        -------

        """
        """
        Source: Plesser's Repository:
        NMBU_INF200_H17 / Lectures / J05 / Plotting / mapping.py (18.01.2018)"""

        rgb_value = {'O': (0.0, 0.0, 1.0),  # blue
                     'M': (0.5, 0.5, 0.5),  # grey
                     'J': (0.0, 0.6, 0.0),  # dark green
                     'S': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        map_rgb = [[rgb_value[column] for column in row]
                   for row in self.island_map.splitlines()]

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

    def make_line_plot(self, vis_steps):
        """
        Method for making the line plot
        Parameters
        ----------
        vis_steps

        Returns
        -------

        """
        if self.user_limits:
            self.ax2.set_xlim(self.x_lim[0], self.x_lim[1])
            self.ax2.set_ylim(self.y_lim[0], self.y_lim[1])
        else:
            self.ax2.set_xlim(0, self.last_step + 1)
            self.ax2.set_ylim(self.y_lim[0], self.y_lim[1])

        self.ax2.set_title('Populations')

        if self.line_herbivore is None:
            self.line_herbivore = \
                self.ax2.plot(np.arange(0, self.last_step + 1, vis_steps),
                              np.nan * np.ones(
                              len(np.arange(0, self.last_step + 1, vis_steps))),
                              'b-')[0]
            self.line_carnivore = \
                self.ax2.plot(np.arange(0, self.last_step + 1, vis_steps),
                              np.nan * np.ones(
                              len(np.arange(0, self.last_step + 1, vis_steps))),
                              'r-')[0]
            self.ax2.legend(['Herbivores', 'Carnivores'])
        else:
            xdata, ydata = self.line_herbivore.get_data()
            xnew = np.arange(xdata[-1] + 1, self.last_step + 1, vis_steps)
            if len(xnew) > 0:
                ynew = np.nan * np.ones_like(xnew)
                self.line_herbivore.set_data(np.hstack((xdata, xnew)),
                                             np.hstack((ydata, ynew)))
            xdata, ydata = self.line_carnivore.get_data()
            xnew = np.arange(xdata[-1] + 1, self.last_step + 1, vis_steps)
            if len(xnew) > 0:
                ynew = np.nan * np.ones_like(xnew)
                self.line_carnivore.set_data(np.hstack((xdata, xnew)),
                                             np.hstack((ydata, ynew)))

    def update_line_plot(self):
        """
        Method for updating the line plot
        Returns
        -------

        """
        ydata = self.line_herbivore.get_ydata()
        ydata[self.vis_index] = self.island.number_of_herbivores_island()
        self.line_herbivore.set_ydata(ydata)

        ydata = self.line_carnivore.get_ydata()
        ydata[self.vis_index] = self.island.number_of_carnivores_island()
        self.line_carnivore.set_ydata(ydata)
        plt.pause(1e-6)
        self.vis_index += 1

    def make_herbivore_density_map(self):
        """
        Method for making the hebrivore density map
        Returns
        -------

        """
        """
        Source: Plesser's Repository:
        NMBU_INF200_H17 / Lectures / J05 / Plotting / mapping.py (18.01.2018)"""

        animals = self.island.herbivores_on_island

        self.herbivore_density = \
            self.ax3.imshow(animals, interpolation='nearest',
                            vmin=self.herbivore_color_code[0],
                            vmax=self.herbivore_color_code[1])
        self.ax3.set_xticks(range(len(animals[0])))
        self.ax3.set_xticklabels(range(1, 1 + len(animals[0])))
        self.ax3.set_yticks(range(len(animals)))
        self.ax3.set_yticklabels(range(1, 1 + len(animals)))
        self.ax3.set_title('Herbivore population density')

    def update_herbivore_density_map(self):
        """
        Method for updating the herbivore density map
        Returns
        -------

        """
        self.herbivore_density.set_data(self.island.herbivores_on_island)

    def make_carnivore_density_map(self):
        """
        Method for making the carnivore density map
        Returns
        -------

        """
        """
        Source: Plesser's Repository:
        NMBU_INF200_H17 / Lectures / J05 / Plotting / mapping.py (18.01.2018)"""

        animals = self.island.carnivores_on_island

        self.carnivore_density = \
            self.ax4.imshow(animals, interpolation='nearest',
                            vmin=self.carnivore_color_code[0],
                            vmax=self.carnivore_color_code[1])
        self.ax4.set_xticks(range(len(animals[0])))
        self.ax4.set_xticklabels(range(1, 1 + len(animals[0])))
        self.ax4.set_yticks(range(len(animals)))
        self.ax4.set_yticklabels(range(1, 1 + len(animals)))
        self.ax4.set_title('Carnivore population density')

    def update_carnivore_density_map(self):
        """
        Method for updating the carnivore density map
        Returns
        -------

        """
        self.carnivore_density.set_data(self.island.carnivores_on_island)

    def make_visualization(self, vis_steps):
        """
        Method for making the visualization
        Parameters
        ----------
        vis_steps : int
            How often the graphics should be updated, in years

        Returns
        -------

        """
        if self.fig is None:
            self.fig = plt.figure()

            self.ax1 = self.fig.add_subplot(2, 2, 1)
            self.ax2 = self.fig.add_subplot(2, 2, 2)
            self.ax3 = self.fig.add_subplot(2, 2, 3)
            self.ax4 = self.fig.add_subplot(2, 2, 4)

            self.make_rgb_map()
            self.make_herbivore_density_map()
            self.make_carnivore_density_map()
            self.year_counter()

        self.make_line_plot(vis_steps)

    def update_visualization(self):
        """
        Method for updating the visualization
        Returns
        -------

        """
        self.update_line_plot()
        self.update_herbivore_density_map()
        self.update_carnivore_density_map()
        self.year_counter()

    def simulate(self, num_steps, vis_steps=1, img_steps=None):
        """
        Method for simulating the entire island
        Parameters
        ----------
        num_steps : int
            Numbers of years to be simulated
        vis_steps : int
            How often the graphics should be updated, in years
        img_steps : How often the graphic should be saved

        Returns
        -------

        """
        plt.ion()
        if img_steps is None:
            img_steps = vis_steps
        self.last_step += num_steps

        self.make_visualization(vis_steps)

        # Run through num_steps years
        while self.year <= self.last_step:
            self.island.cycle()

            if (self.year % vis_steps) == 0:
                self.update_visualization()
            if self.year % img_steps == 0:
                pass

            self.year += 1
            """            print('Year over:', self.year)
            print('Number of animals: ',
                  self.island.number_of_herbivores_island(),
                  self.island.number_of_carnivores_island())"""


if __name__ == '__main__':

    isle_map = """\
              OOOOO
              OJJJO
              OSSSO
              OOOOO"""

    isle_map = textwrap.dedent(isle_map)
    ini_herb = [{'loc': (2, 2),
                 'pop': [{'species': 'Herbivore',
                          'age': 5,
                          'weight': 20}
                         for _ in range(40)]}]
    ini_carn = [{'loc': (3, 4),
                 'pop': [{'species': 'Carnivore',
                          'age': 5,
                          'weight': 20}
                         for _ in range(5)]}]

    sim = BioSim(island_map=isle_map, ini_pop=ini_herb + ini_carn, seed=12345)


    #sim.simulate(50, 1, 2000)
    #sim.make_visualization()

    #sim.make_rgb_map()

    #sim.simulate_in_one_place_herbivores(num_steps=200, printing=True)

    df = sim.status_per_cell_animal_count()
    print(df)
    print(df['herbivores'][2,2])
    print(df['carnivores'][3,4])

    input('Press ENTER')
