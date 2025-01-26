from PySide6.QtCore import QObject
from timemanager.presenter.presenter import Presenter
from timemanager.view.MainWindow import MainWindow
from timemanager.application import Application

class plugin(QObject):

  def __init__(self, app: Application) -> None:
    super().__init__(app)
    self.app = app

  def requiresModelUpdate(self) -> bool:
    raise NotImplementedError('requiresModelUpdate must be implemented inside the plugin')

  def modelUpdate(self, enable: bool):
    raise NotImplementedError('modelUpdate must be implemented inside the plugin')

  def appUpdate(self):
    raise NotImplementedError('appUpdate must be implemented inside the plugin')
