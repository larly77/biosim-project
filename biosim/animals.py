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
    def set_parameters(cls, parameter_changes):
        """
        Method that allows the user to set parameter values for the animal.

        Method that allows the user to set parameter values for the animal.
        This replaces the default values.

        Parameters
        ----------
        parameter_changes : dictionary
            A dictionary with one or more keys to set new parameters for the
            animal. The items should be numeric.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If parameter_changes contain contain keys not already in the
            dictionary. 
        """

        #       Idiotsikring her?

        for key in parameter_changes:
            cls.parameters[key] = parameter_changes[key]

    def __init__(self, age, weight):
        """
        init-function for setting age and weight to a herbivore
        Parameters
        ----------
        age : int
            age of herbivore
        weight : float
            weight of herbivore
        """
        self.age = age
        self.weight = weight
        self.fitness = None
        self.update_fitness()

    def update_fitness(self):
        """
        Method for updating fitness
        Returns
        -------
        An updated value of fitness

        """
        q_plus = 1/(1+math.exp(self.parameters['phi_age'] *
                               (self.age -
                                self.parameters['a_half'])))
        q_minus = 1/(1+math.exp(-self.parameters['phi_weight'] *
                                (self.weight -
                                self.parameters['w_half'])))

        self.fitness = q_plus * q_minus

    def get_weight(self):
        """
        Returns
        -------
        returns the weight of the animal

        """
        return self.weight

    def feeding(self, landscape_instance):
        """
        Handles the feeding of  the animal
        Parameters
        ----------
        landscape_instance : The tile, that the given animal is in

        Returns
        -------

        """
        available_fodder = landscape_instance.get_fodder()
        appetite = self.parameters['F']
        if available_fodder >= appetite:
            self.weight += self.parameters['beta'] * appetite
            landscape_instance.reduce_fodder(appetite)
            self.update_fitness()
        elif 0 < available_fodder < appetite:
            self.weight += self.parameters['beta'] * available_fodder
            landscape_instance.fodder = 0
            self.update_fitness()
        else:
            pass

    def procreation(self, landscape_instance, number_of_adults):
        """
        Handles the procreation of the animals
        Parameters
        ----------
        landscape_instance : object
            The tile of the animal
        number_of_adults : int
            Number of animals old enough to procreate

        Returns
        -------

        """
        if self.weight >= self.parameters['zeta'] * (
                self.parameters['w_birth'] + self.parameters['sigma_birth']):
            probability_of_birth = min([1, self.parameters['gamma'] *
                                        self.fitness * (number_of_adults-1)])

            if random.random() < probability_of_birth:
                weight_birth = random.gauss(self.parameters['w_birth'],
                                            self.parameters['sigma_birth'])
                self.weight -= self.parameters['xi'] * weight_birth

                if type(self).__name__ == 'Herbivore':
                    landscape_instance.herbivores_new.append(
                        Herbivore(age=0, weight=weight_birth))
                if type(self).__name__ == 'Carnivore':
                    landscape_instance.carnivores_new.append(
                        Carnivore(age=0, weight=weight_birth))

    def migration(self):
        """
        Method for checking if the animal will migrate
        Returns
        -------
        True or False value, wether the animal wil move or not

        """
        probability_move = self.parameters['mu'] * self.fitness
        return random.random() < probability_move

    def aging(self):
        """
        Method for handling the aging of an animal, also update fitness
        Returns
        -------

        """
        """Method that increases the age of the animal by one year"""
        self.age += 1
        self.update_fitness()

    def loss_of_weight(self):
        """
        Method for handling the loss of weight, by natural causes

        A mathod for decreasing the weight of animal every year by a parameter
        'eta' multiplied by the animals own weight, also updates fitness
        Returns
        -------

        """
        """Method that decreases the weight of the animal by a percent-value"""
        self.weight -= self.parameters['eta'] *\
            self.weight
        self.update_fitness()

    def death(self):
        """
        Method for for checking if the animal should die from natural causes

        Calculates the chance of dying due to low fitness, by using the
        parameter 'omega'
        Returns
        -------

        """
        probability_of_death = self.parameters['omega'] * (1-self.fitness)
        return random.random() < probability_of_death


class Carnivore(Herbivore):

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

    def __init__(self, age, weight):
        """
        Init function for carnivores

        The carnivore class is a subclass of the Herbivore class, using most of
        the methods from Herbivore except the feeding method
        Parameters
        ----------
        age : int
            Age of animal
        weight : float
            Weight of animal
        """
        super().__init__(age, weight)

    def feeding(self, preys):
        """
        Feeding method for carnivores

        Goes though all the herbivores in the same tile as the carnivore
        and checks if the carnivore eats it or not, depending on fitness of
        both carnivore an herbivore, the parameters 'DeltaPhiMax' and 'beta and
        the appetite of the carnivore and a bit of luck.
        It also updates the weight and fitness of the carnivore.
        Parameters
        ----------
        preys : list
            A list of all the herbivores on the same tile as the given carnovre

        Returns
        -------
        eaten_bool : list
            Liste of true/false values for which herbivores to be eaten

        """
        appetite = copy.deepcopy(self.parameters['F'])
        eaten_bool = [True] * len(preys)
        for index, prey in enumerate(preys):
            if appetite >= prey.get_weight():
                if self.fitness <= prey.fitness:
                    continue
                elif 0 < self.fitness - prey.fitness < \
                        self.parameters['DeltaPhiMax']:

                    probability = (self.fitness - prey.fitness) /\
                                  self.parameters['DeltaPhiMax']
                    if random.random() < probability:
                        eaten_bool[index] = False
                        self.weight += self.parameters['beta'] * prey.weight
                        appetite -= prey.weight
                        self.update_fitness()
                else:
                    eaten_bool[index] = False
                    self.weight += self.parameters['beta'] * prey.weight
                    appetite -= prey.weight
                    self.update_fitness()

            elif 0 < appetite < prey.get_weight():
                if self.fitness <= prey.fitness:
                    continue
                elif 0 < self.fitness - prey.fitness < \
                        self.parameters['DeltaPhiMax']:

                    probability = (self.fitness - prey.fitness) /\
                                  self.parameters['DeltaPhiMax']
                    if random.random() < probability:
                        eaten_bool[index] = False
                        self.weight += self.parameters['beta'] * appetite
                        appetite = 0
                        self.update_fitness()
                else:
                    eaten_bool[index] = False
                    self.weight += self.parameters['beta'] * appetite
                    appetite = 0
                    self.update_fitness()
            else:
                continue

        return eaten_bool

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
    print(x)


if __name__ == '__main__':
    h1 = Herbivore(3, 20)
    print(type(h1).__name__)
