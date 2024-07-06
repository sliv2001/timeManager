from typing import final

class ViewData():

  Done: final = "DONE"

  def __init__(self, itemName, itemPK, status, dateTime, elapsedTime) -> None:
    self.itemName = itemName
    self.itemPK = itemPK
    self.status = status
    self.dateTime = dateTime
    self.elapsedTime = elapsedTime

  def done(self):
    return self.status == self.Done
