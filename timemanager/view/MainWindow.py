from datetime import datetime, timedelta, time
from random import randint

from PySide6.QtCore import Qt, Signal, Slot, QModelIndex, QItemSelectionModel
from PySide6.QtWidgets import QMainWindow, QWidget, QAbstractButton, QPushButton, QDialogButtonBox, QInputDialog
from PySide6.QtGui import QCloseEvent

from timemanager.view.Ui_mainWindow import Ui_MainWindow
from timemanager.presenter.presenter import Presenter
from timemanager.presenter.ViewData import ViewData
from timemanager.view.CustomGroupBox import CustomGroupBox
from timemanager.presenter.Statuses import ViewStatuses
from timemanager.view.ViewUpdateTimers import ViewUpdateTimers
from timemanager.utils.settings import Settings
from timemanager.plugins.pluginHandler import pluginHandler

class MainWindow(QMainWindow):

  ui: Ui_MainWindow
  windowInitialized = Signal(None, name = 'windowInitialized')
  windowClosed = Signal(None, name = 'windowClosed')

  def __init__(self, settings: Settings, presenter: Presenter, parent: QWidget | None = ..., flags: Qt.WindowType = ...) -> None:
    super(MainWindow, self).__init__()
    self.settings = settings
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.presenter = presenter
    self.ui.listView.setModel(self.presenter)
    self.ui.verboseView.setUp(self.ui, self.presenter)

    self.timers = ViewUpdateTimers(self.ui, self.presenter)
    self.timers.setUpdateTime(time(hour=0, minute=0, second=0))

    closeButton = QPushButton(text="Закрыть", parent=self.ui.buttonBox)
    closeButton.setObjectName("closeButton")
    closeButton.clicked.connect(slot=self.closeButton_clicked)
    randomButton = QPushButton(text="Случайный", parent=self.ui.buttonBox)
    randomButton.setObjectName("randomButton")
    randomButton.clicked.connect(slot=self.ui.chooseRandom.trigger)
    newItemButton = QPushButton(text="Создать", parent=self.ui.buttonBox)
    newItemButton.clicked.connect(slot=self.ui.addItem.trigger)
    newItemButton.setObjectName("newItemButton")
    upButton = QPushButton(text="Поднять", parent=self.ui.buttonBox)
    upButton.clicked.connect(slot=self.ui.upItem.trigger)
    upButton.setObjectName("upButton")
    downButton = QPushButton(text="Опустить", parent=self.ui.buttonBox)
    downButton.clicked.connect(slot=self.ui.downItem.trigger)
    downButton.setObjectName("upButton")
    self.ui.buttonBox.addButton(closeButton, QDialogButtonBox.ButtonRole.DestructiveRole)
    self.ui.buttonBox.addButton(newItemButton, QDialogButtonBox.ButtonRole.ActionRole)
    self.ui.buttonBox.addButton(randomButton, QDialogButtonBox.ButtonRole.ActionRole)
    self.ui.buttonBox.addButton(upButton, QDialogButtonBox.ButtonRole.ActionRole)
    self.ui.buttonBox.addButton(downButton, QDialogButtonBox.ButtonRole.ActionRole)

    self.ui.chooseRandom.triggered.connect(slot=self.chooseRandomTriggered)
    self.ui.removeItem.triggered.connect(slot=self.deleteTriggered)
    self.ui.addItem.triggered.connect(slot=self.addTriggered)
    self.ui.verboseItem.triggered.connect(slot=self.ui.verboseView.show)
    self.ui.checkItem.triggered.connect(slot=self.checkTriggered)
    self.ui.upItem.triggered.connect(slot=self.upItemTriggered)
    self.ui.downItem.triggered.connect(slot=self.downItemTriggered)
    self.ui.listView.selectionModel().selectionChanged.connect(slot=self.itemSelectionChanged)
    self.ui.listView.addAction(self.ui.addItem)
    self.ui.listView.addAction(self.ui.removeItem)
    self.ui.listView.addAction(self.ui.verboseItem)
    self.ui.listView.addAction(self.ui.checkItem)
    self.ui.listView.addAction(self.ui.upItem)
    self.ui.listView.addAction(self.ui.downItem)
    self.ui.listView.addAction(self.ui.chooseRandom)

    self.enableItemEditActions()

    self.windowInitialized.connect(self.settings.applySettings)
    self.windowClosed.connect(self.windowClosing)
    self.windowClosed.connect(self.settings.saveSettings)
    self.settings.addSetting('view/mainWindow/geometry', self.normalGeometry, self.setGeometry)
    self.settings.addSetting('view/mainWindow/verbose_view/geometry', self.ui.splitter.sizes, self.ui.splitter.setSizes)
    self.settings.addSetting('view/mainWindow/fullscreen', self.isFullScreen, self.setFullScreen)
    self.windowInitialized.emit()

