import sys
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication
from timemanager.view.MainWindow import MainWindow

from timemanager.application import Application

def main():
    settings = QSettings('ISTech', 'TimeManager')
    app = Application(settings, sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
