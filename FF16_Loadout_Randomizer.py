from random import *

feat_dict = {"Phoenix": "Phoenix Shift", 
             "Garuda": "Deadly Embrace",
             "Ramuh": "Blind Justice",
             "Titan": "Titanic Block",
             "Bahamut": "Wings of Light",
             "Shiva": "Cold Snap",
             "Odin": "Arm of Darkness",
             "Leviathan": "Serpent's Cry",
             "Ultima": "Ascension"
             }

ability_dict = {"Ifrit": ["Will o' the Wykes", "Ignition", "", ""],
                "Phoenix": ["Rising Flames", "Heatwave", "Flames of Rebirth", "Scarlet Cyclone"],
                "Garuda": ["Gouge", "Wicked Wheel", "Rook's Gambit", "Aerial Blast"],
                "Ramuh": ["Thunderstorm", "Judgement Bolt", "Lightning Rod", "Pile Drive"],
                "Titan": ["Upheavel", "Raging Fists", "Windup", "Earthen Fury"],
                "Bahamut": ["Flare Breath", "Impulse", "Satellite", "Gigaflare"],
                "Shiva": ["Diamond Dust", "Rime", "Ice Age", "Mesmerize"],
                "Odin": ["Gungnir", "Heaven's Cloud", "Rift Slip", "Dancing Steel"],
                "Leviathan": ["Deluge", "Abyssal Tear", "Tsunami", "Cross Swell"],
                "Ultima": ["Dominion", "Proselytize", "Voice of God", "Ultimate Demise"]
                }

def randomizer(feats, abilities):
    loadout = {}
    # choose 3 random feats
    feat_set = sample(list(feats.values()), 3)

    for feat in feat_set:
        ability_one, abilities = random_ability_remove(abilities)
        ability_two, abilities = random_ability_remove(abilities)

        loadout[feat] = [ability_one, ability_two]

    return loadout

def random_ability_remove(abilities):
    # choose a random eikon
    ability_set = choice(list(abilities.items()))

    # choose a random ability from that eikon
    ability = choice(ability_set[1])

    # remove that ability (list item) from it's respective eikon (key) in the dictionary
    abilities[ability_set[0]] = ability_set[1].remove(ability)

    return ability, abilities

print(randomizer(feat_dict, ability_dict))