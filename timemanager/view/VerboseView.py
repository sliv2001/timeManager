from PySide6.QtCore import Slot
from timemanager.view.Ui_mainWindow import Ui_MainWindow
from timemanager.presenter.presenter import Presenter

class VerboseView:
  itemPK: int = -1
  name: str
  verboseText: str
  ui: Ui_MainWindow
  presenter: Presenter

  def __init__(self, ui, presenter):
    self.ui = ui
    self.presenter = presenter
    self.hide()

  @Slot()
  def show(self):
    currentItems = self.ui.listWidget.selectedItems()
    if len(currentItems) == 1:
      currentItemData = self.presenter.GetItem(currentItems[0].itemPK)
      self.ui.itemVerboseGroupBox.setTitle(currentItemData.itemName)
      self.ui.itemVerboseTextEdit.setMarkdown(currentItemData.comment)
      self.ui.itemVerboseTextView.setPlainText(self.ui.itemVerboseTextEdit.toPlainText())
      self.ui.itemVerboseGroupBox.show()

    else:
      raise RuntimeError("One item must be chosen for showing verbose view!")

  @Slot()
  def hide(self):
    self.ui.itemVerboseGroupBox.hide()
