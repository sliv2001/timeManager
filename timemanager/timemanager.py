import sys
from PySide6.QtWidgets import QApplication
from timemanager.view.MainWindow import MainWindow

from timemanager.application import Application

def main():
    app = Application(sys.argv)
    window = MainWindow(app.settings)
    window.show()
    sys.exit(app.exec())
