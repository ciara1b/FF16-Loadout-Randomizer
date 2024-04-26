import copy
import os
from random import *
import sys

class LoadoutRandomizer():

    def __init__(self):
        # add empty keys:value pairs for "No Ability" and "No Feat" settings
        self.feat_dict = {}
        self.ability_dict = {}

    def set_parameters(self, eikons, exclude_ability, exclude_feat, exclude_dlc):
        # reset dictionaries with empty keys:value pairs for "No Ability" and "No Feat" settings
        self.feat_dict = {"": ""}
        self.ability_dict = {"": ["", "", "", "", "", ""]}

        self.eikons = self.exclusion_criteria(exclude_ability, exclude_feat, exclude_dlc, eikons)
        self.fetch_eikon_details()

        self.temp_feat_dict = copy.deepcopy(self.feat_dict)
        self.temp_ability_dict = copy.deepcopy(self.ability_dict)
    
    # method for compiled version
    def get_correct_path(self, relative_path):
        try:
            base_path = sys._MEIPASS + "\\"
        except Exception:
            base_path = os.path.abspath(".")
            base_path = os.path.join(base_path, relative_path)
        
        return base_path
        
    def fetch_eikon_details(self):

        rel_path = self.get_correct_path("")
        count = 1
        with open(rel_path + "feats_and_abilities.txt", "r") as f:
            lines = f.readlines()
            for i, eikon in enumerate(self.eikons):
                if eikon == "Ifrit":
                    self.ability_dict[self.eikons[0]] = lines[0].strip("\n").split(",")
                else:
                    if i != 0:
                        if eikon != "":
                            self.feat_dict[eikon] = lines[count].strip("\n")
                            self.ability_dict[eikon] = lines[count+1].strip("\n").split(",")
                        count += 2

        f.close()

    def exclusion_criteria(self, exclude_ability, exclude_feat, exclude_dlc, eikons):
        # exlcude DLC eikons
        # don't allow no feat
        # don't allow no ability

        if exclude_dlc is True:
            if "Leviathan" in eikons:
                eikons.remove("Leviathan")
            if "Ultima" in eikons:
                eikons.remove("Ultima")
            while len(eikons) > 8:
                eikons.pop(-1)
        if exclude_feat is False:
            self.feat_dict.pop("")
        if exclude_ability is False:
            self.ability_dict.pop("")
        return eikons

    def randomize(self, replacement, pairing, pair_abilities):
        loadout = {}

        # choose feats
        feat_set = self.random_feat()
        while len(feat_set) < 3:
            feat_set.append("")

        # "apply" abilities to every feat
        for feat in feat_set:
            if pairing is True:
                eikon = self.find_eikon_from_feat(feat)
            elif pair_abilities is True:
                paired_abilities = self.random_ability(replacement, pair=pair_abilities)
            else:
                eikon = None
            
            if 'paired_abilities' in locals():
                loadout[feat] = paired_abilities
            else:
                ability_one = self.random_ability(replacement, pair_eikon=eikon)
                ability_two = self.random_ability(replacement, pair_eikon=eikon)
                if feat == "" and feat in list(loadout.keys()):
                    loadout[" "] = [ability_one, ability_two]
                else:
                    loadout[feat] = [ability_one, ability_two]
        
        # reset dictionaries for possible re-randomize
        self.reset_dictionaries()

        return loadout
    
    def find_eikon_from_feat(self, feat):
        if feat != "":
            return list(self.temp_feat_dict.keys())[list(self.temp_feat_dict.values()).index(feat)]
        else:
            return ""
    
    def reset_dictionaries(self):
        self.temp_ability_dict = copy.deepcopy(self.ability_dict)
        self.temp_feat_dict = copy.deepcopy(self.feat_dict)
        return

    def random_feat(self):
        # choose 3 random feats
        return sample(list(self.temp_feat_dict.values()), (3 if len(self.temp_feat_dict) >= 3 else len(self.temp_feat_dict)))

    def random_ability(self, replacement, pair_eikon=None, pair=None):
        # choose a random eikon
        ability_set = ["", None]

        # pair chosen ability with respective eikon if provided
        if (pair_eikon is not None and pair_eikon != "") is True:
            if self.temp_ability_dict[pair_eikon]:
                given_eikon_details = [pair_eikon, self.temp_ability_dict[pair_eikon]]
                if len(self.ability_dict.items()) == 11:
                    ability_set = choices([given_eikon_details, ["", [""]]], weights=[9, 1], k=1)[0]
                else:
                    ability_set = given_eikon_details
        # else if no eikon provided, provided two abilities from same random eikon if requested
        elif pair is True:
            ability_set = choice(list(self.temp_ability_dict.items()))
            
            # check for replacement and ability sets with less than two abilities left
            if (replacement is False) and (len(ability_set[1]) > 1):
                paired_abilities = sample(list(ability_set[1]), 2)
                ability_set[1].remove(paired_abilities[0])
                ability_set[1].remove(paired_abilities[1])
                self.temp_ability_dict[ability_set[0]] = ability_set[1]
            elif (replacement is True) and (len(ability_set[1]) > 0):
                paired_abilities = choices(list(ability_set[1]), k=2)
            elif (len(ability_set[1]) == 0):
                paired_abilities = ["", ""]

            return paired_abilities
        # else parameters don't matter here, just pick an ability at random
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