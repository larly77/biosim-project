# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no'

import numpy as np
from island import Island
from landscape import Jungle, Savannah
from animals import Carnivore, Herbivore

ISLE_MAP = """\
        JSS
        SSJ
        SSS"""
INI_HERB = [{'loc': (1, 1),
             'pop': [{'species': 'Herbivore',
                      'age': 5,
                      'weight': 20}
                     for _ in range(20)]}]
INI_CARN = [{'loc': (1, 1),
             'pop': [{'species': 'Carnivore',
                      'age': 5,
                      'weight': 40}
                     for _ in range(20)]}]


class TestIsland:
    """Class for testing island"""

    def test_string_to_array(self):
        """Test for the method Island.string_to_array"""
        i1 = Island(ISLE_MAP)
        arry = i1.string_to_array()
        correct_arry = np.array([['J', 'S', 'S'],
                                 ['S', 'S', 'J'],
                                 ['S', 'S', 'S']])
        assert np.array_equal(arry, correct_arry)

    def test_array_to_island(self):
        i1 = Island(ISLE_MAP)
        correct_island = np.array([[Jungle(), Savannah(), Savannah()],
                                   [Savannah(), Savannah(), Jungle()],
                                   [Savannah(), Savannah(), Savannah()]])
        island_shape = np.shape(correct_island)   # type: tuple
        for i in range(island_shape[0]):
            for j in range(island_shape[1]):
                assert type(i1.cells[i, j]) == type(correct_island[i, j])

    def test_add_animal_island(self):

        i1 = Island(ISLE_MAP)
        assert len(i1.cells[1, 1].herbivores) == 0
        i1.add_animal_island((1, 1), INI_HERB[0]['pop'])
        assert len(i1.cells[1, 1].herbivores) == 20

        for animal in i1.cells[1, 1].herbivores:
            assert isinstance(animal, Herbivore)

        assert len(i1.cells[1, 1].carnivores) == 0
        i1.add_animal_island((1, 1), INI_CARN[0]['pop'])
        assert len(i1.cells[1, 1].carnivores) == 20

        for animal in i1.cells[1, 1].carnivores:
            assert isinstance(animal, Carnivore)

    def test_get_random_coordinates(self):
        ISLE_MAP2 = """\
                JSSJJSS
                SSJJSSJ
                SSSJJSJ
                JJJSSSS
                JJJSSSJ"""
        i1 = Island(ISLE_MAP2)
        assert [type(a) == tuple for a in i1.get_random_coordinates()]
        assert [len(a) == 2 for a in i1.get_random_coordinates()]

    def test_get_pi_values_herbivores(self):


