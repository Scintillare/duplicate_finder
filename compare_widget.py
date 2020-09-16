from PyQt5 import QtCore, QtGui, QtWidgets
from resize_label import Label


class Compare_Widget(QtWidgets.QWidget):

    def __init__(self, img_finder, *args, **kwargs):
        super(Compare_Widget, self).__init__(*args, **kwargs)
        self.img_finder = img_finder
        self.compare_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.compare_layout)
        self.setupUI()

        self._augment_UI()
        self._connect_signals()

    def setupUI(self):
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.imgspace_widget = QtWidgets.QWidget()
        self.imgspace_widget.setObjectName("imgspace_widget")
        self.imgspace_layout = QtWidgets.QHBoxLayout(self.imgspace_widget)
        self.imgspace_layout.setObjectName("imgspace_layout")
        self.verticalLayout.addWidget(self.imgspace_widget)
        self.remove_button = QtWidgets.QPushButton()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.remove_button.sizePolicy().hasHeightForWidth())
        self.remove_button.setSizePolicy(sizePolicy)
        self.remove_button.setMinimumSize(QtCore.QSize(1, 1))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.remove_button.setFont(font)
        self.remove_button.setAutoFillBackground(False)
        self.remove_button.setCheckable(False)
        self.remove_button.setChecked(False)
        self.remove_button.setDefault(False)
        self.remove_button.setFlat(True)
        self.remove_button.setObjectName("remove_button")
        self.verticalLayout.addWidget(
            self.remove_button, 0, QtCore.Qt.AlignHCenter)

        # self.retranslateUi(Compare_Form)
        # QtCore.QMetaObject.connectSlotsByName(Form)

    # def retranslateUi(self):
    #     _translate = QtCore.QCoreApplication.translate
    #     self.remove_button.setText(_translate("MainWindow", "Remove"))

    def _augment_UI(self):
        self._add_photo_group(next(self.img_iterator))

    def _get_image_area(self, img_path):
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
        lbl_size = QtWidgets.QLabel(
            text=str(round(os.path.getsize(img_path)/(1024*1024), 2))+'Mb')

        self.choices.append(self.Choice(img_path, like_checkbox))

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
                width: 150px;
                height: 70px;
                background-color: rgb(235, 73, 86);
                border-style: outset;
                border-width: 2px;
                border-radius: 10px;
                border-color: brown;
            }
            QPushButton:pressed {
                background-color: rgb(224, 0, 0);
                border-style: inset;
            }
            '''
        )

        horiz_layout = QtWidgets.QHBoxLayout()
        horiz_layout.addWidget(like_checkbox)  # , 0, QtCore.Qt.AlignHCenter)
        horiz_layout.addWidget(lbl_size, 0, QtCore.Qt.AlignRight)

        vert_layout = QtWidgets.QVBoxLayout()
        vert_layout.addWidget(lbl_path, 0, QtCore.Qt.AlignLeft)
        vert_layout.addWidget(lbl_img)
        vert_layout.addLayout(horiz_layout)

        scrollArea.setLayout(vert_layout)
        lbl_img.adjustSize()
        return scrollArea

    def _connect_signals(self):
        self.remove_button.clicked.connect(self._slot_remove_clicked)

    def _slot_remove_clicked(self):
        for path, checkbox in self.choices:
            if not checkbox.isChecked():
                print(path)  # FIXME remove image
        self.choices = []
        self._add_photo_group(next(self.img_iterator))

    def _clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()

    def _add_photo_group(self, img_group):
        self._clear_layout(self.imgspace_layout)
        for img in img_group:
            scrollArea = self._get_image_area(img)
            self.imgspace_layout.addWidget(scrollArea)
