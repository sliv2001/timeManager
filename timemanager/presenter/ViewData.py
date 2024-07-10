from .Statuses import Statuses

class ViewData():

  def __init__(self, itemName, itemPK, status, dateTime, elapsedTime, timeout = 24*3600) -> None:
    self.itemName = itemName
    self.itemPK = itemPK
    self.timeout = timeout
    self.status = status
    self.dateTime = dateTime
    self.elapsedTime = elapsedTime

  def done(self):
    return self.status == Statuses.Done
