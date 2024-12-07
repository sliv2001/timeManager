from timemanager.presenter.presenter import Presenter
from timemanager.view.MainWindow import MainWindow

class Plugin:
  def __init__(self, view: MainWindow, presenter: Presenter) -> None:
    pass

  def requiresModelUpdate(self) -> bool:
    raise NotImplementedError('requiresModelUpdate must be implemented inside the plugin')

  def modelUpdate(self, enable: bool):
    raise NotImplementedError('modelUpdate must be implemented inside the plugin')

  def presenterUpdate(self, presenter: Presenter = None):
    raise NotImplementedError('presenterUpdate must be implemented inside the plugin')

  def viewUpdate(self, view: MainWindow = None):
    raise NotImplementedError('viewUpdate must be implemented inside the plugin')
