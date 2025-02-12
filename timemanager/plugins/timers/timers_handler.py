from datetime import datetime, timedelta
from PySide6.QtCore import QTimer, Slot, Signal, QObject
from timemanager.plugins.plugin import plugin

class _InternalTimer:
  IntID: int
  endTime: datetime
  outdated: bool

  def __init__(self, IntID, timeout): # remain in seconds
    self.IntID = IntID
    self.endTime = datetime.now()+timedelta(seconds=timeout)
    self.timeout = timeout
    self.outdated = False

  def tick(self):
    if self.endTime <= datetime.now():
      self.outdated = True
      return True
    return False

class TimersHandler(QObject):
  _entries: list[_InternalTimer]
  _eventTimer: QTimer
  _scale: int = 1
  timerFinished = Signal(int, name='timerFinished', arguments=['intID'])

  def __init__(self, parent = ...):
    super().__init__(parent)
    self._entries = []
    self._eventTimer = QTimer(self)
    self._eventTimer.setInterval(1000 // self._scale)
    self._eventTimer.timeout.connect(self.tick)
    self.stop()

  def start(self):
    if not self._eventTimer.isActive():
      self._eventTimer.start()

  def stop(self):
    if self._eventTimer.isActive():
      self._eventTimer.stop()

  def createEntry(self, IntID, timeout):
    self.start()
    self._entries.append(_InternalTimer(IntID, timeout=timeout))

  def finishEntry(self, entry: _InternalTimer):
    self.timerFinished.emit(entry.IntID)

  @Slot()
  def tick(self):
    finished = [entry for entry in self._entries if entry.tick()]
    for entry in finished:
      self.finishEntry(entry)
    self._entries = [entry for entry in self._entries if not entry.outdated]
    if not self._entries:
      self.stop()
