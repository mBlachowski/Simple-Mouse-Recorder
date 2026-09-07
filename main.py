import sys

from gui import MainWindow
from PySide6.QtWidgets import QApplication


if __name__ == '__main__':
   app = QApplication(sys.argv)
   window = MainWindow(app)
   app.exec()

