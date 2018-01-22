# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen', 'Lars Martin Boe Lied'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no',\
            'lars.martin.boe.lied@nmbu.no'


from biosim.landscape import Jungle, Savannah, Desert, Mountain, Ocean
from biosim.animals import Herbivore, Carnivore
import copy
import numpy as np
import random
import math


class Island:
    """
    Class for the island
    """

    def __init__(self, island_map):
        """
        Init method for class Island

        Parameters
        ----------
        island_map : str
            A string representing the map
        """
        self.map = island_map
        self.cells = None
        self.array_to_island()
        self.herbivores_on_island = None
        self.carnivores_on_island = None

    def string_to_array(self):
        """
        A method for concerting thr given string into an array

        Returns
        -------
        map_arr : arr
            An array of the map, where each letter has a seperate place

        Raises
        ------
        SyntaxError
            If self.map have lines of unequal length.
            If self.map have edges unequal to 'O'.

        """
        temp_map = copy.deepcopy(self.map.replace(" ", ""))
        map_list = [[a for a in row] for row in temp_map.splitlines()]

        # Checks that all lines are of equal length
        for line in map_list:
            for index in range(len(map_list)):
                if len(map_list[index]) == len(line):
                    continue
                else:
                    raise SyntaxError("Island geography multi-line string "
                                      "must have lines of same length.")
        map_arr = np.array(map_list)

        # Checks that there are only 'O's at the edges.
        edge = []
        edge += list(map_arr[0, :])
        edge += list(map_arr[-1, :])
        edge += list(map_arr[1:-1, 0])
        edge += list(map_arr[1:-1, -1])
        if set(edge) == {'O'}:
            pass
        else:
            raise SyntaxError("Island geography multi-line string "
                              "must have 'O' around the edges. ")

        return map_arr

    def array_to_island(self):
        """
        Converts the array from the method string_to_array into a island.

        changes the array consisting of strings into an array consisting of
        instances of classes depedning on the letter that was previously in
        the array, for example 'J' would turn into an instance of the
        Jungle-class. These are stored in Island.cells

        Returns
        -------

        Raises
        ------
        SyntaxError
            If self.map contain other letters than 'J', 'S', 'D', 'O', 'M'.

        """

        array_map = self.string_to_array()
        array_shape = np.shape(array_map)   # type: tuple

        nested = list(np.zeros(array_shape))
        for i, e in enumerate(nested):
            nested[i] = list(e)

        for i in range(array_shape[0]):
            for j in range(array_shape[1]):
                if array_map[i, j] == 'J':
                    nested[i][j] = Jungle()
                elif array_map[i, j] == 'S':
                    nested[i][j] = Savannah()
                elif array_map[i, j] == 'D':
                    nested[i][j] = Desert()
                elif array_map[i, j] == 'O':
                    nested[i][j] = Ocean()
                elif array_map[i, j] == 'M':
                    nested[i][j] = Mountain()
                else:
                    raise SyntaxError("Island geography multi-line string "
                                      "must only have these letters: "
                                      "'J', 'S', 'D', 'O', 'M'")

        self.cells = np.array(nested)

    def animals_on_island(self):
        """
        Method for getting the number of carnivores and herbivores on island

        Makes one matrix for herbivores and one for carnivores, containing
        the number of carnivores and herbivores on the tile on the island
        matching the matrix.

        Returns
        -------

        """
        shape = np.shape(self.string_to_array())  # type: tuple
        herbivore_matrix = np.zeros(shape=shape)
        carnivore_matrix = np.zeros(shape=shape)

        for i in range(1, shape[0] - 1):
            for j in range(1, shape[1] - 1):
                if isinstance(self.cells[i, j], (Jungle, Savannah, Desert)):
                    herbivore_matrix[i, j] = \
                        len(self.cells[i, j].get_herbivores())
                    carnivore_matrix[i, j] = \
                        len(self.cells[i, j].get_carnivores())

        self.herbivores_on_island = herbivore_matrix
        self.carnivores_on_island = carnivore_matrix

    def number_of_herbivores_island(self):
        """
        Method for getting the total amount of herbivores on island

        Returns
        -------
        Number of herbivores on island

        """
        return np.sum(self.herbivores_on_island)

    def number_of_carnivores_island(self):
        """
        Method for getting the total amount of herbivores on island

        Returns
        -------
        Number of carnivores on island
        """
        return np.sum(self.carnivores_on_island)

    def add_animal_island(self, coordinates, animals_list):
        """
        Method for adding animals to the island

        Parameters
        ----------
        coordinates : tuple
            Where to put the animals on the island
        animals_list : list
            The list of animals to put on the island

        Returns
        -------

        Raises
        -------
        ValueError
            If coordinates is not in jungle, savannah or desert

        """

        if isinstance(self.cells[coordinates], (Jungle, Savannah, Desert)):
            for animal in animals_list:
                if animal['species'] == 'Herbivore':
                    self.cells[coordinates].add_herbivore(animal['age'],
                                                          animal['weight'])

                if animal['species'] == 'Carnivore':
                    self.cells[coordinates].add_carnivore(animal['age'],
                                                          animal['weight'])
        else:
            raise ValueError('Coordinates must be for cell with'
                             ' Jungle, Savannah, or Desert')
        self.animals_on_island()

    @staticmethod
    def get_direction(pi_values):
        """
        Method for getting the direction for the animal to move in

        Parameters
        ----------
        pi_values : tuple
            Values used to calculate the direction, found in the method;
            get_pi_values_herbivores and get_pi_values_carnivores

        Returns
        -------
        Direction as a string for example 'right' or 'left

        """
        if pi_values == (0, 0, 0, 0):
            return 'do not move'
        pi_right, pi_up, pi_left, pi_down = pi_values
        pi_sum = sum((pi_right, pi_up, pi_left, pi_down))

        p_right = pi_right / pi_sum
        p_up = pi_up / pi_sum
        p_left = pi_left / pi_sum
        p_down = pi_down / pi_sum

        return np.random.choice(
            ('right', 'up', 'left', 'down'),
            p=[p_right, p_up, p_left, p_down])

    def get_random_coordinates(self):
        """
        Method for getting random coordinates from the island

        Shuffles the coordinates on the island, for use in a different method
        excludes the ocean at the edge of the island

        Returns
        -------
        points_on_island : list
            a randomly shuffled list of coordinates from the island

        """
        array_shape = np.shape(self.cells)  # type: tuple
        points_on_island = []
        for i in range(1, array_shape[0] - 1):
            for j in range(1, array_shape[1] - 1):
                points_on_island.append((i, j))
        random.shuffle(points_on_island)
        return points_on_island

    def get_pi_values_herbivores(self, coordinate):
        """
        Method for calculating pi-values(propensity) for herbivores

        Parameters
        ----------
        coordinate : tuple
            Coordinates  from which to find the animals to calculate pi's for

        Returns
        -------
        pi_right, pi_up, pi_left, pi_down : float
            Different propensity-values for each direction in given cell


        """
        right = (coordinate[0], coordinate[1] + 1)
        if isinstance(self.cells[right], (Mountain, Ocean)):
            pi_right = 0
        else:
            pi_right = math.exp(
                Herbivore.parameters['lambda'] * self.cells[
                    right].get_abundance_herbivore())

        up = (coordinate[0] - 1, coordinate[1])
        if isinstance(self.cells[up], (Mountain, Ocean)):
            pi_up = 0
        else:
            pi_up = math.exp(
                Herbivore.parameters['lambda'] * self.cells[
                    up].get_abundance_herbivore())

        left = (coordinate[0], coordinate[1] - 1)
        if isinstance(self.cells[left], (Mountain, Ocean)):
            pi_left = 0
        else:
            pi_left = math.exp(
                Herbivore.parameters['lambda'] * self.cells[
                    left].get_abundance_herbivore())

        down = (coordinate[0] + 1, coordinate[1])
        if isinstance(self.cells[down], (Mountain, Ocean)):
            pi_down = 0
        else:
            pi_down = math.exp(
                Herbivore.parameters['lambda'] * self.cells[
                    down].get_abundance_herbivore())

        return pi_right, pi_up, pi_left, pi_down

    def get_pi_values_carnivores(self, coordinate):
        """
        Method for calculating pi-values(propensity) for carnivores

        Parameters
        ----------
        coordinate : tuple
            Coordinates  from which to find the animals to calculate pi's for

        Returns
        -------
        pi_right, pi_up, pi_left, pi_down : float
            Different propensity-values for each direction in given cell
        """
        right = (coordinate[0], coordinate[1] + 1)
        if isinstance(self.cells[right], (Mountain, Ocean)):
            pi_right = 0
        else:
            pi_right = math.exp(
                Carnivore.parameters['lambda'] * self.cells[
                    right].get_abundance_carnivore())

        up = (coordinate[0] - 1, coordinate[1])
        if isinstance(self.cells[up], (Mountain, Ocean)):
            pi_up = 0
        else:
            pi_up = math.exp(
                Carnivore.parameters['lambda'] * self.cells[
                    up].get_abundance_carnivore())

        left = (coordinate[0], coordinate[1] - 1)
        if isinstance(self.cells[left], (Mountain, Ocean)):
            pi_left = 0
        else:
            pi_left = math.exp(
                Carnivore.parameters['lambda'] * self.cells[
                    left].get_abundance_carnivore())

        down = (coordinate[0] + 1, coordinate[1])
        if isinstance(self.cells[down], (Mountain, Ocean)):
            pi_down = 0
        else:
            pi_down = math.exp(
                Carnivore.parameters['lambda'] * self.cells[
                    down].get_abundance_carnivore())

        return pi_right, pi_up, pi_left, pi_down

    def cell_move_herbivores(self, coordinate):
        """
        method for moving herbivores in given cell, if they should move

        Parameters
        ----------
        coordinate : tuple
            coordinates in which to move herbivores

        Returns
        -------

        """
        """Moves the herbivores that should move in given cell"""

        right = (coordinate[0], coordinate[1] + 1)
        up = (coordinate[0] - 1, coordinate[1])
        left = (coordinate[0], coordinate[1] - 1)
        down = (coordinate[0] + 1, coordinate[1])

        length = len(self.cells[coordinate].herbivores)
        for _ in range(length):
            herbivore = self.cells[coordinate].herbivores.pop(0)

            if herbivore.migration():
                move_direction = self.get_direction(
                    self.get_pi_values_herbivores(coordinate))
                if move_direction == 'right':
                    self.cells[right].herbivores_new.append(herbivore)
                elif move_direction == 'up':
                    self.cells[up].herbivores_new.append(herbivore)
                elif move_direction == 'left':
                    self.cells[left].herbivores_new.append(herbivore)
                elif move_direction == 'down':
                    self.cells[down].herbivores_new.append(herbivore)
                else:
                    self.cells[coordinate].herbivores.append(herbivore)
            else:
                self.cells[coordinate].herbivores.append(herbivore)

    def cell_move_carnivores(self, coordinate):
        """
        method for moving herbivores in given cell, if they should move

        Parameters
        ----------
        coordinate : tuple
            coordinates in which to move herbivores

        Returns
        -------

        """

        right = (coordinate[0], coordinate[1] + 1)
        up = (coordinate[0] - 1, coordinate[1])
        left = (coordinate[0], coordinate[1] - 1)
        down = (coordinate[0] + 1, coordinate[1])

        length = len(self.cells[coordinate].carnivores)
        for _ in range(length):
            carnivore = self.cells[coordinate].carnivores.pop(0)

            if carnivore.migration():
                move_direction = self.get_direction(
                    self.get_pi_values_carnivores(coordinate))
                if move_direction == 'right':
                    self.cells[right].carnivores_new.append(carnivore)
                elif move_direction == 'up':
                    self.cells[up].carnivores_new.append(carnivore)
                elif move_direction == 'left':
                    self.cells[left].carnivores_new.append(carnivore)
                elif move_direction == 'down':
                    self.cells[down].carnivores_new.append(carnivore)
                else:
                    self.cells[coordinate].carnivores.append(carnivore)
            else:
                self.cells[coordinate].carnivores.append(carnivore)

    def migration(self):
        """
        Method for handling migration

        Implements the previous move-methods for herbivores and carnivores,
        including all new animals in that were appended in the move-methods

        Returns
        -------

        """

        coordinates = self.get_random_coordinates()
        for coordinate in coordinates:
            if isinstance(self.cells[coordinate], (Jungle, Savannah, Desert)):
                self.cell_move_herbivores(coordinate)
                self.cell_move_carnivores(coordinate)

        for coordinate in coordinates:
            if isinstance(self.cells[coordinate], (Jungle, Savannah, Desert)):
                self.cells[coordinate].move_new_animals()

    def cycle(self):
        """
        Simulates one cycle/year

        Every method is done in the order specified in the assignment
        Returns
        -------

        """

        coordinates = self.get_random_coordinates()

        for coord in coordinates:
            if isinstance(self.cells[coord], (Jungle, Savannah, Desert)):
                self.cells[coord].feeding()

        for coord in coordinates:
            if isinstance(self.cells[coord], (Jungle, Savannah, Desert)):
                self.cells[coord].procreation()

        self.migration()

        for coord in coordinates:
            if isinstance(self.cells[coord], (Jungle, Savannah, Desert)):
                self.cells[coord].aging()

        for coord in coordinates:
            if isinstance(self.cells[coord], (Jungle, Savannah, Desert)):
                self.cells[coord].loss_of_weight()

        for coord in coordinates:
            if isinstance(self.cells[coord], (Jungle, Savannah, Desert)):
                self.cells[coord].death()

        self.animals_on_island()


if __name__ == '__main__':

    isle_map = """\
            JSS
            SSJ
            SSS"""
    ini_herb = [{'loc': (10, 10),
                 'pop': [{'species': 'Herbivore',
                          'age': 5,
                          'weight': 20}
                         for _ in range(20)]}]

    isle = Island(isle_map)
    isle.array_to_island()

    print(isle.cells)
