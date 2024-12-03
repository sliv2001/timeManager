from PySide6.QtCore import Slot, QSettings

class Setting:

  def __init__(self, name, getter, setter) -> None:
    self.name = name
    self.getter = getter
    self.setter = setter

class Settings(QSettings):

  settings: list[Setting]

  def __init__(self, organization, app_name):
    super().__init__(organization, app_name)
    self.settings = []

  def addSetting(self, name, getter, setter):
    self.settings.append(Setting(name, getter, setter))

  @Slot()
  def applySettings(self):
    for setting in self.settings:
      val = self.value(setting.name)
      (setting.setter)(val if not val is None else (setting.getter)())

  @Slot()
  def saveSettings(self):
    for setting in self.settings:
      val = (setting.getter)()
      self.setValue(setting.name, val)
