from PySide6.QtWidgets import QListWidgetItem

class ListItem(QListWidgetItem):
  itemPK: int
  def __init__(self, item, itemPK) -> None:
    self.itemPK = itemPK
    return super().__init__(item)
