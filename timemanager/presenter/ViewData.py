from pony import orm
from timemanager.model.model import Fulfill, Items, Statuses
from .Statuses import Statuses as PresenterStatuses

class ViewData():

  def __init__(self, itemPK, itemName = None, status = None, dateTime = None, elapsedTime = None, timeout = None, comment = None) -> None:
    self.itemName = itemName
    self.itemPK = itemPK
    self.timeout = timeout
    self.status = status
    self.dateTime = dateTime
    self.elapsedTime = elapsedTime
    self.comment = comment

  @orm.db_session
  def __init__(self, item: Items = None, fulfill: Fulfill = None):
    if item is None and fulfill is None:
      raise RuntimeError('Cannot create View Data with empty initializers')
    if item is not None:
      self.itemName = item.name
      self.itemPK = item.pk
      self.timeout = item.timeout
      statusEntry = Statuses[item.status]
      self.status = statusEntry.name
      self.comment = item.comment
      self.dateTime = None
      self.elapsedTime = None
    if fulfill is not None:
      self.dateTime = fulfill.dateTime
      self.elapsedTime = fulfill.elapsedTime

  def done(self):
    return self.status == PresenterStatuses.Done
