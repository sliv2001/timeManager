import sys
from PySide6.QtWidgets import QApplication
from timemanager.view.MainWindow import MainWindow
from timemanager.utils.settings import Settings

from timemanager.application import Application

def main():
    settings = Settings('ISTech', 'TimeManager')
    app = Application(settings, sys.argv)
    window = MainWindow(app.settings)
    window.show()
    sys.exit(app.exec())
