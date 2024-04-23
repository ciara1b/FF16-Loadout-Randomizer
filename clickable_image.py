from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class PicButton(QAbstractButton):

    def __init__(self, image, parent=None):
        super(PicButton, self).__init__(parent)
        
        self.image = image
        self.pixmap = QPixmap(self.image)

    def get_image(self):
        return self.image
    def set_image(self, image):
        self.image = image

    def set_pixmap(self):
        self.pixmap = QPixmap(self.image)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()
