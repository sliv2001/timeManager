from PySide6.QtCore import Slot, QModelIndex
from PySide6.QtWidgets import QDialogButtonBox, QGroupBox
from timemanager.presenter.presenter import Presenter
from timemanager.presenter.ViewData import ViewData

class CustomGroupBox(QGroupBox):
  itemPK: int = -1
  name: str = ""
  verboseText: str = ""
  presenter: Presenter

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def setUp(self, ui, presenter):
    self.ui = ui
    self.presenter = presenter
    self.ui.itemVerboseButtonBox.button(QDialogButtonBox.StandardButton.Close).setText("Скрыть")
    self.ui.itemVerboseButtonBox.button(QDialogButtonBox.StandardButton.Close).clicked.connect(self.hide)
    self.ui.itemVerboseButtonBox.button(QDialogButtonBox.StandardButton.Save).clicked.connect(self.saveAndHide)
    self.ui.itemVerboseButtonBox.button(QDialogButtonBox.StandardButton.Save).setText("Сохранить")
    self.ui.tabWidget.currentChanged.connect(slot=self.switchTextFormat)
    self.hide()

  def isValid(self):
    return self.itemPK >= 0

  @Slot()
  def show(self):
    if self.isVisible():
      self.save()
    currentItems = self.ui.listView.selectedIndexes()
    if len(currentItems) == 1:
      currentItem = currentItems[0]
      self.updateInterface(currentItem)
    else:
      raise RuntimeError("One item must be chosen for showing verbose view!")
    super().show()

  def updateInterface(self, currentItem: QModelIndex):
      currentItemData = self.presenter.GetItem(currentItem.internalId())
      self.itemPK = currentItem.internalId()
      self.name = currentItemData.itemName
      self.verboseText = currentItemData.comment
      self._drawInterface()

  def _drawInterface(self):
    self.setTitle(self.name)
    self.ui.itemVerboseTextEdit.setPlainText(self.verboseText)
    self.ui.itemVerboseTextView.setMarkdown(self.ui.itemVerboseTextEdit.toPlainText())

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
    if self.isValid():
      self.presenter.UpdateItem(ViewData(self.itemPK, comment=self.verboseText))

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
