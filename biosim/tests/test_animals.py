# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen', 'Lars Martin Boe Lied'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no',\
            'lars.martin.boe.lied@nmbu.no'


from biosim.animals import Herbivore, Carnivore
from biosim.landscape import Jungle
import pytest

DEFAULT_HERBIVORE_PARAMETERS = {'w_birth': 8.0,
                                    'sigma_birth': 1.5,
                                    'beta': 0.9,
                                    'eta': 0.05,
                                    'a_half': 40.0,
                                    'phi_age': 0.2,
                                    'w_half': 10.0,
                                    'phi_weight': 0.1,
                                    'mu': 0.25,
                                    'lambda': 1.0,
                                    'gamma': 0.2,
                                    'zeta': 3.5,
                                    'xi': 1.2,
                                    'omega': 0.4,
                                    'F': 10.0}

DEFAULT_CARNIVORE_PARAMETERS = {'w_birth': 6.0,
                                'sigma_birth': 1.0,
                                'beta': 0.75,
                                'eta': 0.125,
                                'a_half': 60.0,
                                'phi_age': 0.4,
                                'w_half': 4.0,
                                'phi_weight': 0.4,
                                'mu': 0.4,
                                'lambda': 1.0,
                                'gamma': 0.8,
                                'zeta': 3.5,
                                'xi': 1.1,
                                'omega': 0.9,
                                'F': 50.0,
                                'DeltaPhiMax': 10.0}

class TestAnimal:
    """
    Class for testing animal.
    """
    @pytest.fixture(autouse=True)
    def set_default_animal(self):
        """
        Method for resetting to default parameters for herbivore and carnivore

        Returns
        -------

        """
        Herbivore.set_parameters(DEFAULT_HERBIVORE_PARAMETERS)
        Carnivore.set_parameters(DEFAULT_CARNIVORE_PARAMETERS)

    def test_init_parameters(self):
        """
        Test for init_parameters, that we can change parameters

        Returns
        -------

        """
        h1 = Herbivore(age=5, weight=20)

        assert h1.age == 5
        assert h1.weight == 20
        assert h1.parameters['phi_age'] == 0.2
        assert h1.parameters['xi'] == 1.2

    def test_set_parameters(self):
        """
        Test for method set_parameters.

        Returns
        -------

        """
        h1 = Herbivore(age=5, weight=20)
        Herbivore.set_parameters({'xi': 1.3, 'w_half': 20})

        assert h1.parameters['xi'] == 1.3
        assert h1.parameters['w_half'] == 20

    def test_feeding_plenty(self):
        """
        Test for herbivore feeding method with plenty of fodder.

        Returns
        -------

        """
        h1 = Herbivore(age=5, weight=20)
        j1 = Jungle()
        h1.feeding(j1)
        assert h1.weight == 29
        assert j1.get_fodder() == 790

    def test_feeding_little(self):
        """
        Test for herbivore feeding method with little fodder.

        Returns
        -------

        """
        h1 = Herbivore(age=5, weight=20)
        j1 = Jungle()
        j1.fodder = 5
        h1.feeding(j1)
        assert h1.weight == 24.5
        assert j1.get_fodder() == 0

    def test_feeding_none(self):
        """
        Test for herbivore feeding method with no fodder.

        Returns
        -------

        """
        h1 = Herbivore(age=5, weight=20)
        j1 = Jungle()
        j1.fodder = 0
        h1.feeding(j1)
        assert h1.weight == 20
        assert j1.get_fodder() == 0

    def test_aging(self):
        """
        Tests that the animal's age increases properly, including fitness.

        Returns
        -------

        """
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
        """
        Tests that the animal loses weight, including fitness update.

        Returns
        -------

        """
        h1 = Herbivore(age=5, weight=20)
        fit_0 = h1.fitness
        h1.loss_of_weight()
        fit_1 = h1.fitness

        assert h1.weight < 20
        assert h1.weight == (1-0.05)*20
        assert fit_1 < fit_0

    def test_feeding_carnivore_fit(self):
        """
        Test for carnivore feeding method, with fit carnivore.

        Returns
        -------

        """
        c1 = Carnivore(1, 3000) # fitness ~= 1
        c1.set_parameters({'DeltaPhiMax': 1.00001})
        j1 = Jungle()
        j1.add_herbivore(5,10)
        j1.herbivores[0].fitness = 0

        boolean = c1.feeding(j1.herbivores)

        c1.set_parameters({'DeltaPhiMax': 10.0}) # default-value
        assert c1.weight == 3007.5
        assert boolean == [False]


    def test_feeding_carnivore_unfit(self):
        """
        Test for carnivore feeding method, with unfit carnivore.

        Returns
        -------

        """
        c1 = Carnivore(1, 20)
        c1.fitness = 0.0001
        c1.set_parameters({'DeltaPhiMax': 1.00001})
        j1 = Jungle()
        j1.add_herbivore(5,10)
        j1.herbivores[0].fitness = 1

        boolean = c1.feeding(j1.herbivores)

        c1.set_parameters({'DeltaPhiMax': 10.0}) # default-value
        assert c1.weight == 20
        assert boolean == [True]

    def test_feeding_carnivore_appetite(self):
        """
        Test for a fit carnivore's feeding method, with low appetite.

        Returns
        -------

        """
        c1 = Carnivore(1, 20)
        c1.fitness = 1
        c1.set_parameters({'DeltaPhiMax': 1.00001, 'F': 10.0})
        j1 = Jungle()
        j1.add_herbivore(5,20)
        j1.herbivores[0].fitness = 0

        boolean = c1.feeding(j1.herbivores)

        c1.set_parameters({'DeltaPhiMax': 10.0, 'F': 50.0}) # default-value
        assert c1.weight == 27.5
        assert boolean == [False]
