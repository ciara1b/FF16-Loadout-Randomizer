from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class PicButton(QAbstractButton):

    def __init__(self, image, parent=None):
        super(PicButton, self).__init__(parent)
        
        self.image = image
        self.pixmap = QPixmap(self.image)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def get_image(self):
        return self.image
    def set_image(self, image):
        self.image = image

    def set_pixmap(self, selected):
        if selected is False:
            self.pixmap.load(self.image)
        else:
            self.pixmap.load(self.image)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()
