from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QListView

class CustomListView(QListView):

  def _checkAllSelected(self):
    model = self.model()
    indexes = self.selectedIndexes()
    setCheckState = Qt.CheckState.Unchecked
    for index in indexes:
      if model.data(index, Qt.ItemDataRole.CheckStateRole) == Qt.CheckState.Unchecked:
        setCheckState = Qt.CheckState.Checked
        break
    for index in indexes:
      model.setData(index, setCheckState.value, Qt.ItemDataRole.CheckStateRole)

  def keyPressEvent(self, event: QKeyEvent):
    if event.key() == Qt.Key.Key_Space:
      self._checkAllSelected()
    else:
      super().keyPressEvent(event)
