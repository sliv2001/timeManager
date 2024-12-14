from timemanager.presenter.presenter import Presenter
from timemanager.view.MainWindow import MainWindow

class plugin:

  def __init__(self, app) -> None:
    self.app = app

  def requiresModelUpdate(self) -> bool:
    raise NotImplementedError('requiresModelUpdate must be implemented inside the plugin')

  def modelUpdate(self, enable: bool):
    raise NotImplementedError('modelUpdate must be implemented inside the plugin')

  def appUpdate(self):
    raise NotImplementedError('appUpdate must be implemented inside the plugin')
