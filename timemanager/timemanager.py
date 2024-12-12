import sys
from PySide6.QtWidgets import QApplication

from timemanager.application import Application

def main():
    app = Application(sys.argv)
    sys.exit(app.exec())
