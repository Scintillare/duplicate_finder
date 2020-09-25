'''
https://stackoverflow.com/questions/8211982/qt-resizing-a-qlabel-containing-a-qpixmap-while-keeping-its-aspect-ratio
Adapted from Timmmm to PYQT5
'''

from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QLabel
from PIL import Image


class ImageLabel(QLabel):

    # clicked = QtCore.pyqtSignal()

    def __init__(self, img_path):
        super(ImageLabel, self).__init__()

        self.img_path = img_path
        self.setPixmap(QPixmap(img_path))
        self.setScaledContents(True)
        self.pixmap_width: int = 1
        self.pixmapHeight: int = 1

    def mouseReleaseEvent(self, event):
        if self.pixmap() and self.img_path:
            img = Image.open(self.img_path)
            img.show()
        # self.clicked.emit()

    def setPixmap(self, pm: QPixmap) -> None:
        self.pixmap_width = pm.width()
        self.pixmapHeight = pm.height()

        self.updateMargins()
        super(ImageLabel, self).setPixmap(pm)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.updateMargins()
        super(ImageLabel, self).resizeEvent(a0)

    def updateMargins(self):
        if self.pixmap() is None:
            return
        pixmapWidth = self.pixmap().width()
        pixmapHeight = self.pixmap().height()
        if pixmapWidth <= 0 or pixmapHeight <= 0:
            return
        w, h = self.width(), self.height()
        if w <= 0 or h <= 0:
            return

        if w * pixmapHeight > h * pixmapWidth:
            m = int((w - (pixmapWidth * h / pixmapHeight)) / 2)
            self.setContentsMargins(m, 0, m, 0)
        else:
            m = int((h - (pixmapHeight * w / pixmapWidth)) / 2)
            self.setContentsMargins(0, m, 0, m)
