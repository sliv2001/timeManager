from typing import Any
from datetime import datetime
from PySide6.QtCore import QModelIndex, QPersistentModelIndex, Qt, QTimer, Signal, Slot
from timemanager.plugins.plugin import plugin
from timemanager.plugins.pluginHandler import modify_func
from timemanager.plugins.timers.timers_handler import TimersHandler
from timemanager.presenter.Statuses import ViewStatuses
from timemanager.presenter.ViewData import ViewData

class timers(plugin):

  def requiresModelUpdate(self) -> bool:
    return False

  def modelUpdate(self, enable: bool):
    pass

  def appUpdate(self):
    self.timers_handler = TimersHandler(self)
    self.app.presenter.dataChanged.connect(slot=self.dataChanged)
    self.timers_handler.timerFinished.connect(slot=self.timerFinished)

# //////////////////////////////////////////////////////// Signals Handling /////////////////////////////////////////////////////// #

  @Slot()
  def dataChanged(self, begin: QModelIndex, end: QModelIndex, roles: list[int]):
    if Qt.ItemDataRole.CheckStateRole in roles:
      for row in range(begin.row(), end.row()+1): # Because if (1, 1), we need to process it
        intID = self.app.presenter.index(row, 0).internalId()
        done = self.app.presenter._getCache()[row].status == ViewStatuses.Done
        if not done:
          continue
        timeout = 900
        self.startTheTimer(row, timeout)

  @Slot()
  def timerFinished(self, intID: int):
    index = self.app.presenter.createIndex(intID, 0)
    self.app.presenter._updateItem(ViewData(index.internalId(),
                                            status=ViewStatuses.Done,
                                            dateTime=datetime.now(),
                                            elapsedTime=15*60))
    self.app.presenter.dataChanged.emit(index, index, [Qt.ItemDataRole.CheckStateRole])
    print('finished entry', intID)

# ///////////////////////////////////////////////////////////// Timers //////////////////////////////////////////////////////////// #

  def startTheTimer(self, row: int, timeout: int):
    self.timers_handler.createEntry(row, timeout)

# ///////////////////////////////////////////////////// New Presenter Features //////////////////////////////////////////////////// #

  # @modify_func('setData')
  # def setData(self, index: QModelIndex | QPersistentModelIndex, value: Any, role: int = ...):
  #   if role == Qt.ItemDataRole.CheckStateRole and value == Qt.CheckState.Checked.value:
  #     self.dataChanged.emit(index, index, [role])
  #     return False
  #   return None

  # @modify_func('data')
  # def data(self, index: QModelIndex | QPersistentModelIndex, role: int = ...):
  #   return None
