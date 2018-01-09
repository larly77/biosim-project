# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen', 'Lars Martin Boe Lied'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no',\
            'lars.martin.boe.lied@nmbu.no'


from animals import Herbivore


class TestHerbivores:
    """Class with tests for the class Herbivores in animals"""

    def test_init_parameters(self):
        """Test input parameters and some default parameters"""
        h1 = Herbivore(age=5, weight=20)

        assert h1.parameters['age'] == 5
        assert h1.parameters['weight'] == 20
        assert h1.parameters['phi_age'] == 0.2
        assert h1.parameters['xi'] == 1.2

    def test_set_parameters(self):
        """Test for the method set_parameters"""
        h1 = Herbivore(age=5, weight=20)
        h1.set_parameters({'age': 4,
                           'xi': 1.3})

        assert h1.parameters['age'] == 4
        assert h1.parameters['xi'] == 1.3

    def test_aging(self):
        """Tests that the animal's age increases properly"""
        h1 = Herbivore(age=5, weight=20)
        h1.aging()
        assert h1.parameters['age'] > 5
        h1.aging()
        assert h1.parameters['age'] == 7

    def test_loss_of_weight(self):
        """Tests that the animal loses weight"""
        h1 = Herbivore(age=5, weight=20)
        h1.loss_of_weight()

        assert h1.parameters['weight'] < 20
        assert h1.parameters['weight'] == (1-0.05)*20
