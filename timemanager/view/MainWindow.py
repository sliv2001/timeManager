from datetime import datetime, timedelta

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QMainWindow, QWidget, QAbstractButton, QPushButton, QDialogButtonBox, QInputDialog
from PySide6.QtGui import QColor

from timemanager.view.Ui_mainWindow import Ui_MainWindow
from timemanager.presenter.presenter import Presenter
from timemanager.presenter.ViewData import ViewData
from timemanager.view.listItem import ListItem
from timemanager.view.VerboseView import VerboseView

class MainWindow(QMainWindow):

  ui: Ui_MainWindow

  def __init__(self, parent: QWidget | None = ..., flags: Qt.WindowType = ...) -> None:
    super(MainWindow, self).__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.presenter = Presenter(self)
    self.verboseView = VerboseView(self.ui, self.presenter)
    closeButton = QPushButton(text="Закрыть", parent=self.ui.buttonBox)
    closeButton.setObjectName("closeButton")
    closeButton.clicked.connect(slot=self.closeButton_clicked)
    newItemButton = QPushButton(text="Создать", parent=self.ui.buttonBox)
    newItemButton.clicked.connect(slot=self.ui.addItem.trigger)
    self.ui.buttonBox.addButton(closeButton, QDialogButtonBox.ButtonRole.DestructiveRole)
    self.ui.buttonBox.addButton(newItemButton, QDialogButtonBox.ButtonRole.ActionRole)
    self.ui.removeItem.triggered.connect(slot=self.deleteTriggered)
    self.ui.addItem.triggered.connect(slot=self.addTriggered)
    self.ui.verboseItem.triggered.connect(slot=self.verboseView.show)
    self.ui.listWidget.itemChanged.connect(slot=self.item_checked)
    self.ui.listWidget.addAction(self.ui.removeItem)
    self.ui.listWidget.addAction(self.ui.addItem)
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
    if self.ui.listWidget.count() > 0:
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
    currentItems = self.ui.listWidget.selectedItems()
    if len(currentItems) > 0:
      self.presenter.RemoveItems([item.itemPK for item in self.ui.listWidget.selectedItems()])

  def update(self):
    self.todayData = self.presenter.getDataSinceToday()
    self.drawCheckboxes()

  def setRemovalEnabled(self, currentItems):
      self.ui.removeItem.setEnabled(len(currentItems) > 0)

  def createNewItem(self):
    newItem, res = QInputDialog.getText(self, 'Новый пункт', 'Название нового пункта: ')
    if res and len(newItem) > 0:
      self.presenter.AddItem(newItem)
