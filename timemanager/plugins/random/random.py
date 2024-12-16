from random import randint
from PySide6.QtCore import Slot, QItemSelectionModel
from PySide6.QtWidgets import QPushButton, QDialogButtonBox
from PySide6.QtGui import QAction

from timemanager.application import Application
from timemanager.view.MainWindow import MainWindow
from timemanager.plugins.plugin import plugin

class random(plugin):

  app: Application

  def requiresModelUpdate(self) -> bool:
    return False

  def modelUpdate(self, enable: bool):
    pass

  @Slot()
  def chooseRandomTriggered(self):
    rand = randint(0, self.app.presenter.rowCount()-1)
    self.app.view.ui.listView.selectionModel().select(self.app.presenter.index(rand, 0), QItemSelectionModel.SelectionFlag.ClearAndSelect)

  def appUpdate(self):

    # Action
    self.chooseRandom = QAction(self)
    self.chooseRandom.setObjectName(u"chooseRandom")
    self.chooseRandom.setMenuRole(QAction.MenuRole.ApplicationSpecificRole)
    self.chooseRandom.setText(u'\u0421\u043b\u0443\u0447\u0430\u0439\u043d\u044b\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442')
    self.chooseRandom.setToolTip(u'\u041f\u0440\u0435\u0434\u043b\u043e\u0436\u0438\u0442\u044c \u0441\u043b\u0443\u0447\u0430\u0439\u043d\u044b\u0439 \u044d\u043b\u0435\u043c\u0435\u043d\u0442')
    self.chooseRandom.setShortcut('Ctrl+R')
    self.chooseRandom.triggered.connect(slot=self.chooseRandomTriggered)

    self.randomButton = QPushButton(text="Случайный", parent=self.app.view.ui.buttonBox)
    self.randomButton.setObjectName("randomButton")
    self.randomButton.clicked.connect(slot=self.chooseRandom.trigger)
    self.app.view.ui.buttonBox.addButton(self.randomButton, QDialogButtonBox.ButtonRole.ActionRole)

