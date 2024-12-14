from PySide6.QtWidgets import QApplication
from timemanager.utils.settings import Settings
from timemanager.presenter.presenter import Presenter
from timemanager.plugins.pluginHandler import pluginHandler
from timemanager.view.MainWindow import MainWindow

class Application(QApplication):
  settings: Settings
  presenter: Presenter
  view: MainWindow
  pluginHandler: pluginHandler

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.settings = Settings('ISTech', 'TimeManager')
    self.presenter = Presenter(settings=self.settings)
    self.view = MainWindow(self.settings, presenter=self.presenter)
    self.presenter.view = self.view
    self.pluginHandler = pluginHandler(self)
    self.view.show()
