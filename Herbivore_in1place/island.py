# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no'


from landscape import Jungle, Savannah, Desert, Mountain, Ocean
import copy
import numpy as np


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
        a = list(temp_map)
        line_length = 0

        # Removes the line-shifts and calculate the lengths
        # of the rows in the new array
        a2 = [e for e in a if '\n' not in e]
        for element in a:
            if element == '\n':
                line_length = len(a[0:a.index(element)])
                break

        # divide the lhe list into equal chunks,
        # that fits with the row-lengths found earlier
        a3 = []
        for i in range(0, len(a2), line_length):
            af = a2[i:i + line_length]
            a3.append(af)

        # lager en array av det
        a4 = np.array(a3)
        return a4

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

    def cycle(self):
        cells_shape = np.shape(self.cells)   # type: tuple
        for i in range(cells_shape[0]):
            for j in range(cells_shape[1]):
                if isinstance(self.cells[i, j], Jungle) or \
                        isinstance(self.cells[i, j], Savannah) or \
                        isinstance(self.cells[i, j], Desert):
                    self.cells[i, j].feeding()
                    self.cells[i, j].procreation()
                    self.cells[i, j].migration()
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
