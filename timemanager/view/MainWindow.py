from datetime import datetime, timedelta

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QMainWindow, QWidget, QAbstractButton, QPushButton, QDialogButtonBox, QInputDialog, QMenu
from PySide6.QtGui import QColor

from timemanager.view.Ui_mainWindow import Ui_MainWindow
from timemanager.presenter.presenter import Presenter
from timemanager.presenter.ViewData import ViewData
from timemanager.view.listItem import ListItem

class MainWindow(QMainWindow):

  ui: Ui_MainWindow

  previousItemPK: int = -1

  def __init__(self, parent: QWidget | None = ..., flags: Qt.WindowType = ...) -> None:
    super(MainWindow, self).__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.presenter = Presenter(self)
    closeButton = QPushButton(text="Закрыть", parent=self.ui.buttonBox)
    closeButton.setObjectName("closeButton")
    closeButton.clicked.connect(slot=self.closeButton_clicked)
    newItemButton = QPushButton(text="Создать", parent=self.ui.buttonBox)
    newItemButton.clicked.connect(slot=self.ui.addItem.trigger)
    self.ui.buttonBox.addButton(closeButton, QDialogButtonBox.ButtonRole.DestructiveRole)
    self.ui.buttonBox.addButton(newItemButton, QDialogButtonBox.ButtonRole.ActionRole)
    self.ui.removeItem.triggered.connect(slot=self.deleteTriggered)
    self.ui.addItem.triggered.connect(slot=self.addTriggered)
    self.ui.listWidget.itemChanged.connect(slot=self.item_checked)
    self.ui.listWidget.addAction(self.ui.removeItem)
    self.ui.listWidget.addAction(self.ui.addItem)
    self.ui.listWidget.itemSelectionChanged.connect(self.changeItemSelection)
    newItemButton.setObjectName("newItemButton")

    self.ui.tabWidget.currentChanged.connect(self.textViewChanged)

    self.update()

  def drawCheckbox(self, item):
    line = ListItem(item.itemName, item.itemPK, item.comment)
    line.setFlags(line.flags() | Qt.ItemFlag.ItemIsUserCheckable)
    line.setCheckState(Qt.CheckState.Checked if item.done() else Qt.CheckState.Unchecked)
    if item.dateTime.date() < (datetime.now()-timedelta(seconds=item.timeout)).date():
      line.setBackground(QColor("Red"))
    self.ui.listWidget.addItem(line)

  def drawCheckboxes(self):
    self.ui.listWidget.clear()
    for item in self.todayData:
      self.drawCheckbox(item)

  @Slot()
  def closeButton_clicked(self, button: QAbstractButton):
    self.saveSession()
    exit()

  @Slot()
  def addTriggered(self, button: QAbstractButton):
    self.createNewItem()

  @Slot()
  def item_checked(self, item: ListItem):
    if item.checkState():
      self.presenter.SetStatus(itemPK=item.itemPK, statusLine='DONE', elapsedTime=15*60, dateTime=datetime.now())

  @Slot()
  def deleteTriggered(self):
    self.presenter.RemoveItems([item.itemPK for item in self.ui.listWidget.selectedItems()])

  @Slot()
  def changeItemSelection(self):
    currentItems = self.ui.listWidget.selectedItems()
    self.saveCurrentDetails()
    self.drawItemDetails(currentItems)
    self.previousItemPK = -1 if len(currentItems) != 1 else currentItems[0].itemPK

  def drawItemDetails(self, currentItems):
      self.updateItemVerbose(currentItems)
      self.setRemovalEnabled(currentItems)

  @Slot()
  def textViewChanged(self, index):
    # If index is 0, we switched to MD from text, as MD is 0-th widget
    self.updateTextFormatting(index == 0)

  def updateItemVerbose(self, currentItems):
    if len(currentItems) == 1:
      self.setAndShowItemVerbose(currentItems)
    else:
      self.hideItemVerbose()


  def updateTextFormatting(self, toMD):
    if toMD:
      self.ui.itemVerboseTextEdit.setPlainText(self.ui.itemVerboseTextView.toMarkdown())
    else:
      self.ui.itemVerboseTextView.setMarkdown(self.ui.itemVerboseTextEdit.toPlainText())


  def hideItemVerbose(self):
      self.ui.itemVerbose.hide()

  def setAndShowItemVerbose(self, currentItems):
      self.ui.itemVerbose.setTitle(currentItems[0].text())
      self.ui.itemVerboseTextEdit.setPlainText(currentItems[0].comment)
      self.ui.itemVerboseTextView.setMarkdown(currentItems[0].comment)
      self.ui.itemVerbose.show()

  def update(self):
    self.todayData = self.presenter.getDataSinceToday()
    self.drawCheckboxes()
    currentItems = self.ui.listWidget.selectedItems()
    self.drawItemDetails(currentItems)

  def setRemovalEnabled(self, currentItems):
      self.ui.removeItem.setEnabled(len(currentItems) > 0)

  def createNewItem(self):
    newItem, res = QInputDialog.getText(self, 'Новый пункт', 'Название нового пункта: ')
    if res and len(newItem) > 0:
      self.presenter.AddItem(newItem)

  def saveSession(self):
    self.saveCurrentDetails()

  def saveCurrentDetails(self):
    if self.previousItemPK >= 0:
      self.presenter.UpdateComment(self.previousItemPK, self.ui.itemVerboseTextEdit.toPlainText())
