from datetime import time, datetime
from PySide6.QtCore import QTimer, Slot
from timemanager.view.Ui_mainWindow import Ui_MainWindow
from timemanager.presenter.presenter import Presenter

class Timer:
  tt: time
  updated: bool
  updateDT: datetime

  def __init__(self, time, updated):
    self.tt = time
    self.updated = updated
    self.updateDT = datetime.now()

class ViewUpdateTimers:
  _timers: list[Timer] = []
  ui: Ui_MainWindow
  presenter: Presenter

  def __init__(self, ui, presenter):
    self.ui = ui
    self.presenter = presenter
    self.presenter.layoutChanged.connect(self.setActualUpdateTime)
    self.presenter.dataChanged.connect(self.setActualUpdateTime)

  @staticmethod
  def compareTimeGt(a: time, b: time):
    return a.hour >= b.hour and a.minute >= b.minute and a.second >= b.second

  @Slot()
  def setActualUpdateTime(self, *args):
    now = datetime.now()
    for timer in self._timers:
      if self.compareTimeGt(now, timer.tt):
        timer.updated = True
        timer.updateDT = now

  @Slot()
  def timeout(self):
    now = datetime.now()
    if now.hour == 0 and now.minute == 0 and (now.second == 0 or now.second == 1):
      self.nightlyReset()
    if any(self.compareTimeGt(now, timer.tt) and not timer.updated or timer.updateDT.date() < now.date() for timer in self._timers):
      self.updateByTimer()

  def updateByTimer(self):
    # TODO config: debug log and updating messages
    print('Interface was updated')
    self.presenter._updatedCache = False
    self.presenter.layoutChanged.emit()

  def nightlyReset(self):
    for timer in self._timers:
      timer.updated = False

  def setUpdateTime(self, time: time):
    timer = QTimer(self.ui.listView)
    timer.timeout.connect(slot=self.timeout)
    timer.start(1000)
    self._timers.append(Timer(time, True))
