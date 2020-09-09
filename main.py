from duplui import Ui_MainWindow
from PyQt5 import QtWidgets, QtGui, QtCore
import sys, os
from group_by_similarity import get_similar_groups
from resize_label import Label


#pyuic5 path/to/design.ui -o output/path/to/design.py


# TODO const QString message = tr("Opened \"%1\", %2x%3, Depth: %4")
#         .arg(QDir::toNativeSeparators(fileName)).arg(image.width()).arg(image.height()).arg(image.depth());
#     statusBar()->showMessage(message);

class DuplApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна

        self._augmentUI()
        self._connectSignals()
        
        
    def _augmentUI(self):
        self.img_iterator = get_similar_groups()
        self._addPhotoGroup(next(self.img_iterator))

    def _getImageArea(self, img_path):
        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidgetResizable(True)

        lbl_img = Label() 
        pixmap = QtGui.QPixmap(img_path)
        lbl_img.setPixmap(pixmap)
        lbl_img.setScaledContents(True)
        
        like_checkbox = QtWidgets.QCheckBox(text="Like")
        like_checkbox.setCheckState(True)
        like_checkbox.setTristate(False)
        lbl_path = QtWidgets.QLabel(text=img_path)
        lbl_size = QtWidgets.QLabel(text=str(round(os.path.getsize(img_path)/(1024*1024), 2))+'Mb')
        
        font = lbl_path.font()
        font.setPointSize(10)
        lbl_path.setFont(font)
        like_checkbox.setStyleSheet('''
                QCheckBox {
                    spacing: 5px;  
                    font: 20px "Segoe UI";
                }

                QCheckBox::indicator {
                        width: 30px;
                        height: 30px;
                }

                QCheckBox::indicator:unchecked {
                    image: url(./images/unlike.png);
                }

                QCheckBox::indicator:checked {
                    image: url(./images/like.png);
                }
        ''')
        self.remove_button.setStyleSheet(
            '''
            QPushButton {
                background-color: rgb(235, 73, 86);
                border-style: outset;
                border-width: 2px;
                border-radius: 10px;
                border-color: brown;
                padding: 6px;
            }
            QPushButton:pressed {
                background-color: rgb(224, 0, 0);
                border-style: inset;
            }
            '''
        )

        horiz_layout = QtWidgets.QHBoxLayout()
        horiz_layout.addWidget(like_checkbox)#, 0, QtCore.Qt.AlignLeft)
        horiz_layout.addWidget(lbl_size, 0, QtCore.Qt.AlignRight)


        vert_layout = QtWidgets.QVBoxLayout()
        vert_layout.addWidget(lbl_path, 0, QtCore.Qt.AlignLeft) #QtCore.Qt.AlignHCenter)
        vert_layout.addWidget(lbl_img)
        vert_layout.addLayout(horiz_layout)
        # vert_layout.addWidget(like_checkbox, 0, QtCore.Qt.AlignLeft) #QtCore.Qt.AlignHCenter)

        scrollArea.setLayout(vert_layout)
        lbl_img.adjustSize()
        return scrollArea

    def _connectSignals(self):
        self.remove_button.clicked.connect(self._remove_clicked)

    def _remove_clicked(self):
        self._addPhotoGroup(next(self.img_iterator))


    def _clearLayout(self, layout):
        for i in reversed(range(layout.count())): 
            layout.itemAt(i).widget().deleteLater()

    def _addPhotoGroup(self, img_group):
        self._clearLayout(self.imgspace_layout)
        for img in img_group:            
            scrollArea = self._getImageArea(img)
            self.imgspace_layout.addWidget(scrollArea)
            #TODO [] scrollArea -> connect to signals resize, resize items

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    QtWidgets.QStyleFactory
    app.setStyle(QtWidgets.QStyleFactory.create("Fusion"));
    p = app.palette()
    p.setColor(QtGui.QPalette.Window, QtGui.QColor(53,53,53));
    p.setColor(QtGui.QPalette.Button, QtGui.QColor(53,53,53));
    p.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142,45,197));
    p.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(255,255,255));
    p.setColor(QtGui.QPalette.WindowText, QtGui.QColor(255,255,255));
    app.setPalette(p);
    window = DuplApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    window.setWindowState(QtCore.Qt.WindowMaximized)
    app.exec_()  # и запускаем приложение

if __name__ == "__main__":
    main()