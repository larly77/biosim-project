# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen', 'Lars Martin Boe Lied'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no',\
            'lars.martin.boe.lied@nmbu.no'


import copy
from animals import Herbivore, Carnivore


class Jungle:
    """"""

    DEFAULT_JUNGLE_PARAMETERS = {'f_max': 800.0}
    parameters = copy.deepcopy(DEFAULT_JUNGLE_PARAMETERS)

    @classmethod
    def set_parameters(cls, dictionary_changes):
        """Method that allows the user to set parameter values for the landscape.
        This replaces the default values."""
        #       Idiotsikring her?

        for key in dictionary_changes:
            cls.parameters[key] = dictionary_changes[key]

    def __init__(self):
        self.fodder = copy.deepcopy(self.parameters['f_max'])
        self.herbivores = []
        self.carnivores = []
        self.herbivores_new = []
        self.carnivores_new = []

    def add_herbivore(self, age, weight):
        """Method for adding a herbivore into the landscape-cell"""
        self.herbivores.append(Herbivore(age, weight))

    def add_carnivore(self, age, weight):
        """Method for adding a carnivore into the landscape-cell"""
        self.carnivores.append(Carnivore(age, weight))

    def reset_fodder(self):
        """Method that set the amount of fodder in the jungle to f_max."""
        self.fodder = copy.deepcopy(self.parameters['f_max'])

    def reduce_fodder(self, amount):
        """"""
        self.fodder -= amount

    def get_fodder(self):
        """"""
        return self.fodder
    
    def move_new_animals(self):
        self.herbivores += self.herbivores_new
        self.herbivores_new = []
        self.carnivores += self.carnivores_new
        self.carnivores_new = []

    def get_herbivores(self):
        """"""
        return self.herbivores

    def get_carnivores(self):
        """"""
        return self.carnivores

    def feeding(self):
        """Method that makes all animals in the cell feed"""
        self.reset_fodder()
        self.herbivores.sort(key=lambda x: x.fitness, reverse=True)
        for animal in self.herbivores:
            animal.feeding(landscape_instance=self)

        self.carnivores.sort(key=lambda x: x.fitness, reverse=True)
        self.herbivores.sort(key=lambda x: x.fitness, reverse=False)
        for animal in self.carnivores:
            eaten_bool = animal.feeding(landscape_instance=self)
            self.herbivores = [animal for index, animal in
                               enumerate(self.herbivores) if eaten_bool[index]]

    def procreation(self):
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
        """Method that makes all animals in the cell try to migrate"""
        liste = [0] * len(self.herbivores + self.carnivores)
        for index, animal in enumerate(self.herbivores + self.carnivores):
            if animal.migration():
                liste[index] = True
        return liste

    def get_abundance_herbivore(self):
        Ek = (self.get_fodder())/((len(self.herbivores + self.herbivores_new) + 1) * Herbivore.parameters['F'] )
        return Ek




    def aging(self):
        """Method that makes all animals in the cell age"""
        for animal in self.herbivores + self.carnivores:
            animal.aging()

    def loss_of_weight(self):
        """Method that makes all animals in the cell lose weight"""
        for animal in self.herbivores + self.carnivores:
            animal.loss_of_weight()

    def death(self):
        """Method that makes some animals in the cell die, and remove them"""

        self.herbivores = [animal for animal in self.herbivores
                           if not animal.death()]
        self.carnivores = [animal for animal in self.carnivores
                           if not animal.death()]


class Savannah(Jungle):
    """"""

    DEFAULT_SAVANNAH_PARAMETERS = {'f_max': 300.0, 'alpha': 0.3}
    parameters = copy.deepcopy(DEFAULT_SAVANNAH_PARAMETERS)

    def __init__(self):
        super().__init__()

    def reset_fodder(self):
        """Method that updates the fodder amount in the savannah each year"""
        self.fodder += self.parameters['alpha'] * \
            (self.parameters['f_max'] - self.fodder)


class Desert(Jungle):
    """"""

    def __init__(self):
        super().__init__()

    def feeding(self):
        """Replaces the method Jungle.feeding. It does nothing."""


class Ocean:
    """Class for ocean-landscape"""
    def __init__(self):
        """"""

class Mountain:
    """Class for mountain-landscape"""
    def __init__(self):
        """"""


if __name__ == '__main__':

    j1 = Jungle()
    s1 = Savannah()
    j2 = Jungle()
    s2 = Savannah()
    m1 = Mountain()

    print(j1.parameters['f_max'])
    print(s1.parameters['f_max'])
    print(j2.parameters['f_max'])
    print(s2.parameters['f_max'], s2.fodder)

    # isinstanse

    print(isinstance(s1, (Jungle, Savannah, Desert)))