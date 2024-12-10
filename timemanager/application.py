from PySide6.QtWidgets import QApplication
from timemanager.utils.settings import Settings
from timemanager.plugins.pluginHandler import pluginHandler

class Application(QApplication):
  def __init__(self, *args, **kwargs):
    settings = Settings('ISTech', 'TimeManager')
    self.settings = settings
    super().__init__(*args, **kwargs)
