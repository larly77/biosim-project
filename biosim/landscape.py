# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen', 'Lars Martin Boe Lied'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no',\
            'lars.martin.boe.lied@nmbu.no'


import copy
from biosim.animals import Herbivore, Carnivore


class Jungle:
    """
    Class for the jungle, containing all methods used in the Jungle-landscape
    """

    DEFAULT_JUNGLE_PARAMETERS = {'f_max': 800.0}
    parameters = copy.deepcopy(DEFAULT_JUNGLE_PARAMETERS)

    @classmethod
    def set_parameters(cls, parameter_changes):
        """
        Method that allows the user to set parameter values for the landscape.

        Parameters
        ----------
        parameter_changes : dict
            The changes to be made to the parameters

        Returns
        -------

        """

        for key in parameter_changes:
            if key in cls.parameters:

                if key is 'f_max':
                    if parameter_changes[key] < 0:
                        raise ValueError("'f_max' must be positive")
                    else:
                        cls.parameters[key] = parameter_changes[key]

                elif key is 'alpha':
                    if 0 <= parameter_changes[key] <= 1:
                        cls.parameters[key] = parameter_changes[key]
                    else:
                        raise ValueError("'alpha' must be in interval [0, 1].")
                else:
                    pass

            else:
                raise KeyError("You have entered an unknown parameter key:'{0}'"
                               ".Keys must be found in Table 2; Column: 'Name'."
                               " Table 2 can be found in the 'Modelling the "
                               "Ecosystem of Rossumøya' project description".
                               format(key))

    def __init__(self):
        """
        Constructor for the jungle class
        """

        self.fodder = copy.deepcopy(self.parameters['f_max'])
        self.herbivores = []
        self.carnivores = []
        self.herbivores_new = []
        self.carnivores_new = []

    def add_herbivore(self, age, weight):
        """
        Method for adding a herbivore into the landscape instance.

        Parameters
        ----------
        age : int
            The age for the herbivore to be added
        weight : float
            The weight for the animal to be added

        Returns
        -------

        """
        self.herbivores.append(Herbivore(age, weight))

    def add_carnivore(self, age, weight):
        """
        Method for adding a carnivore into the landscape-cell

        Parameters
        ----------
        age : int
            The age for the carnivore to be added
        weight : float
            The weight for the carnivore to be added

        Returns
        -------

        """
        self.carnivores.append(Carnivore(age, weight))

    def reset_fodder(self):
        """
        Method that resets the amount of fodder in the jungle to f_max.

        Returns
        -------

        """
        self.fodder = copy.deepcopy(self.parameters['f_max'])

    def reduce_fodder(self, amount):
        """
        Method for reducing the amount of fodder available in landscape instance

        Parameters
        ----------
        amount : float, int
            How much fodder is to be removed from landscape instance.

        Returns
        -------

        """
        self.fodder -= amount

    def get_fodder(self):
        """
        Method for getting fodder in the landscape instance.

        Returns
        -------
        self.fodder : int
            Amount of fodder left is landscape instance.

        """
        return self.fodder
    
    def move_new_animals(self):
        """
        Method for moving animals from the new-lists into the real one.

        Returns
        -------

        """
        self.herbivores += self.herbivores_new
        self.herbivores_new = []
        self.carnivores += self.carnivores_new
        self.carnivores_new = []

    def get_herbivores(self):
        """
        Method for getting a list of all herbivore in the landscape instance

        Returns
        -------
        self.hebivores : list
            List of herbivores in instance

        """
        return self.herbivores

    def get_carnivores(self):
        """
        Method for getting a list of all carnivores in the landscape instance

        Returns
        -------
        self.carnivores : list
            List of carnivores in landscape instance.
        """
        return self.carnivores

    def get_abundance_herbivore(self):
        """
        Method for calculating abundance of food for herbivore in landscape.

        Returns
        -------
        ek : float
            Abundance of food for herbivores in landscape.

        """
        ek = (self.get_fodder())/((len(self.herbivores + self.herbivores_new)
                                   + 1) * Herbivore.parameters['F'])
        return ek

    def get_abundance_carnivore(self):
        """
        Method for calculating abundance of food for carnivore in landscape.

        Returns
        -------
        ek : float
            Abundance of food for carnivores in landscape
        """
        herbivores_weight = 0
        for animal in self.herbivores + self.herbivores_new:
            herbivores_weight += animal.get_weight()

        ek = herbivores_weight / ((len(self.carnivores + self.carnivores_new)
                                   + 1) * Carnivore.parameters['F'])
        return ek

    def feeding(self):
        """
        Method that makes all animals in the cell feed.

        Returns
        -------

        """
        self.reset_fodder()
        self.herbivores.sort(key=lambda x: x.fitness, reverse=True)
        for animal in self.herbivores:
            animal.feeding(landscape_instance=self)

        self.carnivores.sort(key=lambda x: x.fitness, reverse=True)
        self.herbivores.sort(key=lambda x: x.fitness, reverse=False)
        for animal in self.carnivores:
            eaten_bool = animal.feeding(self.herbivores)
            self.herbivores = [animal for index, animal in
                               enumerate(self.herbivores) if eaten_bool[index]]

    def procreation(self):
        """
        Method that makes all animals in the cell try to procreate

        Returns
        -------

        """
        """Method that makes all animals in the cell try to procreate"""
        number_adult_herbivores = len(self.herbivores)
        number_adult_carnivores = len(self.carnivores)

        for animal in self.herbivores:
            animal.procreation(landscape_instance=self,
                               number_of_adults=number_adult_herbivores)
        for animal in self.carnivores:
            animal.procreation(landscape_instance=self,
                               number_of_adults=number_adult_carnivores)

        self.move_new_animals()

    def migration(self):
        """
        Dummy. Migration is handled by the class Island.

        Returns
        -------

        """

    def aging(self):
        """
        Method that makes all animals in the cell age

        Returns
        -------

        """
        for animal in self.herbivores + self.carnivores:
            animal.aging()

    def loss_of_weight(self):
        """
        Method that makes all animals in the cell lose weight

        Returns
        -------

        """
        for animal in self.herbivores + self.carnivores:
            animal.loss_of_weight()

    def death(self):
        """
        Method that makes some animals in the cell die, and remove them.

        Returns
        -------

        """
        self.herbivores = [animal for animal in self.herbivores
                           if not animal.death()]
        self.carnivores = [animal for animal in self.carnivores
                           if not animal.death()]


class Savannah(Jungle):
    """
    Savannah is a subclass of Jungle, inheriting most of its methods
    """

    DEFAULT_SAVANNAH_PARAMETERS = {'f_max': 300.0, 'alpha': 0.3}
    parameters = copy.deepcopy(DEFAULT_SAVANNAH_PARAMETERS)

    def __init__(self):
        super().__init__()

    def reset_fodder(self):
        """
        Method that updates the fodder amount in the savannah each year

        Returns
        -------

        """
        self.fodder += self.parameters['alpha'] * \
            (self.parameters['f_max'] - self.fodder)


class Desert(Jungle):
    """
    Desert is a subclass of Jungle, inheriting most of its methods
    """

    def __init__(self):
        super().__init__()
        self.fodder = 0

    def reset_fodder(self):
        """
        Replaces the method Jungle.reset_fodder. It does nothing

        Returns
        -------

        """

    def feeding(self):
        """
        Replaces the method Jungle.feeding. It does nothing

        Returns
        -------

        """


class Ocean:
    """
    Class for Ocean landscape. Is passive.
    """
    def __init__(self):
        """"""


class Mountain:
    """
    Class for mountain landscape. Is passive.
    """
    def __init__(self):
        """"""