####### Events redefinition

  def closeEvent(self, event: QCloseEvent) -> None:
    self.windowClosed.emit()
    return super().closeEvent(event)

####### Events handling slots

  @Slot()
  def closeButton_clicked(self, button: QAbstractButton):
    self.close()

  @Slot()
  def addTriggered(self, button: QAbstractButton):
    self.createNewItem()

  @Slot()
  def itemSelectionChanged(self):
    self.enableItemEditActions()

  @Slot()
  def chooseRandomTriggered(self):
    rand = randint(0, self.presenter.rowCount()-1)
    self.ui.listView.selectionModel().select(self.presenter.index(rand, 0), QItemSelectionModel.SelectionFlag.ClearAndSelect)

  @Slot()
  def deleteTriggered(self):
    currentItems = self.ui.listView.selectedIndexes()
    if len(currentItems) > 0:
      self.presenter.RemoveItems([ViewData(itemPK=itemIndex.internalId(), itemIndex=itemIndex.row(), status=ViewStatuses.Removed) for itemIndex in currentItems])
    else:
      raise RuntimeError('Delete triggered for empty range of objects!')

  @Slot()
  def checkTriggered(self, checked):
    currentItems = self.ui.listView.selectedIndexes()
    if len(currentItems) == 1:
      self.presenter.UpdateItem(ViewData(currentItems[0].internalId(),
                                         status=ViewStatuses.Done if checked else ViewStatuses.Undone,
                                         dateTime=datetime.now(),
                                         elapsedTime=15*60), row=currentItems[0].row())

  @Slot()
  def upItemTriggered(self):
    self.makePriorityStep(-1)

  @Slot()
  def downItemTriggered(self):
    self.makePriorityStep(1)

  @Slot()
  def windowClosing(self):
    self.saveBeforeExit()

  ####### UI Updating facilities

  def setFullScreen(self, full: bool):
    if full:
      self.showFullScreen()
    else:
      self.showNormal()

  def enableItemEditActions(self):
    currentItems = self.ui.listView.selectedIndexes()
    lenCI = len(currentItems)
    enable = lenCI > 0
    self.ui.removeItem.setEnabled(enable)
    self.ui.verboseItem.setEnabled(enable)
    self.ui.upItem.setEnabled(lenCI == 1)
    self.ui.downItem.setEnabled(lenCI == 1)
    self.ui.checkItem.setEnabled(lenCI == 1)
    self.ui.verboseItem.setEnabled(lenCI == 1)
    self.ui.checkItem.setChecked(lenCI == 1 and currentItems[0].data(role=Qt.ItemDataRole.CheckStateRole) == Qt.CheckState.Checked)
    self.ui.buttonBox.buttons()[3].setEnabled(lenCI == 1)
    self.ui.buttonBox.buttons()[4].setEnabled(lenCI == 1)

  def createNewItem(self):
    newItemName, res = QInputDialog.getText(self, 'Новый пункт', 'Название нового пункта: ')
    if res and len(newItemName) > 0:
      self.presenter.AddItem(ViewData(itemPK=None, itemName=newItemName))

####### Auxillary functions

  def makePriorityStep(self, step):
    currentItems = self.ui.listView.selectedIndexes()
    currentItem = currentItems[0]

    if len(currentItems) != 1:
      raise RuntimeError('Priority change triggered for wrong range of objects!')

    currentIndex = currentItem.row()

    if currentIndex + step < 0 or currentIndex + step > self.presenter.rowCount():
      raise RuntimeError('Priority change triggered for top priority object!')

    # If we move to the top, we must put current item after one before previous,
    # Otherwise, after one after following
    newIndex = currentIndex + step - 1 if step < 0 else currentIndex + step
    modelIndex = self.presenter.index(newIndex, 0, QModelIndex())
    self.presenter.SetItemAfter(currentItem, modelIndex)

  def saveBeforeExit(self):
    self.ui.verboseView.save()
