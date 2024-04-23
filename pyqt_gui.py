import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from functools import partial

from loadout_randomizer import *
from clickable_image import *

class MainWindow(QMainWindow):
    def __init__(self, randomizer, parent=None):
        super().__init__()

        self.exclusion_criteria = {"replacement": False, "pairing": False, "pair_abilities": False, "exclude_ability": False,
                                   "exclude_feat": False, "exclude_dlc": True}
        self.chosen_eikons = []
        self.temp_eikons = ["Leviathan", "Utima"]
        self.init_eikons()

        self.randomizer = randomizer

        self.widget = QWidget()
        self.layout = QGridLayout()
        for i in range(21):
            r = (6 % (i + 1)) // 6
            self.layout.setColumnStretch(i % 6, 1)
            self.layout.setRowStretch(r, 1)
        self.layout_setup()

    def init_eikons(self):
        if len(self.chosen_eikons) == 8:
            self.chosen_eikons.append("" if self.temp_eikons[0] == "" else "Leviathan")
            self.chosen_eikons.append("" if self.temp_eikons[1] == "" else "Ultima")
        elif len(self.chosen_eikons) == 0:
            self.chosen_eikons = ["Ifrit", "Phoenix", "Garuda", "Ramuh", "Titan", "Bahamut", "Shiva", "Odin", "Leviathan", "Ultima"]
        return

    def layout_setup(self):
        # Button with text, and a parent widget
        button = QPushButton(text="Randomize", parent=self)
        button.setFixedSize(100, 30)
        button.clicked.connect(self.finalize_parameters)

        # labels and tooltips for checkboxes
        labels = ["Repeat Abilities", "Match Feats & Abilities", "Pair Abilities", "Allow No Ability", "Allow No Feat", "Exclude DLC Eikons"]
        tooltips = ["Every ability can appear more than once. If you're unlucky, this could result in every ability being the same.",
                    "Example: if one of your feats was Bahamut, it will only choose between Bahamut's abilities to be paired with \nthat feat. If the feat is empty, this will give you two completely random abilites instead.",
                    "Regardless of the chosen feat, for each pair, selected abilities will always be from the same Eikon. This \noption will never give you an empty ability regardless of if 'Allow No Ability' is selected. \nWARNING: this option does nothing if 'Match Feats & Abilities' is also selected.",
                    "Check this if you want it to be possible for any given ability to be empty.",
                    "Check this if you want it to be possible for any given feat to be empty.",
                    "Eikons only available through DLC will not be considered."]

        # create checkboxes
        for i in range(0, 6):
            checkbox = self.create_checkbox(labels[i], tooltips[i], list(self.exclusion_criteria)[i])
            if i == 5:
                checkbox.setCheckState(Qt.CheckState.Checked)
            self.layout.addWidget(checkbox, i, 0)

        # create images
        count = 1
        for i in range(0, len(self.chosen_eikons)):
            eikon_icon = PicButton("./Assets/Eikon Icons/" + self.chosen_eikons[i] + "_icon.png")
            if i <= 4:
                self.layout.addWidget(eikon_icon, 0, count)
                count += 1
            else:
                count = 4
                self.layout.addWidget(eikon_icon, 1, i-count)
            eikon_icon.clicked.connect(partial(self.set_image, self.chosen_eikons[i]))
    
        titles = QLabel(text="Feats\t\tAbilities")
        self.layout.addWidget(titles, 2, 1)
        for i in range (3):
            current_set = QLabel(text="")
            self.layout.addWidget(current_set, i+3, 1)

        self.layout.addWidget(button, 6, 0)

        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def create_checkbox(self, text, tooltip, name):
        widget = QCheckBox()
        widget.setCheckState(Qt.CheckState.Unchecked)
        widget.stateChanged.connect(partial(self.set_state, name))
        widget.setText(text)
        widget.setToolTip(tooltip)
        widget.setAccessibleName(name)
        return widget
    
    def set_state(self, name):
        i = 0
        checkboxes = (self.layout.itemAt(i) for i in range(self.layout.count()))
        for item in checkboxes:
            self.exclusion_criteria[item.widget().accessibleName()] = (True if item.widget().isChecked() else False)
            i += 1
            if i >= 6:
                break
    
    def set_image(self, eikon):

        eikon_icons = [self.layout.itemAt(i).widget() for i in range(6, 6 + len(self.chosen_eikons))]
        for icon in eikon_icons:
            if eikon in icon.get_image():
                if icon.get_selected() is False:
                    self.chosen_eikons[eikon_icons.index(icon)] = eikon
                    selected = True
                else:
                    self.chosen_eikons[self.chosen_eikons.index(eikon)] = ""
                    selected = False
                icon.set_pixmap(selected)
                break
        self.temp_eikons = copy.deepcopy(self.chosen_eikons[8:10])
    
    def generate_loadout(self):
        results = self.randomizer.randomize(self.exclusion_criteria.get("replacement"), self.exclusion_criteria.get("pairing"),
                                        self.exclusion_criteria.get("pair_abilities"))
        keys = list(results.keys())
        values = list(results.values())

        i = 0
        sets_labels = [self.layout.itemAt(i).widget() for i in range(17, 20)]
        for set_label in sets_labels:
            if keys[i] == "" or keys[i] == " ":
                key_text = "EMPTY: \t\t"
            else:
                key_text = keys[i] + ": \t"

            if values[i][0] == (""):
                value_one_text = "EMPTY"
            else:
                value_one_text = values[i][0]
            if values[i][1] == (""):
                value_two_text = "EMPTY"
            else:
                value_two_text = values[i][1]

            set_label.setText(key_text + value_one_text + ", " + value_two_text)
            i += 1

        self.init_eikons()
    
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