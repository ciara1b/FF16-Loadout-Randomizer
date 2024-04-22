import copy
from random import *

class LoadoutRandomizer():
    def __init__(self, feat_dict, ability_dict):
        self.feat_dict = feat_dict
        self.temp_feat_dict = copy.deepcopy(self.feat_dict)
        self.ability_dict = ability_dict
        self.temp_ability_dict = copy.deepcopy(self.ability_dict)

    def randomize(self, replacement, exclude_ability, exclude_feat, exclude_dlc, pairing, pair_abilities):
        loadout = {}

        # exlcude DLC eikons
        # don't allow no feat
        # don't allow no ability
        if exclude_dlc is True:
            self.temp_feat_dict.pop("Leviathan")
            self.temp_feat_dict.pop("Ultima")
            self.temp_ability_dict.pop("Leviathan")
            self.temp_ability_dict.pop("Ultima")
        if exclude_feat is False:
            self.temp_feat_dict.pop("")
        if exclude_ability is False:
            self.temp_ability_dict.pop("")

        # choose 3 random feats
        feat_set = sample(list(self.temp_feat_dict.values()), 3)

        # "apply" abilities to every feat
        for feat in feat_set:
            if pairing is True:
                eikon = list(self.temp_feat_dict.keys())[list(self.temp_feat_dict.values()).index(feat)]
            elif pair_abilities is True:
                paired_abilities = self.random_ability(replacement, pair=pair_abilities)
            else:
                eikon = None
            
            if 'paired_abilities' in locals():
                loadout[feat] = paired_abilities
            else:
                ability_one = self.random_ability(replacement, pair_eikon=eikon)
                ability_two = self.random_ability(replacement, pair_eikon=eikon)
                loadout[feat] = [ability_one, ability_two]
        
        # reset dictionaries for possible re-randomize
        self.temp_ability_dict = copy.deepcopy(self.ability_dict)
        self.temp_feat_dict = copy.deepcopy(self.feat_dict)

        return loadout

    def random_ability(self, replacement, pair_eikon=None, pair=None):
        # choose a random eikon
        ability_set = ("", None)

        if (pair_eikon is not None and pair_eikon != "") is True:
            if self.temp_ability_dict[pair_eikon]:
                ability_set = [pair_eikon, self.temp_ability_dict[pair_eikon]]
                ability = choice(list(ability_set[1]))
        elif pair is True:
            ability_set = choice(list(self.temp_ability_dict.items()))
            if (replacement is False) and (len(ability_set[1]) > 1):
                paired_abilities = sample(list(ability_set[1]), 2)
                ability_set[1].remove(paired_abilities[0])
                ability_set[1].remove(paired_abilities[1])
                self.temp_ability_dict[ability_set[0]] = ability_set[1]
            else:
                paired_abilities = choices(list(ability_set[1]), k=2)
            return paired_abilities
        else:
            while ability_set[1] is None or not ability_set[1]:
                ability_set = choice(list(self.temp_ability_dict.items()))
        
        # choose a random ability from that eikon
        ability = choice(ability_set[1])

        # remove that ability (list item) from it's respective eikon (key) in the dictionary
        if replacement is False:
            ability_set[1].remove(ability)
            self.temp_ability_dict[ability_set[0]] = ability_set[1]

        return ability