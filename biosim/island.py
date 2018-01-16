# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no'


from landscape import Jungle, Savannah, Desert, Mountain, Ocean
from animals import Herbivore, Carnivore
import copy
import numpy as np
import random
import math


class Island:
    """"""

    def __init__(self, island_map):
        """"""
        self.map = island_map
        self.cells = None
        self.array_to_island()

    def string_to_array(self):
        """Converts the string-input for the map into an array"""

        temp_map = copy.deepcopy(self.map.replace(" ", ""))

        # ny versjon
        kart_list = [[a for a in row] for row in temp_map.splitlines()]
        kart_arr = np.array(kart_list)

        return kart_arr

    def array_to_island(self):
        """converts the array into a map"""

        array_map = self.string_to_array()
        array_shape = np.shape(array_map)   # type: tuple

        nested = list(np.zeros(array_shape))
        for i, e in enumerate(nested):
            nested[i] = list(e)

        for i in range(array_shape[0]):
            for j in range(array_shape[1]):
                if array_map[i, j] == 'J':
                    nested[i][j] = Jungle()
                if array_map[i, j] == 'S':
                    nested[i][j] = Savannah()
                if array_map[i, j] == 'D':
                    nested[i][j] = Desert()
                if array_map[i, j] == 'O':
                    nested[i][j] = Ocean()
                if array_map[i, j] == 'M':
                    nested[i][j] = Mountain()

        self.cells = np.array(nested)

    def add_animal_island(self, coordinates, animals_list):
        """dummy"""
        for animal in animals_list:
            if animal['species'] == 'Herbivore':
                self.cells[coordinates].add_herbivore(animal['age'],
                                                      animal['weight'])

            if animal['species'] == 'Carnivore':
                self.cells[coordinates].add_carnivore(animal['age'],
                                                      animal['weight'])


    def get_direction(self, pi_values):
            """"""
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
        """Returns random coordinates from across the island.
        Excludes the Oceans at the edge of island"""
        array_shape = np.shape(self.cells)  # type: tuple
        points_on_island = []
        for i in range(1, array_shape[0] - 1):
            for j in range(1, array_shape[1] - 1):
                points_on_island.append((i, j))
        random.shuffle(points_on_island)
        return points_on_island

    def get_pi_values_herbivores(self, coordinate):
        """Returns propensity-values for herbivores given cell"""

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
        """returns propensity-values for carnivores for given cell """

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
        """Moves the herbivores that should move in given cell"""

        right = (coordinate[0], coordinate[1] + 1)
        up = (coordinate[0] - 1, coordinate[1])
        left = (coordinate[0], coordinate[1] - 1)
        down = (coordinate[0] + 1, coordinate[1])

        for _ in range(len(self.cells[coordinate].herbivores)):
            herbivore = self.cells[coordinate].herbivores.pop(0)

            if herbivore.migration():
                move_direction = self.get_direction(
                    self.get_pi_values_herbivores(coordinate))
                if move_direction == 'right':
                    self.cells[right].herbivores_new.append(herbivore)
                if move_direction == 'up':
                    self.cells[up].herbivores_new.append(herbivore)
                if move_direction == 'left':
                    self.cells[left].herbivores_new.append(herbivore)
                if move_direction == 'down':
                    self.cells[down].herbivores_new.append(herbivore)
            else:
                self.cells[coordinate].herbivores.append(herbivore)

    def cell_move_carnivores(self, coordinate):
        right = (coordinate[0], coordinate[1] + 1)
        up = (coordinate[0] - 1, coordinate[1])
        left = (coordinate[0], coordinate[1] - 1)
        down = (coordinate[0] + 1, coordinate[1])

        for _ in range(len(self.cells[coordinate].carnivores)):
            carnivore = self.cells[coordinate].carnivores.pop(0)

            if carnivore.migration():
                move_direction = self.get_direction(
                    self.get_pi_values_carnivores(coordinate))
                if move_direction == 'right':
                    self.cells[right].carnivores_new.append(carnivore)
                if move_direction == 'up':
                    self.cells[up].carnivores_new.append(carnivore)
                if move_direction == 'left':
                    self.cells[left].carnivores_new.append(carnivore)
                if move_direction == 'down':
                    self.cells[down].carnivores_new.append(carnivore)
            else:
                self.cells[coordinate].carnivores.append(carnivore)

        coordinates = self.get_random_coordinates()
        for coordinate in coordinates:
            self.cell_move_carnivores(coordinate)

        for coordinate in coordinates:
            self.cells[coordinate].move_new_animals()


    def migration(self):
        """"""

        coordinates = self.get_random_coordinates()
        for coordinate in coordinates:
            self.cell_move_herbivores(coordinate)
            self.cell_move_carnivores(coordinate)

        for coordinate in coordinates:
            self.cells[coordinate].move_new_animals()

    def cycle(self):
        cells_shape = np.shape(self.cells)   # type: tuple
        for i in range(cells_shape[0]):
            for j in range(cells_shape[1]):
                if isinstance(self.cells[i, j], Jungle) or \
                        isinstance(self.cells[i, j], Savannah) or \
                        isinstance(self.cells[i, j], Desert):
                    self.cells[i, j].feeding()
                    self.cells[i, j].procreation()
#                   self.cells[i, j].migration()
                    self.cells[i, j].aging()
                    self.cells[i, j].loss_of_weight()
                    self.cells[i, j].death()


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
