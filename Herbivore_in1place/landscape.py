# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen', 'Lars Martin Boe Lied'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no',\
            'lars.martin.boe.lied@nmbu.no'


import copy


DEFAULT_JUNGLE_PARAMETERS = {'f_max': 800.0}
DEFAULT_SAVANNAH_PARAMETERS = {'f_max': 300.0, 'alpha': 0.3}


class Jungle:
    """"""

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
        self.herbivore_list = []
        self.carnivore_list = []

    def reset_fodder(self):
        """Method that set the amount of fodder in the jungle to f_max."""
        self.fodder = copy.deepcopy(self.parameters['f_max'])

    def reduce_fodder(self, amount):
        """"""
        self.fodder -= amount

    def get_fodder(self):
        """"""
        return self.fodder
