# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no'

import numpy as np
from biosim.island  import Island
from biosim.landscape import Jungle, Savannah
from biosim.animals import Carnivore, Herbivore
import math
import pytest

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

ISLE_MAP2 = """\
                        JSSJJSS
                        SSJMSSJ
                        SSSJOSJ
                        JJJSSSS
                        JJJSSSJ"""


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
        """test for converting the array into a map"""
        i1 = Island(ISLE_MAP)
        correct_island = np.array([[Jungle(), Savannah(), Savannah()],
                                   [Savannah(), Savannah(), Jungle()],
                                   [Savannah(), Savannah(), Savannah()]])
        island_shape = np.shape(correct_island)   # type: tuple
        for i in range(island_shape[0]):
            for j in range(island_shape[1]):
                assert type(i1.cells[i, j]) == type(correct_island[i, j])

    def test_add_animal_island(self):
        """test for adding animals to map"""
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

    def test_get_direction(self):
        """test for getting direction to move"""
        pis = (20, 30, 10, 40)
        options = ['right', 'up', 'left', 'down']
        direction = Island.get_direction(pis)
        assert direction in options
        pis = (0, 0, 0, 0)
        option = 'do not move'
        assert Island.get_direction(pis) == option

    def test_get_random_coordinates(self):
        """test for getting random coordinates, for type and length """

        i1 = Island(ISLE_MAP2)
        assert [type(a) == tuple for a in i1.get_random_coordinates()]
        assert [len(a) == 2 for a in i1.get_random_coordinates()]

    def test_get_pi_values_herbivores(self):
        """test for getting pi-values for hebivores"""
        import math
        import pytest

        i1 = Island(ISLE_MAP2)
        coordinate = (2, 3)
        edown = 300/10
        eleft = 300/10

        correct_pi_right = 0
        correct_pi_up = 0
        correct_pi_left = math.exp(1*eleft)
        correct_pi_down = math.exp(1*edown)
        assert i1.get_pi_values_herbivores(coordinate) == pytest.approx(
            (correct_pi_right, correct_pi_up, correct_pi_left, correct_pi_down))

    def test_get_pi_values_carnivores_no_herb(self):
        """test for getting pi_values for carns without any herbivores"""

        i1 = Island(ISLE_MAP2)
        coordinate = (2, 3)

        edown = 0
        eleft = 0
        correct_pi_right = 0
        correct_pi_up = 0
        correct_pi_left = math.exp(1*eleft)
        correct_pi_down = math.exp(1*edown)
        assert i1.get_pi_values_carnivores(coordinate) == pytest.approx(
            (correct_pi_right, correct_pi_up, correct_pi_left, correct_pi_down))

    def test_get_pi_values_carnivores_with_herbs_and_carns(self):
        """test for get_pi_values_carnivores with herbivores and
        ekstra carnivores in adjacent cells"""
        i1 = Island(ISLE_MAP2)
        coordinate = (2, 3)
        i1.add_animal_island((2, 2), INI_HERB[0]['pop'])
        i1.add_animal_island((3, 3), INI_HERB[0]['pop'])
        i1.add_animal_island((3, 3), INI_CARN[0]['pop'])

        correct_weight_left = 400
        correct_weight_right = 400
        eleft = correct_weight_left/50
        edown = correct_weight_right/((20+1)*50)

        correct_pi_left = math.exp(1*eleft)
        correct_pi_up = 0
        correct_pi_right = 0
        correct_pi_down = math.exp(1*edown)
        assert i1.get_pi_values_carnivores(coordinate) == pytest.approx(
            (correct_pi_right, correct_pi_up, correct_pi_left, correct_pi_down))

    def test_cell_move_herbivore_and_carnivore(self):
        """test for movin herbivore and carnivore"""
        i1 = Island(ISLE_MAP2)
        Herbivore.set_parameters({'mu': 1.0})
        Carnivore.set_parameters({'mu': 1.0})

        coordinate = (2, 3)
        i1.add_animal_island(coordinate, INI_HERB[0]['pop'])
        i1.add_animal_island(coordinate, INI_CARN[0]['pop'])
        for herbivore in i1.cells[2, 3].herbivores:
            herbivore.fitness = 1
        for carnivore in i1.cells[2, 3].carnivores:
            carnivore.fitness = 1

        assert len(i1.cells[2, 3].herbivores) == 20
        assert len(i1.cells[2, 3].carnivores) == 20
        i1.cell_move_herbivores(coordinate)
        i1.cell_move_carnivores(coordinate)

        assert len(i1.cells[2, 3].herbivores) == 0
        assert len(i1.cells[2, 3].carnivores) == 0

        # can only move left or down
        len_left_herb = len(i1.cells[2, 2].herbivores_new)
        len_down_herb = len(i1.cells[3, 3].herbivores_new)

        len_left_carn = len(i1.cells[2, 2].carnivores_new)
        len_down_carn = len(i1.cells[3, 3].carnivores_new)

        assert (len_down_herb + len_left_herb,
                len_left_carn + len_down_carn) == (20, 20)

    def test_migration(self):
        """test for migration"""
        i1 = Island(ISLE_MAP2)
        Herbivore.set_parameters({'mu': 1.0})
        Carnivore.set_parameters({'mu': 1.0})

        coordinate = (2, 3)
        i1.add_animal_island(coordinate, INI_HERB[0]['pop'])
        i1.add_animal_island(coordinate, INI_CARN[0]['pop'])

        for herbivore in i1.cells[2, 3].herbivores:
            herbivore.fitness = 1
        for carnivore in i1.cells[2, 3].carnivores:
            carnivore.fitness = 1

        i1.migration()

        # can only move left or down
        len_left_herb = len(i1.cells[2, 2].herbivores)
        len_down_herb = len(i1.cells[3, 3].herbivores)
        len_left_carn = len(i1.cells[2, 2].carnivores)
        len_down_carn = len(i1.cells[3, 3].carnivores)

        assert (len_down_herb + len_left_herb,
                len_left_carn + len_down_carn) == (20, 20)
