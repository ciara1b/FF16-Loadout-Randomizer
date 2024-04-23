from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class PicButton(QAbstractButton):

    def __init__(self, image, parent=None):
        super(PicButton, self).__init__(parent)
        
        self.image = image
        self.pixmap = QPixmap(self.image)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.selected = True

    def get_image(self):
        return self.image
    
    def set_image(self, image):
        self.image = image

    def set_pixmap(self, selected):
        self.selected = selected
        if self.selected is False:
            self.pixmap.load(self.image)
        else:
            self.pixmap.load(self.image)
        self.update()

    def get_selected(self):
        return self.selected

    def paintEvent(self, event):
        painter = QPainter(self)
        
        if self.selected is False:
            painter.setOpacity(0.5)
        else:
            painter.setOpacity(1)

        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()
