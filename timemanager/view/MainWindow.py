from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QMainWindow, QWidget, QAbstractButton

from timemanager.view.Ui_mainWindow import Ui_MainWindow
from timemanager.presenter.presenter import Presenter
from timemanager.view.listItem import ListItem

class MainWindow(QMainWindow):

  ui: QMainWindow

  def __init__(self, parent: QWidget | None = ..., flags: Qt.WindowType = ...) -> None:
    super(MainWindow, self).__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.presenter = Presenter(self)
    self.update()

  def drawCheckbox(self, item):
    line = ListItem(item.name, item.pk)
    line.setFlags(line.flags() | Qt.ItemFlag.ItemIsUserCheckable)
    line.setCheckState(Qt.CheckState.Unchecked)
    self.ui.listWidget.addItem(line)

  def drawCheckboxes(self):
    for item in self.data:
      self.drawCheckbox(item)

  @Slot()
  def on_buttonBox_clicked(button: QAbstractButton):
    exit()

  def update(self):
    self.data = self.presenter.getData()
    self.drawCheckboxes()
