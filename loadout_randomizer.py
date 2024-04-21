import copy
from random import *

class LoadoutRandomizer():
    def __init__(self, feat_dict, ability_dict, parent=None):
        self.feat_dict = feat_dict
        self.ability_dict = ability_dict
        self.temp_ability_dict = copy.deepcopy(self.ability_dict)

    def randomize(self):
        loadout = {}

        # choose 3 random feats
        feat_set = sample(list(self.feat_dict.values()), 3)

        for feat in feat_set:
            ability_one = self.random_ability_remove()
            ability_two = self.random_ability_remove()

            loadout[feat] = [ability_one, ability_two]
        
        self.temp_ability_dict = copy.deepcopy(self.ability_dict)

        return loadout

    def random_ability_remove(self):
        # choose a random eikon
        ability_set = ("", None)
        while ability_set[1] is None or ability_set[1] == []:
            ability_set = choice(list(self.temp_ability_dict.items()))

        # choose a random ability from that eikon
        ability = choice(ability_set[1])

        # remove that ability (list item) from it's respective eikon (key) in the dictionary
        ability_set[1].remove(ability)
        self.temp_ability_dict[ability_set[0]] = ability_set[1]

        return ability