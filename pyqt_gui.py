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
        # temp testing
        print(self.randomizer.randomize(replacement=False, pairing=False, pair_abilities=True))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # exclusion parameters included for testing
    window = Window(LoadoutRandomizer(eikons=["", "Phoenix", "Garuda", "Ramuh", "Titan", "Bahamut", "Shiva", "Odin", "Leviathan", "Ultima"], exclude_ability=False, exclude_feat=False, exclude_dlc=False))
    window.setWindowTitle("Final Fantasy XVI - Loadout Randomizer")
    window.setGeometry(100, 100, 700, 300)
    window.show()
    sys.exit(app.exec())