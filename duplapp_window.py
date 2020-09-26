from PyQt5 import QtCore, QtGui, QtWidgets
from imagefinder import ImageFinder
from load_widget import Load_Widget
from compare_widget import Compare_Widget

import os
from collections import namedtuple

# TODO const QString message = tr("Opened \"%1\", %2x%3, Depth: %4")
#         .arg(QDir::toNativeSeparators(fileName)).arg(image.width()).arg(image.height()).arg(image.depth());
#     statusBar()->showMessage(message);

class DuplApp(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self._setup_ui()

        self.image_finder = ImageFinder()
        self.compare_scene = Compare_Widget(self.image_finder)
        self.load_scene = Load_Widget(self.image_finder)

        self.load_scene.finished_signal.connect(self.to_compare_scene)
        self.compare_scene.restarted_signal.connect(self.to_load_scene)

        if self.image_finder.is_index_created():
            self.to_compare_scene()
        else:
            self.to_load_scene()

    def _setup_ui(self):
        self.setObjectName("MainWindow")
        self.setWindowTitle("Duplicate Finder")
        self.setFont(QtGui.QFont("Segoe UI", pointSize=12))
        self.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
        p = self.palette()
        p.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
        p.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
        p.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142, 45, 197))
        p.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(86, 20, 77))
        p.setColor(QtGui.QPalette.WindowText, QtGui.QColor(255, 255, 255))
        self.setPalette(p)

        # MainWindow.resize(676, 464)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        # MainWindow.setSizePolicy(sizePolicy)

    @QtCore.pyqtSlot()
    def to_compare_scene(self):
        self.setCentralWidget(self.compare_scene)
        self.setWindowState(QtCore.Qt.WindowMaximized)

    @QtCore.pyqtSlot()
    def to_load_scene(self):
        self.setCentralWidget(self.load_scene)
        self.setWindowState(QtCore.Qt.WindowMinimized)

    def closeEvent(self, event):
        if isinstance(self.centralWidget(), Load_Widget):
            self.centralWidget().stop_button.click()
