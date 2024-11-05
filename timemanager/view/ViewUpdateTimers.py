from datetime import time, datetime
from PySide6.QtCore import QTimer, Slot
from timemanager.view.Ui_mainWindow import Ui_MainWindow
from timemanager.presenter.presenter import Presenter

class ViewUpdateTimers:
  _timers: list[time] = []
  ui: Ui_MainWindow
  presenter: Presenter

  def __init__(self, ui, presenter):
    self.ui = ui
    self.presenter = presenter
    self.presenter.layoutChanged.connect(self.setActualUpdateTime)
    self.presenter.dataChanged.connect(self.setActualUpdateTime)
    self.updateTime = datetime.now()

  @staticmethod
  def compareTimeGt(a: time, b: time):
    return a.hour >= b.hour and a.minute >= b.minute and a.second >= b.second

  @Slot()
  def setActualUpdateTime(self, *args):
    self.updateTime = datetime.now()

  @Slot()
  def timeout(self):
    now = datetime.now()
    if any(self.compareTimeGt(now, tt) and self.compareTimeGt(tt, self.updateTime) or
           self.compareTimeGt(tt, now) and self.compareTimeGt(self.updateTime, tt) for tt in self._timers):
      # TODO config: debug log and updating messages
      print('Interface was updated')
      self.presenter.layoutChanged.emit()

  def setUpdateTime(self, time: time):
    timer = QTimer(self.ui.listView)
    timer.timeout.connect(slot=self.timeout)
    timer.start(1000)
    self._timers.append(time)
