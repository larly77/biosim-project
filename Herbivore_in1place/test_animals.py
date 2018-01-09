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
        """Test input values and some default parameters"""
        h1 = Herbivore(age=5, weight=20)

        assert h1.age == 5
        assert h1.weight == 20
        assert h1.parameters['phi_age'] == 0.2
        assert h1.parameters['xi'] == 1.2

    def test_set_parameters(self):
        """Test for the method set_parameters"""
        h1 = Herbivore(age=5, weight=20)
        h1.set_parameters({'xi': 1.3, 'w_half': 20})

        assert h1.parameters['xi'] == 1.3
        assert h1.parameters['w_half'] == 20

    def test_aging(self):
        """Tests that the animal's age increases properly, including fitness"""
        h1 = Herbivore(age=5, weight=20)
        fit_0 = h1.fitness

        h1.aging()
        fit_1 = h1.fitness
        assert h1.age > 5
        assert fit_1 < fit_0

        h1.aging()
        fit_2 = h1.fitness
        assert h1.age == 7
        assert fit_2 < fit_1 and fit_2 < fit_0

    def test_loss_of_weight(self):
        """Tests that the animal loses weight, including fitness update"""
        h1 = Herbivore(age=5, weight=20)
        fit_0 = h1.fitness
        h1.loss_of_weight()
        fit_1 = h1.fitness

        assert h1.weight < 20
        assert h1.weight == (1-0.05)*20
        assert fit_1 < fit_0
