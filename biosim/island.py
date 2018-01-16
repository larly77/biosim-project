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

    def migration(self):
        """Makes migration happens at random across the island.
        Excludes the Oceans at the edge of island"""

        array_shape = np.shape(self.cells)   # type: tuple
        coordinates = []
        for i in range(1, array_shape[0]-1):
            for j in range(1, array_shape[1]-1):
                coordinates.append((i, j))

        random.shuffle(coordinates)
        for coordinate in coordinates:
            stay = [True] * len(self.cells[coordinate].herbivores)
            for index, herbivore in enumerate(self.cells[coordinate].herbivores):
                if herbivore.migration():
                    stay[index] = False
                    right = (coordinate[0], coordinate[1]+1)
                    if isinstance(self.cells[right], (Mountain, Ocean)):
                        pi_right = 0
                    else:
                        pi_right = math.exp(Herbivore.parameters['lambda'] * self.cells[right].get_abundance_herbivore())

                    up = (coordinate[0]-1, coordinate[1])
                    if isinstance(self.cells[up], (Mountain, Ocean)):
                        pi_up = 0
                    else:
                        pi_up = math.exp(Herbivore.parameters['lambda'] * self.cells[up].get_abundance_herbivore())

                    left = (coordinate[0], coordinate[1]-1)
                    if isinstance(self.cells[left], (Mountain, Ocean)):
                        pi_left = 0
                    else:
                        pi_left = math.exp(Herbivore.parameters['lambda'] * self.cells[left].get_abundance_herbivore())

                    down = (coordinate[0]+1, coordinate[1])
                    if isinstance(self.cells[down], (Mountain, Ocean)):
                        pi_down = 0
                    else:
                        pi_down = math.exp(Herbivore.parameters['lambda'] * self.cells[down].get_abundance_herbivore())

                    pi_sum = sum((pi_right, pi_up, pi_left, pi_down))
                    p_right = pi_right / pi_sum
                    p_up = pi_up / pi_sum
                    p_left = pi_left / pi_sum
                    p_down = pi_down / pi_sum

                    move_direction = np.random.choice(
                        ('right', 'up', 'left', 'down'),
                        p=[p_right, p_up, p_left, p_down])

                    if move_direction == 'right':
                        self.cells(right).herbivores_new.append(herbivore)
                    if move_direction == 'up':
                        self.cells(up).herbivores_new.append(herbivore)
                    if move_direction == 'left':
                        self.cells(left).herbivores_new.append(herbivore)
                    if move_direction == 'down':
                        self.cells(down).herbivores_new.append(herbivore)

            self.cells[coordinate].herbivores = [a for i, a in enumerate(self.cells[coordinate].herbivores) if stay[i]]

        for coordinate in coordinates:
            # flytte fra liste til liste_new.

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
