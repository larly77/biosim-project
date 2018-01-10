# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no'



class BioSim:
    """"""

    def __init__(self, island_map, ini_pop, seed):
        self.map = island_map
        self.pop = ini_pop

        self.seed = seed

    def create_map(self):
        
