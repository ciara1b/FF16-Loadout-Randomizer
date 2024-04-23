from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class PicButton(QAbstractButton):

    def __init__(self, image, parent=None):
        super(PicButton, self).__init__(parent)
        
        self.pixmap = QPixmap(image)
        self.clicked.connect(self.test)

    def test(self):
        if self.underMouse():
            print("test")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()
