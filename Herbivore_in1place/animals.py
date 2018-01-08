# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no'


class Herbivore:
    """"""

    def __init__(self, age, weight):
        self.parameters = {'age': age,
                           'weight': weight,
                           'w_birth': 8.0,
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

        """
        self.age = age
        self.weight = weight
        self.w_birth = 8.0
        self.sigma_birth = 1.5
        self.beta = 0.9
        self.eta = 0.05
        self.a_half = 40.0
        self.phi_age = 0.2
        self.w_half = 10.0
        self.phi_weight = 0.1
        self.mu = 0.25
        self.lambda = 1.0
        self.gamma = 0.2
        self.zeta = 3.5
        self.xi = 1.2
        self.omega = 0.4
        self.F = 10.0
        """

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

    def loss_of_weight(self):
        """Dummy"""

    def death(self):
        """Dummy"""
