from PySide6.QtWidgets import QListWidgetItem

class ListItem(QListWidgetItem):
  index: int
  def __init__(self, item, index) -> None:
    self.index = index
    return super().__init__(item)
