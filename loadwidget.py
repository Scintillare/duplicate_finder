from PyQt5 import QtCore, QtGui, QtWidgets
from worker import Worker


class LoadWidget(QtWidgets.QWidget):
  
    finished_signal = QtCore.pyqtSignal()

    def __init__(self, image_finder, *args, **kwargs):
        super(LoadWidget, self).__init__(*args, **kwargs)
        self.image_finder = image_finder
        self.threadpool = QtCore.QThreadPool()
        self.is_thread_stopped = False
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        self.verticalLayout = QtWidgets.QVBoxLayout()

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.addWidget(QtWidgets.QLabel("Root Folder:"))

        self.dir_lineEdit = QtWidgets.QLineEdit()
        self.dir_lineEdit.setEnabled(False)
        self.horizontalLayout.addWidget(self.dir_lineEdit)

        self.browse_button = QtWidgets.QPushButton(text="Browse")
        self.horizontalLayout.addWidget(self.browse_button)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.start_button = QtWidgets.QPushButton(text="Start")
        self.stop_button = QtWidgets.QPushButton(text="Stop")
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.buttonLayout.addWidget(self.start_button)
        self.buttonLayout.addWidget(self.stop_button)
        
        self.verticalLayout.addLayout(self.buttonLayout)

        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setTextVisible(False)
        self.progressBar.setVisible(False)
        self.verticalLayout.addWidget(self.progressBar)

        self.textEdit = QtWidgets.QPlainTextEdit()
        self.textEdit.setReadOnly(True)
        self.textEdit.setLineWrapMode(QtWidgets.QPlainTextEdit.WidgetWidth)
        self.textEdit.setWordWrapMode(QtGui.QTextOption.WrapAnywhere)
        self.textEdit.setVisible(False)
        self.textEdit.setFont(QtGui.QFont("Segoe UI", pointSize=9))
        self.verticalLayout.addWidget(self.textEdit)

        self.setLayout(self.verticalLayout)

    def _connect_signals(self):
        self.browse_button.clicked.connect(self._slot_browse_clicked)
        self.start_button.clicked.connect(self._slot_start_clicked)
        self.stop_button.clicked.connect(self._slot_stop_clicked)

    def _slot_browse_clicked(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, 
            "Open Directory", "C:", QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontResolveSymlinks)
        if directory:
            self.dir_lineEdit.setText(directory)
            self.start_button.setEnabled(True)

    def _slot_start_clicked(self):
        self.image_finder.BASE_DIR = self.dir_lineEdit.text()       
        self.stop_button.setEnabled(True)
        self.progressBar.setVisible(True)
        self.progressBar.setMaximum(0)  # switch to endless progress line
        self.textEdit.setVisible(True)
        self.textEdit.clear()

        worker = Worker(self._iter_add_img)
        self.is_thread_stopped = False
        self.threadpool.start(worker)

    def _iter_add_img(self):
        for img_path in self.image_finder.add_images():
            if self.is_thread_stopped:
                self.image_finder.delete_index()
                break
            QtCore.QMetaObject.invokeMethod(self.textEdit, "appendPlainText", 
                QtCore.Qt.AutoConnection, QtCore.Q_ARG(str, img_path))
        self.finished_signal.emit()

    def _slot_stop_clicked(self):
        self.is_thread_stopped = True
        self.progressBar.setMaximum(100)
        self.textEdit.clear()
        self.textEdit.appendPlainText('Index deleted')
