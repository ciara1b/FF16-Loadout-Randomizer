import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

from loadout_randomizer import *

class MainWindow(QMainWindow):
    def __init__(self, randomizer, parent=None):
        super().__init__()

        self.exclusion_criteria = {"replacement": False, "pairing": False, "pair_abilities": False, "exclude_ability": False,
                                   "exclude_feat": False, "exclude_dlc": True}

        self.randomizer = randomizer
        self.chosen_eikons = ["Ifrit", "Phoenix", "Garuda", "Ramuh", "Titan", "Bahamut", "Shiva", "Odin", "Leviathan", "Ultima"]

        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.layout_setup()

    def layout_setup(self):
        # Button with text, and a parent widget
        button = QPushButton(
            text="Randomize",
            parent=self
        )
        button.setFixedSize(100, 30)
        button.clicked.connect(self.finalize_parameters)

        labels = ["Repeat Abilities", "Match Feats & Abilities", "Pair Abilities", "Allow No Ability", "Allow No Feat", "Exclude DLC Eikons"]
        tooltips = ["Every ability can appear more than once. If you're unlucky, this could result in every ability being the same.",
                    "Example: if one of your feats was Bahamut, it will only choose between Bahamut's abilities to be paired with \nthat feat. If the feat is empty, this will give you two completely random abilites instead.",
                    "Regardless of the chosen feat, for each pair, selected abilities will always be from the same Eikon. This \noption will never give you an empty ability regardless of if 'Allow No Ability' is selected. \nWARNING: this option does nothing if 'Match Feats & Abilities' is also selected.",
                    "Check this if you want it to be possible for any given ability to be empty.",
                    "Check this if you want it to be possible for any given feat to be empty.",
                    "Eikons only available through DLC will not be considered."]

        # create checkboxes
        for i in range(0, 6):
            checkbox = self.create_checkbox()
            if i == 5:
                checkbox.setCheckState(Qt.CheckState.Checked)
            checkbox.setText(labels[i])
            checkbox.setToolTip(tooltips[i])
            self.layout.addWidget(checkbox)

        self.layout.addWidget(button)

        self.layout.addStretch(1)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def create_checkbox(self):
        widget = QCheckBox()
        widget.setCheckState(Qt.CheckState.Unchecked)
        widget.stateChanged.connect(self.set_state)
        return widget
    
    def set_state(self, s):
        i = 0
        checkboxes = (self.layout.itemAt(i) for i in range(self.layout.count()))
        for item in checkboxes:
            current_key = list(self.exclusion_criteria)[i]
            self.exclusion_criteria[current_key] = (True if item.widget().isChecked() else False)
            i += 1
            if i >= 6:
                break
    
    def generate_loadout(self):
        print(self.randomizer.randomize(self.exclusion_criteria.get("replacement"), self.exclusion_criteria.get("pairing"),
                                        self.exclusion_criteria.get("pair_abilities")))
    
    def finalize_parameters(self):
        self.randomizer.set_parameters(self.chosen_eikons, self.exclusion_criteria.get("exclude_ability"),
                                       self.exclusion_criteria.get("exclude_feat"), self.exclusion_criteria.get("exclude_dlc"))
        self.generate_loadout()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    randomizer = LoadoutRandomizer()
    window = MainWindow(randomizer)
    window.setWindowTitle("Final Fantasy XVI - Loadout Randomizer")
    window.show()
    sys.exit(app.exec())