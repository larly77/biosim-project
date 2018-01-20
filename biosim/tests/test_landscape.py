# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen', 'Lars Martin Boe Lied'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no',\
            'lars.martin.boe.lied@nmbu.no'

from biosim.landscape import Jungle, Savannah
from biosim.animals import Herbivore, Carnivore


class TestLandscape:
    """
    Class for testing landscape
    """
    def test_add_herbivore(self):
        """
        method for testing add_herbivore
        Returns
        -------

        """
        j1 = Jungle()
        assert len(j1.herbivores) == 0
        j1.add_herbivore(5, 20)
        assert j1.herbivores[0].weight == 20
        assert j1.herbivores[0].age == 5
        for _ in range(5):
            j1.add_herbivore(5, 20)
        assert len(j1.herbivores) == 6

    def test_add_carnivores(self):
        """
        method for testing add carnivore
        Returns
        -------

        """
        j1 = Jungle()
        assert len(j1.carnivores) == 0
        j1.add_carnivore(5, 20)
        assert j1.carnivores[0].weight == 20
        assert j1.carnivores[0].age == 5
        for _ in range(5):
            j1.add_carnivore(5, 20)
        assert len(j1.carnivores) == 6

    def test_reset_fodder_jungle(self):
        """
        test for reset fodder in Jungle
        Returns
        -------

        """
        j1 = Jungle()
        j1.fodder = 500.0
        j1.reset_fodder()
        assert j1.fodder == 800.0

    def test_reduce_fodder(self):
        """
        Test for method reduce_fodder
        Returns
        -------

        """
        j1 = Jungle()
        j1.reduce_fodder(100.0)
        assert j1.fodder == 700.0
        j1.reduce_fodder(100.0)
        assert j1.fodder == 600

    def test_get_fodder(self):
        """
        Test for method get_fodder
        Returns
        -------

        """
        j1 = Jungle()
        assert j1.get_fodder() == 800.0
        j1.reduce_fodder(100)
        assert j1.get_fodder() == 700

    def test_reset_fodder_savannah(self):
        """
        Test for the method reset_fodder i Savannah
        Returns
        -------

        """
        """Test for the method Savannah.reset_fodder"""
        s1 = Savannah()
        s1.fodder = 150.0
        s1.reset_fodder()
        assert s1.fodder == 195

    def test_feeding_jungle(self):
        """
        Test that all herbivores in the cell feed: the method feeding
        Returns
        -------

        """
        """Test that all herbivores in the cell feed: the method feeding"""
        j1 = Jungle()
        j1.herbivores = [Herbivore(3, 15), Herbivore(3, 20),
                         Herbivore(3, 30), Herbivore(3, 25)]
        j1.feeding()
        assert j1.get_fodder() == 760
        assert j1.herbivores[0].weight == 24    # j1.feeding sorts by 'weakness'
        assert j1.herbivores[3].weight == 39

    def test_feeding_savannah(self):
        """
        Test that all herbivores in the cell feed: the method feeding
        Returns
        -------

        """
        s1 = Savannah()
        s1.herbivores = [Herbivore(3, 15), Herbivore(3, 20),
                         Herbivore(3, 30), Herbivore(3, 25)]
        s1.feeding()
        assert s1.get_fodder() == 260
        assert s1.herbivores[0].weight == 24
        assert s1.herbivores[3].weight == 39

    def test_procreation(self):
        """
        Test that all animals in cell procreate: the method procreation

        Do this by manipulating the parameter gamma
        Returns
        -------

        """
        s1 = Savannah()
        Herbivore.set_parameters({'gamma': 1})
        s1.herbivores = [Herbivore(age=3, weight=1000) for _ in range(3)]
        s1.procreation()
        Herbivore.set_parameters({'gamma': 0.2})  # default value
        assert len(s1.herbivores_new) == 0
        assert len(s1.get_herbivores()) == 6

    def test_aging(self):
        """
        Test that all animals in the cell age: the method aging
        Returns
        -------

        """
        j1 = Jungle()
        j1.herbivores = [Herbivore(age=3, weight=20) for _ in range(5)]
        j1.aging()
        for animal in j1.herbivores:
            assert animal.age == 4
        j1.aging()
        for animal in j1.herbivores:
            assert animal.age == 5

    def test_loss_of_weight(self):
        """
        Test that all animal in cell lose weight:the method loss_of_weight
        Returns
        -------

        """
        j1 = Jungle()
        j1.herbivores = [Herbivore(age=3, weight=20) for _ in range(5)]
        j1.loss_of_weight()
        for animal in j1.herbivores:
            assert animal.weight == 19

    def test_death(self):
        """
        Test that some animals in the cell die: the method death

        do this by maniplating omega
        Returns
        -------

        """
        j1 = Jungle()
        Herbivore.set_parameters({'omega': 1})
        j1.herbivores = [Herbivore(age=3, weight=20) for _ in range(50)]
        for animal in j1.herbivores:
            animal.fitness = 0
        j1.death()
        Herbivore.set_parameters({'omega': 0.4})  # default value
        assert len(j1.herbivores) == 0

    def test_feeding_carnivores(self):
        """
        Test that all carnivores in the cell feeds: the method feeding

        do this by manipulating parameter DeltaPhiMax and the food
        Returns
        -------

        """
        Carnivore.set_parameters({'DeltaPhiMax': 1.000001})
        Jungle.set_parameters({'f_max': 0.0})
        j1 = Jungle()
        j1.herbivores = [Herbivore(1, 40), Herbivore(2, 50), Herbivore(3, 60)]
        j1.carnivores = [Carnivore(1, 20), Carnivore(2, 20), Carnivore(3, 20)]
        for i in range(3):
            j1.herbivores[i].fitness = 0
            j1.carnivores[i].fitness = 1

        j1.feeding()

        Carnivore.set_parameters({'DeltaPhiMax': 10.0})  # default value
        Jungle.set_parameters({'f_max': 800.0})
        assert (j1.carnivores[0].weight, j1.carnivores[1].weight,
                j1.carnivores[2].weight) == (57.5, 57.5, 20)
        assert j1.herbivores == []
