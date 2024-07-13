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
    self.ui.buttonBox.addButton(closeButton, QDialogButtonBox.ButtonRole.DestructiveRole)
    newItemButton = QPushButton(text="Создать", parent=self.ui.buttonBox)
    newItemButton.setObjectName("newItemButton")
    newItemButton.clicked.connect(slot=self.newItemButton_clicked)
    self.ui.buttonBox.addButton(newItemButton, QDialogButtonBox.ButtonRole.ActionRole)
    self.ui.listWidget.itemChanged.connect(slot=self.item_checked)
    self.ui.removeItem.triggered.connect(slot=self.deleteTriggered)
    self.ui.listWidget.addAction(self.ui.removeItem)

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
  def newItemButton_clicked(self, button: QAbstractButton):
    self.createNewItem()

  @Slot()
  def item_checked(self, item: ListItem):
    if item.checkState():
      self.presenter.SetStatus(itemPK=item.itemPK, statusLine='DONE', elapsedTime=15*60, dateTime=datetime.now())

  @Slot()
  def deleteTriggered(self):
    self.presenter.RemoveItem(self.ui.listWidget.currentItem().itemPK)

  def update(self):
    self.todayData = self.presenter.getDataSinceToday()
    self.drawCheckboxes()

  def createNewItem(self):
    newItem, res = QInputDialog.getText(self, 'Новый пункт', 'Название нового пункта: ')
    if res and len(newItem) > 0:
      self.presenter.AddItem(newItem)
