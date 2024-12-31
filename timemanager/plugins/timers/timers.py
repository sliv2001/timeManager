from typing import Any
from PySide6.QtCore import QModelIndex, QPersistentModelIndex, Qt, QTimer, Signal
from timemanager.plugins.plugin import plugin
from timemanager.plugins.pluginHandler import modify_func

class timers(plugin):

  _timers = []
  _timer: QTimer

  def _timerAdd(self, id, timeout):
    self._timers.append((id, timeout))
    self._timer.start()

  def _1SecTick(self):
    for timer in self._timers:
      if timer[1] == 0:
        self.setStateFinished(timer[0])
        self._timers = [timer for timer in self._timers if timer[1]>0]
        if self._timers == []:
          self._timer.stop()
      else:
        timer[1] -= 1

  def setStateFinished(self, id):
    pass

  def requiresModelUpdate(self) -> bool:
    return False

  def modelUpdate(self, enable: bool):
    pass

  def appUpdate(self):
    self._timer = QTimer(self)
    self._timer.timeout.connect(slot=self._1SecTick)
    self._timer.setInterval(1000)
    self.app.presenter.dataUpdated = Signal(None, name = 'dataUpdated')
    self.app.presenter.dataUpdated.connect(self.)

  def handleCheckClick(self):
    raise NotImplementedError('Need to implement')

# ///////////////////////////////////////////////////// New Presenter Features //////////////////////////////////////////////////// #

  @modify_func('setData')
  def setData(self, index: QModelIndex | QPersistentModelIndex, value: Any, role: int = ...):
    if (role == Qt.ItemDataRole.CheckStateRole) and (value == Qt.CheckState.Checked.value):

      self._timerAdd(index.internalId(), self._getCache()[index.row()].timeout)

  @modify_func('data')
  def data(self, index: QModelIndex | QPersistentModelIndex, role: int = ...):
    return None
