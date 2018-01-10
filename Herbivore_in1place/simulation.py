# -*- coding: utf-8 -*-

"""
"""

__author__ = 'Jon-Fredrik Blakstad Cappelen'
__email__ = 'jon-fredrik.blakstad.cappelen@nmbu.no'


from landscape import Jungle, Savannah
from animals import Herbivore
import numpy as np
import copy


class BioSim:
    """"""

    def __init__(self, island_map, ini_pop, seed):
        self.map = island_map
        self.pop = ini_pop
        self.island = None
        self.location = None

        self.seed = seed

    def string_to_array(self):
        """"""

        temp_map = copy.deepcopy(self.map.replace(" ", ""))
        a = list(temp_map)

        # fjerner '\n' og finner hvor lange radene skal være
        a2 = [e for e in a if '\n' not in e]
        for element in a:
            if element == '\n':
                line_length = len(a[0:a.index(element)])
                break

        # deler lista inn i like store chunks, som passer med radlengden vi fant over
        a3 = []
        for i in range(0, len(a2), line_length):
            af = a2[i:i + line_length]
            a3.append(af)

        # lager en array av det
        a4 = np.array(a3)
        return a4



    def simulate_in_one_place_herbivores(self, num_steps):

        # Make 'one place'
        if self.location is None:
            if self.map == 'J':
                self.location = Jungle()
            if self.map == 'S':
                self.location = Savannah()

        # Populate 'one place'
            for animal in self.pop[0]['pop']:
                if animal['species'] == 'Herbivore':
                    self.location.herbivore_list.append(
                        Herbivore(weight=animal['weight'], age=animal['age']))

        # Run thru num_steps years
        for year in range(num_steps):

            # Feeding
            self.location.reset_fodder()
#            self.location.herbivore_list.sort(key=fitness) #???

            for herbivore in self.location.herbivore_list:
                herbivore.feeding(landscape_instance=self.location)

            # Procreation
            number_adults = len(self.location.herbivore_list)

            for herbivore in self.location.herbivore_list:
                herbivore.procreation(self.location, number_adults)

            self.location.herbivore_list += self.location.herbivore_list_newborn
            self.location.herbivore_list_newborn = []

            # Skip Migration

            # Aging
            for herbivore in self.location.herbivore_list:
                herbivore.aging()

            # Loss of weight
            for herbivore in self.location.herbivore_list:
                herbivore.loss_of_weight()

            # Death
            index_list = []

            for index, herbivore in enumerate(self.location.herbivore_list):
                index_list.append(herbivore.death(index_animal_list=index))

            index_list = [el for el in index_list if el is not 'placeholder']

            index_list = [self.location.herbivore_list[index] for index in index_list]
            self.location.herbivore_list = [el for el in self.location.herbivore_list if el not in index_list]

            for animal in self.location.get_herbivore_list():
                print(animal.age, animal.weight)
            print('Year over:', year)
            print('Number of Herbivores: ', len(self.location.get_herbivore_list()))


if __name__ == '__main__':

    ini_herb = [{'loc': (10, 10),
                 'pop': [{'species': 'Herbivore',
                          'age': 5,
                          'weight': 20}
                         for _ in range(20)]}]

    sim = BioSim(island_map="""J""", ini_pop=ini_herb, seed=123)

    sim.simulate_in_one_place_herbivores(200)
