from datetime import datetime, timedelta

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QMainWindow, QWidget, QAbstractButton, QPushButton, QDialogButtonBox, QInputDialog, QMenu
from PySide6.QtGui import QColor

from timemanager.view.Ui_mainWindow import Ui_MainWindow
from timemanager.presenter.presenter import Presenter
from timemanager.view.listItem import ListItem

class MainWindow(QMainWindow):

  ui: Ui_MainWindow

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

    self.update()

  def drawCheckbox(self, item):
    line = ListItem(item.itemName, item.itemPK)
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
    self.updateItemVerbose()
    self.setRemovalEnabled()

  def updateItemVerbose(self):
    currentItems = self.ui.listWidget.selectedItems()
    if len(currentItems) == 1:
      self.setAndShowItemVerbose(currentItems)
      self.ui.textEdit
    else:
      self.hideItemVerbose()

  def hideItemVerbose(self):
      self.ui.itemVerbose.hide()

  def setAndShowItemVerbose(self, currentItems):
      self.ui.itemVerbose.setTitle(currentItems[0].text())
      self.ui.itemVerbose.show()

  def update(self):
    self.todayData = self.presenter.getDataSinceToday()
    self.drawCheckboxes()
    self.changeItemSelection()

  def setRemovalEnabled(self):
      self.ui.removeItem.setEnabled(len(self.ui.listWidget.selectedItems()) > 0)

  def createNewItem(self):
    newItem, res = QInputDialog.getText(self, 'Новый пункт', 'Название нового пункта: ')
    if res and len(newItem) > 0:
      self.presenter.AddItem(newItem)
