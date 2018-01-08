# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no'


import random


class Herbivore:
    """"""

    DEFAULT_PARAMETERS = {'w_birth': 8.0,
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

    def __init__(self, age, weight, default_parameters=DEFAULT_PARAMETERS):
        self.parameters = default_parameters
        self.parameters['age'] = age
        self.parameters['weight'] = weight

    def set_parameters(self, dictionary_changes):
        """"""
#        Idiotsikring her?
        for key in dictionary_changes:
            self.parameters[key] = dictionary_changes[key]

    def feeding(self):
        """Dummy"""

    def procreation(self):
        """Dummy"""

    def migration(self):
        """Dummy"""

    def aging(self):
        """Dummy"""
        self.parameters['age'] += 1

    def loss_of_weight(self):
        """Dummy"""
        self.parameters['weight'] -= self.parameters['eta'] *\
                                     self.parameters['weight']

    def death(self):
        """Dummy"""

#        probability_of_death = self.parameters['omega']*(1-fitness)


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
