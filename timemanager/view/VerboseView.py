from PySide6.QtCore import Slot
from timemanager.view.Ui_mainWindow import Ui_MainWindow

class VerboseView:
  itemPK: int = -1
  name: str
  verboseText: str
  ui: Ui_MainWindow

  def __init__(self, ui):
    self.ui = ui

  @Slot()
  def show(self):
    currentItems = self.ui.listWidget.selectedItems()
    if len(currentItems) == 1:
      ...
    else:
      raise RuntimeError("One item must be chosen for showing verbose view!")

  @Slot()
  def hide(self):
    pass