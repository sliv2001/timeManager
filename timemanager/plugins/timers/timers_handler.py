from PySide6.QtCore import QTimer, Slot, QObject
from timemanager.plugins.plugin import plugin

class _InternalTimer:
  IntID: int
  remain: int
  timeout: int
  scale: int # Ticks per second; >=1, <=1000

  def __init__(self, IntID, timeout, scale = 1): # remain in seconds
    self.IntID = IntID
    self.remain = timeout * scale
    self.timeout = timeout * scale
    self.scale = scale

  def tick(self):
    self.remain -= 1 * self.scale
    if self.remain == 0:
      return True
    return False

class TimersHandler(QObject):
  _entries: list[_InternalTimer]
  _eventTimer: QTimer
  _scale: int = 10

  def __init__(self, parent = ...):
    super().__init__(parent)
    self._entries = []
    self._eventTimer = QTimer(self)
    self._eventTimer.setInterval(100)
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
    self._entries.append(_InternalTimer(IntID, timeout=timeout, scale=self._scale))

  def finishEntry(self, entry: _InternalTimer):
    self.parent().finishEntry(entry.IntID)

  def update(self):
    self.parent().updateInterface([(entry.IntID, entry.remain / entry.timeout) for entry in self._entries])

  @Slot()
  def tick(self):
    finished = [entry for entry in self._entries if entry.tick()]
    for entry in finished:
      self.finishEntry(entry)
    self._entries = [entry for entry in self._entries if entry.remain > 0]
    if not self._entries:
      self.stop()
