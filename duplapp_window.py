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
        self._createElements()
        self._styleElements()

        self.image_finder = ImageFinder()
        if self.image_finder.is_index_created():
            self.setCentralWidget(Compare_Widget(self.image_finder))
        else:
            self.setCentralWidget(Load_Widget(self.image_finder))
            self.centralWidget().connect(self.change_scene)
        # self.setCentralWidget(Load_Widget(self.image_finder))

        # self.Choice = namedtuple('Choice', ['path', 'checkbox'])
        # self.choices = []

        # self._augment_UI()
        # self._connect_signals()

    def _createElements(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Duplicate Finder")

    def _styleElements(self, MainWindow):
        # font = QtGui.QFont("Segoe UI", pointSize=12)
        # font.setFamily("Segoe UI")
        # font.setPointSize(12)
        MainWindow.setFont(QtGui.QFont("Segoe UI", pointSize=12))
        # self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setStyle(QtWidgets.QStyleFactory.create("Fusion"))
        p = self.palette()
        p.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
        p.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
        p.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142, 45, 197))
        p.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(86, 20, 77))
        p.setColor(QtGui.QPalette.WindowText, QtGui.QColor(255, 255, 255))
        MainWindow.setPalette(p)  # TODO or self.setPallete?
        # MainWindow.resize(676, 464)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        # MainWindow.setSizePolicy(sizePolicy)

    @QtCore.pyqtSlot()
    def change_scene(self):
        self.setCentralWidget(Compare_Widget(self.image_finder))

    def closeEvent(self, event):
        if isinstance(self.centralWidget(), Load_Widget):
            self.centralWidget().stop_button.click()
