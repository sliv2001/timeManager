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

  @Slot()
  def timeout(self):
    now = datetime.now()
    if any(now.hour == tt.hour and now.minute == tt.minute and now.second == tt.second for tt in self._timers):
      self.presenter.layoutChanged.emit()

  def setUpdateTime(self, time: time):
    timer = QTimer(self.ui.listView)
    timer.timeout.connect(slot=self.timeout)
    timer.start(1000)
    self._timers.append(time)
