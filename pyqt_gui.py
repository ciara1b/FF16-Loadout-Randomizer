import sys
from PyQt6.QtWidgets import *

from loadout_randomizer import *

class Window(QWidget):
    def __init__(self, randomizer, parent=None):
        super().__init__(parent)

        self.randomizer = randomizer

        # Button with text, and a parent widget
        self.button = QPushButton(
            text="Randomize",
            parent=self
        )
        self.button.setFixedSize(100, 30)
        self.button.clicked.connect(self.generate_loadout)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)
    
    def generate_loadout(self):
        print(self.randomizer.randomize())

if __name__ == "__main__":
    app = QApplication(sys.argv)

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

    ability_dict = {"Ifrit": ["Will o' the Wykes", "Ignition"],
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

    randomizer = LoadoutRandomizer(feat_dict, ability_dict)

    window = Window(randomizer)
    window.setWindowTitle("Final Fantasy XVI - Loadout Randomizer")
    window.setGeometry(100, 100, 700, 300)
    window.show()
    sys.exit(app.exec())