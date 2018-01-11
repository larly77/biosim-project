# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen', 'Lars Martin Boe Lied'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no',\
            'lars.martin.boe.lied@nmbu.no'

from landscape import Jungle, Savannah


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
