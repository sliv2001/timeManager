from .Statuses import Statuses

class ViewData():

  def __init__(self, itemPK, itemName = None, status = None, dateTime = None, elapsedTime = None, timeout = None, comment = None) -> None:
    self.itemName = itemName
    self.itemPK = itemPK
    self.timeout = timeout
    self.status = status
    self.dateTime = dateTime
    self.elapsedTime = elapsedTime
    self.comment = comment

  def done(self):
    return self.status == Statuses.Done
