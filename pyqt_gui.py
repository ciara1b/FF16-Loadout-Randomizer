import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from loadout_randomizer import *

class MainWindow(QMainWindow):
    def __init__(self, randomizer, parent=None):
        super().__init__()

        self.replacement = False
        self.pairing = False
        self.pair_abilities = False
        self.exclude_ability = False
        self.exclude_feat = False
        self.exclude_dlc = True

        self.randomizer = randomizer
        self.chosen_eikons = ["Ifrit", "Phoenix", "Garuda", "Ramuh", "Titan", "Bahamut", "Shiva", "Odin", "Leviathan", "Ultima"]

        self.layout_setup()

    def layout_setup(self):
        # Button with text, and a parent widget
        button = QPushButton(
            text="Randomize",
            parent=self
        )
        button.setFixedSize(100, 30)
        button.clicked.connect(self.finalize_parameters)

        widget = QWidget()
        layout = QVBoxLayout()

        labels = ["Repeat Abilities", "Match Feats & Abilities", "Pair Abilities", "Allow No Ability", "Allow No Feat", "Exclude DLC Eikons"]
        tooltips = ["Every ability can appear more than once. If you're unlucky, this could result in every ability being the same.",
                    "Example: if one of your feats was Bahamut, it will only choose between Bahamut's abilities to be paired with \nthat feat. If the feat is empty, this will give you two completely random abilites instead.",
                    "Regardless of the chosen feat, for each pair, selected abilities will always be from the same Eikon. This \noption will never give you an empty ability regardless of if 'Allow No Ability' is selected. \nWARNING: this option does nothing if 'Match Feats & Abilities' is also selected.",
                    "Check this if you want it to be possible for any given ability to be empty.",
                    "Check this if you want it to be possible for any given feat to be empty.",
                    "Eikons only available through DLC will not be considered."]

        for i in range(0, 6):
            checkbox = self.create_checkbox()
            if i == 5:
                checkbox.setCheckState(Qt.CheckState.Checked)
            checkbox.setText(labels[i])
            checkbox.setToolTip(tooltips[i])
            layout.addWidget(checkbox)

        layout.addWidget(button)

        layout.addStretch(1)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def create_checkbox(self):
        widget = QCheckBox()
        widget.setCheckState(Qt.CheckState.Unchecked)
        widget.stateChanged.connect(self.show_state)
        return widget
    
    def show_state(self, s):
        print(s == Qt.CheckState.Unchecked.value)
        print(s)
    
    def generate_loadout(self):
        print(self.randomizer.randomize(self.replacement, self.pairing, self.pair_abilities))
    
    def finalize_parameters(self):
        self.randomizer.set_parameters(self.chosen_eikons, self.exclude_ability, self.exclude_feat, self.exclude_dlc)
        self.generate_loadout()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    randomizer = LoadoutRandomizer()
    window = MainWindow(randomizer)
    window.setWindowTitle("Final Fantasy XVI - Loadout Randomizer")
    window.show()
    sys.exit(app.exec())