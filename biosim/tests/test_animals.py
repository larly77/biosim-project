# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen', 'Lars Martin Boe Lied'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no',\
            'lars.martin.boe.lied@nmbu.no'


from biosim.animals import Herbivore, Carnivore
from biosim.landscape import Jungle


class TestAnimal:
    """Class for testing animal"""

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
        Herbivore.set_parameters({'xi': 1.3, 'w_half': 20})

        assert h1.parameters['xi'] == 1.3
        assert h1.parameters['w_half'] == 20

    def test_feeding_plenty(self):
        """Test for herbivore feeding method with plenty of fodder"""
        h1 = Herbivore(age=5, weight=20)
        j1 = Jungle()
        h1.feeding(j1)
        assert h1.weight == 29
        assert j1.get_fodder() == 790

    def test_feeding_little(self):
        """Test for herbivore feeding method with little fodder"""
        h1 = Herbivore(age=5, weight=20)
        j1 = Jungle()
        j1.fodder = 5
        h1.feeding(j1)
        assert h1.weight == 24.5
        assert j1.get_fodder() == 0

    def test_feeding_none(self):
        """Test for herbivore feeding method with no fodder"""
        h1 = Herbivore(age=5, weight=20)
        j1 = Jungle()
        j1.fodder = 0
        h1.feeding(j1)
        assert h1.weight == 20
        assert j1.get_fodder() == 0

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

    def test_feeding_carnivore_fit(self):
        """Test for carnivore feeding method, with fit carnivore"""
        c1 = Carnivore(1, 3000) # fitness ~= 1
        c1.set_parameters({'DeltaPhiMax': 1.00001})
        j1 = Jungle()
        j1.add_herbivore(5,10)
        j1.herbivores[0].fitness = 0

        boolean = c1.feeding(j1)

        c1.set_parameters({'DeltaPhiMax': 10.0}) # default-value
        assert c1.weight == 3007.5
        assert boolean == [False]

    def test_feeding_carnivore_unfit(self):
        """Test for carnivore feeding method, with unfit carnivore"""
        c1 = Carnivore(1, 20)
        c1.fitness = 0.0001
        c1.set_parameters({'DeltaPhiMax': 1.00001})
        j1 = Jungle()
        j1.add_herbivore(5,10)
        j1.herbivores[0].fitness = 1

        boolean = c1.feeding(j1)

        c1.set_parameters({'DeltaPhiMax': 10.0}) # default-value
        assert c1.weight == 20
        assert boolean == [True]

    def test_feeding_carnivore_appetite(self):
        """Test for a fit carnivore's feeding method, with low appetite"""
        c1 = Carnivore(1, 20)
        c1.fitness = 1
        c1.set_parameters({'DeltaPhiMax': 1.00001, 'F': 10.0})
        j1 = Jungle()
        j1.add_herbivore(5,20)
        j1.herbivores[0].fitness = 0

        boolean = c1.feeding(j1)

        c1.set_parameters({'DeltaPhiMax': 10.0, 'F': 50.0}) # default-value
        assert c1.weight == 27.5
        assert boolean == [False]
