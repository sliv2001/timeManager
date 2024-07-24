from PySide6.QtCore import Slot
from PySide6.QtWidgets import QDialogButtonBox
from timemanager.view.Ui_mainWindow import Ui_MainWindow
from timemanager.presenter.presenter import Presenter
from timemanager.presenter.ViewData import ViewData

class VerboseView:
  itemPK: int = -1
  name: str = ""
  verboseText: str = ""
  ui: Ui_MainWindow
  presenter: Presenter

  def __init__(self, ui, presenter):
    self.ui = ui
    self.presenter = presenter
    self.ui.itemVerboseButtonBox.button(QDialogButtonBox.StandardButton.Apply).setText("Применить")
    self.ui.itemVerboseButtonBox.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self.saveAndHide)
    self.ui.itemVerboseButtonBox.button(QDialogButtonBox.StandardButton.Close).setText("Скрыть")
    self.ui.itemVerboseButtonBox.button(QDialogButtonBox.StandardButton.Close).clicked.connect(self.hide)
    self.ui.tabWidget.currentChanged.connect(slot=self.switchTextFormat)
    self.hide()

  @Slot()
  def show(self):
    currentItems = self.ui.listWidget.selectedItems()
    if len(currentItems) == 1:
      currentItem = self.ui.listWidget.selectedItems()[0]
      self.updateInterface(currentItem)

    else:
      raise RuntimeError("One item must be chosen for showing verbose view!")

  def updateInterface(self, currentItem):
      currentItemData = self.presenter.GetItem(currentItem.itemPK)
      self.itemPK = currentItem.itemPK
      self.name = currentItemData.itemName
      self.verboseText = currentItemData.comment
      self._drawInterface()

  def _drawInterface(self):
      self.ui.itemVerboseGroupBox.setTitle(self.name)
      self.ui.itemVerboseTextEdit.setPlainText(self.verboseText)
      self.ui.itemVerboseTextView.setMarkdown(self.ui.itemVerboseTextEdit.toPlainText())
      self.ui.itemVerboseGroupBox.show()

  @Slot()
  def saveAndHide(self):
    self.hide()
    self.save()

  @Slot()
  def save(self):
    if (self.ui.tabWidget.currentIndex() == 0):
      self.verboseText = self.ui.itemVerboseTextEdit.toPlainText()
    elif (self.ui.tabWidget.currentIndex() == 1):
      self.verboseText = self.ui.itemVerboseTextView.toMarkdown()
    else:
      raise RuntimeError('Unexpected index of tab in TabWidget!')
    self.presenter.UpdateItem(ViewData(self.itemPK, comment=self.verboseText))

  @Slot()
  def hide(self):
    self.ui.itemVerboseGroupBox.hide()

  @Slot()
  def switchTextFormat(self, newTab: int):
    if newTab == 0:
      # Switch to MD:
      self.ui.itemVerboseTextEdit.setPlainText(self.ui.itemVerboseTextView.toMarkdown())
    elif newTab == 1:
      # Switch to formatted text
      self.ui.itemVerboseTextView.setMarkdown(self.ui.itemVerboseTextEdit.toPlainText())
    else:
      raise RuntimeError('New tab was chosen incorrectly!')
