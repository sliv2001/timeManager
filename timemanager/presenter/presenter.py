from datetime import datetime, date
from pony import orm
from timemanager.model.model import Fulfill, Items

class Presenter:
  def __init__(self, view) -> None:
    self.view = view

  @orm.db_session
  def _addFulfill(self, item, status, elapsedTime, dateTime = datetime.now()):
    itemEntry = Items[item]
    fulfill = Fulfill(dateTime=dateTime, item=itemEntry, status=status, elapsedTime=elapsedTime)

  @orm.db_session
  def _addItem(self, itemName):
    itemEntry = Items(name=itemName)
    return itemEntry.pk

  @orm.db_session
  def _removeItem(self, item):
    Items[item].delete()

  def _updateView(self):
    self.view.update()

  def AddItem(self, itemName):
    pk = self._addItem(itemName)
    self._updateView()
    return pk

  @orm.db_session
  def getData(self):
    today_night = datetime.combine(date.today(), datetime.min.time())
    existingData = orm.select(ff for ff in Fulfill if ff.dateTime >= today_night and ff.dateTime == max(ff.dateTime for ff in Fulfill if ff.dateTime >= today_night))
    allData = orm.left_join((item, ff) for item in Items for ff in existingData)
    return allData[:]

  def RemoveItem(self, item):
    self._removeItem(item)
    self._updateView()

  def SetStatus(self, item, status, elapsedTime = 15*60, dateTime = datetime.now()):
    self._addFulfill(item, status, elapsedTime, dateTime)
    self._updateView()
