from pony import orm
from timemanager.model.model import Fulfill, Items, Statuses
from .Statuses import ViewStatuses

class ViewData():

  def __init__(self, itemPK, itemName = None, status = None, dateTime = None, elapsedTime = None, timeout = None, comment = None, priority = None) -> None:
    self.itemName = itemName
    self.itemPK = itemPK
    self.timeout = timeout
    self.status = status
    self.dateTime = dateTime
    self.elapsedTime = elapsedTime
    self.comment = comment
    self.priority = priority

  @classmethod
  @orm.db_session
  def fromModel(cls, item: Items = None, fulfill: Fulfill = None):
    if item is None and fulfill is None:
      raise RuntimeError('Cannot create View Data with empty initializers')
    if item is not None:
      itemName = item.name
      itemPK = item.pk
      timeout = item.timeout
      status = item.status.name
      comment = item.comment
      dateTime = None
      elapsedTime = None
      priority = item.priority
    if fulfill is not None:
      dateTime = fulfill.dateTime
      elapsedTime = fulfill.elapsedTime
    return cls(itemPK, itemName, status, dateTime, elapsedTime, timeout, comment, priority)

  def done(self):
    return self.status == ViewStatuses.Done

  def outdated(self):
    return self.status == ViewStatuses.Outdated
