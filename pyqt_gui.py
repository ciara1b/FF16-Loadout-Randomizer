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

    feat_dict = {}
    ability_dict = {}
    eikons = ["Ifrit", "Phoenix", "Garuda", "Ramuh", "Titan", "Bahamut", "Shiva", "Odin", "Leviathan", "Ultima"]

    count = 1
    with open("feats_and_abilities.txt", "r") as f:
        lines = f.readlines()
        for eikon in eikons:
            if eikon == "Ifrit":
                ability_dict[eikons[0]] = lines[0].strip("\n").split(",")
            else:
                feat_dict[eikon] = lines[count].strip("\n")
                ability_dict[eikon] = lines[count+1].strip("\n").split(",")
                count += 2
    f.close()

    randomizer = LoadoutRandomizer(feat_dict, ability_dict)

    window = Window(randomizer)
    window.setWindowTitle("Final Fantasy XVI - Loadout Randomizer")
    window.setGeometry(100, 100, 700, 300)
    window.show()
    sys.exit(app.exec())