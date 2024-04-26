import os
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
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

        # set up style
        self.styleComboBox = QComboBox()
        self.styleComboBox.addItems(QStyleFactory.keys())
        self.changeStyle("Fusion")
        
        self.widget = QWidget()
        self.layout = QGridLayout()
        self.layout_setup()

    # method for compiled version
    def get_correct_path(self, relative_path):
        try:
            base_path = sys._MEIPASS + "\\"
        except Exception:
            base_path = os.path.abspath(".")
            base_path = os.path.join(base_path, relative_path)
        
        return base_path

    def init_eikons(self):
        if len(self.chosen_eikons) == 8:
            self.chosen_eikons.append("" if self.temp_eikons[0] == "" else "Leviathan")
            self.chosen_eikons.append("" if self.temp_eikons[1] == "" else "Ultima")
        elif len(self.chosen_eikons) == 0:
            self.chosen_eikons = ["Ifrit", "Phoenix", "Garuda", "Ramuh", "Titan", "Bahamut", "Shiva", "Odin", "Leviathan", "Ultima"]
        return
    
    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        QApplication.setPalette(QApplication.style().standardPalette())

    def layout_setup(self):
        # Button with text, and a parent widget
        button = QPushButton(text="Randomize", parent=self)
        button.setFixedSize(100, 30)
        button.clicked.connect(self.finalize_parameters)

        # labels and tooltips for checkboxes
        labels = ["Repeat Abilities", "Match Feats && Abilities", "Pair Abilities", "Allow No Ability", "Allow No Feat", "Exclude DLC"]
        tooltips = ["Every ability can appear more than once. If you're unlucky, this could result in every ability being the same.",
                    "Example: if one of your feats was Bahamut, it will only choose between Bahamut's abilities to be paired with \nthat feat. If the feat is empty, this will give you two completely random abilites instead.",
                    "Regardless of the chosen feat, for each pair, selected abilities will always be from the same Eikon. This \noption will never give you an empty ability regardless of if 'Allow No Ability' is selected. \nWARNING: this option does nothing if 'Match Feats & Abilities' is also selected.",
                    "Check this if you want it to be possible for any given ability to be empty.",
                    "Check this if you want it to be possible for any given feat to be empty.",
                    "Eikons only available through DLC will not be considered."]

        # create checkboxes
        checkboxesGroup = QGroupBox("Parameters")
        vLayout = QVBoxLayout()
        for i in range(0, 6):
            checkbox = self.create_checkbox(labels[i], tooltips[i], list(self.exclusion_criteria)[i])
            if i == 5:
                checkbox.setCheckState(Qt.CheckState.Checked)
            vLayout.addWidget(checkbox, alignment=(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft))
        checkboxesGroup.setLayout(vLayout)
        self.layout.addWidget(checkboxesGroup, 2, 0, 4, 2)

        # create images
        count = 0
        rel_path = self.get_correct_path("./Assets/Eikon Icons/")
        print(rel_path)
        for i in range(0, len(self.chosen_eikons)):
            eikon_icon = PicButton(rel_path + self.chosen_eikons[i] + "_icon.png")
            if i <= 4:
                self.layout.addWidget(eikon_icon, 0, count)
                count += 1
            else:
                if i > 7:
                    eikon_icon.setVisible(False)
                self.layout.addWidget(eikon_icon, 1, i-count)
            eikon_icon.clicked.connect(partial(self.set_image, self.chosen_eikons[i]))

        # Button to show/unspoiler DLC Eikons
        unspoiler_button = QPushButton(text="Show DLC Spoilers", parent=self)
        unspoiler_button.setFixedSize(126, 30)
        unspoiler_button.clicked.connect(self.show_dlc_eikons)
    
        # create labels for results
        labelsGroup = QGroupBox("Feats && Abilities")
        vLabelLayout = QVBoxLayout()
        for i in range (3):
            current_set = QLabel(text="")
            vLabelLayout.addWidget(current_set, alignment=Qt.AlignmentFlag.AlignVCenter)
        labelsGroup.setLayout(vLabelLayout)
        self.layout.addWidget(labelsGroup, 2, 2, 1, 3)

        self.layout.addWidget(button, 3, 2, 3, 3, alignment=(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter))
        self.layout.addWidget(unspoiler_button, 6, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

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
        if (self.layout.count() > 0):
            checkboxes = (self.layout.itemAt(0).widget().findChildren(QCheckBox))
            for item in checkboxes:
                self.exclusion_criteria[item.accessibleName()] = (True if item.isChecked() else False)
                i += 1
                if i >= 6:
                    break
    
    def set_image(self, eikon):

        eikon_icons = [self.layout.itemAt(i).widget() for i in range(1, 1 + len(self.chosen_eikons))]
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

    def show_dlc_eikons(self):

        eikon_icons = [self.layout.itemAt(i).widget() for i in range(1, 1 + len(self.chosen_eikons))]
        eikon_icons[8].setVisible(True)
        eikon_icons[9].setVisible(True)

        return

    
    def generate_loadout(self):
        if (self.layout.count() > 0):
            if self.chosen_eikons.count("") == len(self.chosen_eikons):
                results = {"EMPTY": ["", ""], "": ["", ""], " ": ["", ""]}
            else:
                results = self.randomizer.randomize(self.exclusion_criteria.get("replacement"), self.exclusion_criteria.get("pairing"),
                                                self.exclusion_criteria.get("pair_abilities"))
            keys = list(results.keys())
            values = list(results.values())

            i = 0
            sets_labels = sample(self.layout.itemAt(11).widget().findChildren(QLabel), 3)
            for set_label in sets_labels:
                if keys[i] == "" or keys[i] == " " or keys[i] == "EMPTY":
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
            return
    
    def finalize_parameters(self):
        if self.chosen_eikons.count("") == len(self.chosen_eikons):
            pass
        else:
            self.randomizer.set_parameters(self.chosen_eikons, self.exclusion_criteria.get("exclude_ability"),
                                        self.exclusion_criteria.get("exclude_feat"), self.exclusion_criteria.get("exclude_dlc"))
        self.generate_loadout()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    randomizer = LoadoutRandomizer()
    window = MainWindow(randomizer)
    window.setWindowTitle("Final Fantasy XVI - Loadout Randomizer")
    rel_path = window.get_correct_path("./Assets/")
    window.setWindowIcon(QIcon(rel_path + "app_icon.png"))
    window.setFixedSize(673, 503)
    window.show()
    sys.exit(app.exec())