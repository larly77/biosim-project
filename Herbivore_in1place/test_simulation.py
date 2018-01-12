# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no'


from simulation import BioSim


ISLE_MAP = """\
        JSS
        SSJ
        SSS"""
INI_HERB = [{'loc': (2, 2),
             'pop': [{'species': 'Herbivore',
                      'age': 5,
                      'weight': 20}
                     for _ in range(20)]}]
INI_CARN = [{'loc': (2, 2),
             'pop': [{'species': 'Carnivore',
                      'age': 5,
                      'weight': 40}
                     for _ in range(10)]}]


class TestSimulation:
    """Class for testing simulation"""

    def test_add_population(self):
        """Tests the population is added to cell on island"""
        s1 = BioSim(island_map=ISLE_MAP, ini_pop=INI_HERB, seed=123)
        assert len(s1.island.cells[1, 1].herbivores) == 20
        s1.add_population(INI_HERB)
        assert len(s1.island.cells[1, 1].herbivores) == 40

        assert len(s1.island.cells[1, 1].carnivores) == 0
        s1.add_population(INI_CARN)
        assert len(s1.island.cells[1, 1].carnivores) == 10
