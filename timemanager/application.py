from PySide6.QtWidgets import QApplication

class Application(QApplication):
  def __init__(self, settings, *args, **kwargs):
    self.settings = settings
    super().__init__(*args, **kwargs)
