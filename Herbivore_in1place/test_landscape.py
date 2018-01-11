# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen', 'Lars Martin Boe Lied'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no',\
            'lars.martin.boe.lied@nmbu.no'

from landscape import Jungle, Savannah
from animals import Herbivore


class TestLandscape:
    """Class for testing landscape"""

    def test_reset_fodder_jungle(self):
        """Test for the method Jungle.reset_fodder"""
        j1 = Jungle()
        j1.fodder = 500.0
        j1.reset_fodder()
        assert j1.fodder == 800.0

    def test_reduce_fodder(self):
        """Test for method reduce_fodder"""
        j1 = Jungle()
        j1.reduce_fodder(100.0)
        assert j1.fodder == 700.0
        j1.reduce_fodder(100.0)
        assert j1.fodder == 600

    def test_get_fodder(self):
        """Test for method get_fodder"""
        j1 = Jungle()
        assert j1.get_fodder() == 800.0
        j1.reduce_fodder(100)
        assert j1.get_fodder() == 700

    def test_reset_fodder_savannah(self):
        """Test for the method Savannah.reset_fodder"""
        s1 = Savannah()
        s1.fodder = 150.0
        s1.reset_fodder()
        assert s1.fodder == 195

    def test_feeding_jungle(self):
        """Test that all animals in the cell feeds: the method feeding"""
        j1 = Jungle()
        j1.herbivore_list = [Herbivore(3, 15), Herbivore(3, 20),
                             Herbivore(3, 30), Herbivore(3, 25)]
        j1.feeding()
        assert j1.get_fodder() == 760
        assert j1.herbivore_list[0].weight == 39
        assert j1.herbivore_list[3].weight == 24

    def test_feeding_savannah(self):
        """Test that all animals in the cell feeds: the method feeding"""
        s1 = Savannah()
        s1.herbivore_list = [Herbivore(3, 15), Herbivore(3, 20),
                             Herbivore(3, 30), Herbivore(3, 25)]
        s1.feeding()
        assert s1.get_fodder() == 260
        assert s1.herbivore_list[0].weight == 39
        assert s1.herbivore_list[3].weight == 24
