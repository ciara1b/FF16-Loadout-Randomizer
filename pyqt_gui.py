import sys
from PyQt6.QtWidgets import *

from loadout_randomizer import *

class Window(QWidget):
    def __init__(self, randomizer, parent=None):
        super().__init__(parent)

        self.replacement = False
        self.pairing = False
        self.pair_abilities = False
        self.exclude_ability = False
        self.exclude_feat = False
        self.exclude_dlc = True

        self.randomizer = randomizer
        self.chosen_eikons = ["Ifrit", "Phoenix", "Garuda", "Ramuh", "Titan", "Bahamut", "Shiva", "Odin", "Leviathan", "Ultima"]

        # Button with text, and a parent widget
        self.button = QPushButton(
            text="Randomize",
            parent=self
        )
        self.button.setFixedSize(100, 30)
        self.button.clicked.connect(self.finalize_parameters)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)
    
    def generate_loadout(self):
        print(self.randomizer.randomize(self.replacement, self.pairing, self.pair_abilities))
    
    def finalize_parameters(self):
        self.randomizer.set_parameters(self.chosen_eikons, self.exclude_ability, self.exclude_feat, self.exclude_dlc)
        self.generate_loadout()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    randomizer = LoadoutRandomizer()
    window = Window(randomizer)
    window.setWindowTitle("Final Fantasy XVI - Loadout Randomizer")
    window.setGeometry(100, 100, 700, 300)
    window.show()
    sys.exit(app.exec())