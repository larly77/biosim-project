# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen', 'Lars Martin Boe Lied'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no',\
            'lars.martin.boe.lied@nmbu.no'


import random
import math
import copy


class Herbivore:
    """"""

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
    parameters = copy.deepcopy(DEFAULT_HERBIVORE_PARAMETERS)

    @classmethod
    def set_parameters(cls, dictionary_changes):
        """Method that allows the user to set parameter values for the animal.
        This replaces the default values."""
        #       Idiotsikring her?

        for key in dictionary_changes:
            cls.parameters[key] = dictionary_changes[key]

    def __init__(self, age, weight):
        self.age = age
        self.weight = weight
        self.fitness = None
        self.update_fitness()

    def update_fitness(self):
        """Method to update the fitness of the animal"""
        q_plus = 1/(1+math.exp(self.parameters['phi_age'] *
                               (self.age -
                                self.parameters['a_half'])))
        q_minus = 1/(1+math.exp(-self.parameters['phi_weight'] *
                                (self.weight -
                                self.parameters['w_half'])))

        self.fitness = q_plus * q_minus

    def feeding(self, landscape_instance):
        """Dummy"""

        available_fodder = landscape_instance.get_fodder()
        appetite = self.parameters['F']
        if available_fodder >= appetite:
            self.weight += self.parameters['beta'] * appetite
            landscape_instance.reduce_fodder(appetite)
        if 0 < available_fodder < appetite:
            self.weight += self.parameters['beta'] * available_fodder
            landscape_instance.fodder = 0

    def procreation(self, landscape_instance, number_of_adults):
        """Dummy"""
        if self.weight >= self.parameters['zeta'] * (
                self.parameters['w_birth'] + self.parameters['sigma_birth']):
            probability_of_birth = min([1, self.parameters['gamma'] *
                                        self.fitness * (number_of_adults-1)])

            if random.random() < probability_of_birth:
                weight_birth = random.gauss(self.parameters['w_birth'],
                                            self.parameters['sigma_birth'])
                self.weight -= self.parameters['xi'] * weight_birth

                if type(self).__name__ == 'Herbivore':
                    landscape_instance.herbivores_newborn.append(
                        Herbivore(age=0, weight=weight_birth))
                if type(self).__name__ == 'Carnivore':
                    landscape_instance.carnivores_newborn.append(
                        Carnivore(age=0, weight=weight_birth))

    def migration(self):
        """Dummy"""

    def aging(self):
        """Method that increases the age of the animal by one year"""
        self.age += 1
        self.update_fitness()

    def loss_of_weight(self):
        """Method that decreases the weight of the animal by a percent-value"""
        self.weight -= self.parameters['eta'] *\
            self.weight
        self.update_fitness()

    def death(self):
        """Dummy"""

        probability_of_death = self.parameters['omega'] * (1-self.fitness)
        return random.random() < probability_of_death


class Carnivore(Herbivore):
    """"""

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
    parameters = copy.deepcopy(DEFAULT_CARNIVORE_PARAMETERS)


# Følgende angir hvordan en docstring bør se ut.
# Med det formatet blir dokumentasjons-porsessen meget grei,
# når vi lærer Sphinx-programmet.
def f(x):
    """
    one line description

    many line description

    Parameters
    ----------
    x : float
        Description of x

    Returns
    -------
    y : float
        The bladibla

    Raises
    ------
    ValueError
        If x is not numeric
    """


if __name__ == '__main__':
    h1 = Herbivore(3, 20)
    print(type(h1).__name__)
