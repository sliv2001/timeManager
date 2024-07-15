from PySide6.QtWidgets import QListWidgetItem

class ListItem(QListWidgetItem):
  itemPK: int
  comment: str
  def __init__(self, item, itemPK, comment = "") -> None:
    self.itemPK = itemPK
    self.comment = comment
    return super().__init__(item)
