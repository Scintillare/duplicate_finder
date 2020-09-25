from PyQt5 import QtCore, QtGui, QtWidgets
from resize_label import ImageLabel
import os
import shutil
from collections import namedtuple



class Compare_Widget(QtWidgets.QWidget):

    Choice = namedtuple('Choice', ['record', 'checkbox'])

    def __init__(self, img_finder, *args, **kwargs):
        super(Compare_Widget, self).__init__(*args, **kwargs)
        self.TRASH_DIR = './tmp_trash'
        if not os.path.exists(self.TRASH_DIR):
            os.mkdir(self.TRASH_DIR)

        self.image_finder = img_finder
        self.img_iterator = img_finder.get_similar_groups()
        self.choices = []

        self._create_elements()
        self._style_elements()
        self._connect_signals()

    def _create_elements(self):
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.imgspace_widget = QtWidgets.QWidget()
        self.imgspace_layout = QtWidgets.QGridLayout(self.imgspace_widget)
        self.remove_button = QtWidgets.QPushButton("Remove")
        self.verticalLayout.addWidget(self.imgspace_widget)
        self.verticalLayout.addWidget(self.remove_button, 0, QtCore.Qt.AlignHCenter)

        self._add_photo_group(next(self.img_iterator))

        self.setLayout(self.verticalLayout)

    def _style_elements(self):
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.remove_button.sizePolicy().hasHeightForWidth())
        self.remove_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont("Segoe UI", pointSize=12, weight=75)
        font.setBold(True)
        self.remove_button.setFont(font)
        self.remove_button.setFlat(True)
        self.remove_button.setStyleSheet(
            '''
            QPushButton {
                width: 150px;
                height: 70px;
                background-color: rgb(235, 73, 86);
                color: white;
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

    def _get_image_area(self, img_record):
        img_path, img_score = img_record['path'], img_record['score']

        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidgetResizable(True)

        te_path = QtWidgets.QPlainTextEdit(img_path)
        te_path.setReadOnly(True)
        te_path.setLineWrapMode(QtWidgets.QPlainTextEdit.WidgetWidth)
        te_path.setWordWrapMode(QtGui.QTextOption.WrapAnywhere)

        lbl_img = ImageLabel(img_path)

        like_checkbox = QtWidgets.QCheckBox(text="Like")
        like_checkbox.setCheckState(True)
        like_checkbox.setTristate(False)
        lbl_score = QtWidgets.QLabel(text=f'Score: {img_score}')
        lbl_size = QtWidgets.QLabel(
            text=str(round(os.path.getsize(img_path)/(1024*1024), 2))+'Mb')

        self.choices.append(self.Choice(img_record, like_checkbox))

        bottom_line_hlayout = QtWidgets.QHBoxLayout()
        bottom_line_hlayout.addWidget(like_checkbox)
        bottom_line_hlayout.addWidget(lbl_score, 0, QtCore.Qt.AlignHCenter)
        bottom_line_hlayout.addWidget(lbl_size, 0, QtCore.Qt.AlignRight)

        vert_layout = QtWidgets.QVBoxLayout()
        vert_layout.addWidget(te_path)  # , 0, QtCore.Qt.AlignLeft)
        vert_layout.addWidget(lbl_img)
        vert_layout.addLayout(bottom_line_hlayout)

        scrollArea.setLayout(vert_layout)
        te_path.adjustSize()
        lbl_img.adjustSize()

        te_path.setStyleSheet('''
                color: rgb(255, 255, 255);
                background-color: rgb(53, 53, 53);
                selection-color: rgb(235, 73, 86);
                selection-background-color: rgb(255, 255, 255);
                border: none;
                font: 10pt "Segoe UI";
                ''')

        like_checkbox.setStyleSheet('''
                QCheckBox {
                    spacing: 5px;
                    font: 15pt "Segoe UI";
                    color: white;
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

        return scrollArea

    def _connect_signals(self):
        self.remove_button.clicked.connect(self._slot_remove_clicked)

    @QtCore.pyqtSlot()
    def _slot_remove_clicked(self):
        for record, checkbox in self.choices:
            if not checkbox.isChecked():
                self._gently_remove(record)
        self.choices = []
        self._add_photo_group(next(self.img_iterator))


    def _gently_remove(self, doc_record):
        try:
            shutil.move(doc_record['path'], self.TRASH_DIR)
            self.image_finder.delete_doc(doc_record['id'])
        except Exception as e:
            with open('err_log.txt', mode='a', encoding='utf-8') as log:
                log.write('shutil.move on compare_widget fail\n')
                log.write(str(e))
                return
                
        # img_path = "%r" % doc_record['path']
        # try:
            # os.remove(img_path)
            # os.remove(doc_record['path'])
            # self.image_finder.delete_doc(doc_record['id'])
        # except Exception as e:
        #     with open('err_log.txt', mode='a', encoding='utf-8') as log:
        #         log.write('os.remove on compare_widget fail\n')
        #         log.write(str(e))
        #     fn = os.path.basename(doc_record['path'])
        #     old_path = doc_record['path'].replace(fn, '')
        #     trash = os.path.abspath(os.path.join(self.TRASH_DIR, fn))
        #     shutil.move(trash, old_path)
            # FIXME show message for user
        
        # TODO send2trash lib?

    def _clear_layout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().deleteLater()

    def _add_photo_group(self, img_group):
        self._clear_layout(self.imgspace_layout)
        ncols = 3
        for i, record in enumerate(img_group):
            if not os.path.exists(record['path']):
                if len(img_group) == 2:
                    self.remove_button.click()
                    break
                continue
            if len(img_group) % 4 == 0:
                ncols = 2
            elif len(img_group) % 3 == 0:
                ncols = 3
            row = i // ncols
            col = i % ncols
            scrollArea = self._get_image_area(record)
            self.imgspace_layout.addWidget(scrollArea, row, col)
