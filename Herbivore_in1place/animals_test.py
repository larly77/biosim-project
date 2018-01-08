# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no'


from animals import Herbivore




class TestHerbivores:
    """"""

    def test_init_parameters(self):
        h1 = Herbivore(age=5, weight=20)
        assert h1.parameters['age'] == 5
        assert h1.parameters['weight'] == 20
        assert h1.parameters['phi_age'] == 0.2
