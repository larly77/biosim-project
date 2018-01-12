# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no'

import numpy as np
from island import Island


ISLE_MAP = """\
        JSS
        SSJ
        SSS"""
INI_HERB = [{'loc': (10, 10),
             'pop': [{'species': 'Herbivore',
                      'age': 5,
                      'weight': 20}
                     for _ in range(20)]}]


class TestIsland:
    """Class for testing island"""

    def test_string_to_array(self):
        """Test for the method Island.string_to_array"""
        i1 = Island(ISLE_MAP, INI_HERB)
        arry = i1.string_to_array()
        correct_arry = np.array([['J', 'S', 'S'],
                                 ['S', 'S', 'J'],
                                 ['S', 'S', 'S']])
        assert np.array_equal(arry, correct_arry)

#    def test_add_animal_island(self):
#        i1 = Island()
