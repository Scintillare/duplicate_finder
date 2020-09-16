import sys
from PyQt5.QtWidgets import QApplication
from duplapp_window import DuplApp

# XXX pyuic5 path/to/design.ui -o output/path/to/design.py

def main():
    app = QApplication(sys.argv)
    window = DuplApp()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
