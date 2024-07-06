from datetime import datetime, date
from pony import orm
from timemanager.model.model import Fulfill, Items
from .ViewData import ViewData

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
    allData = orm.left_join((item, ff) for item in Items for ff in item.fulfil if (ff.dateTime == max(ff.dateTime for ff in item.fulfil if ff.dateTime >= today_night)) or ff is None)
    # allData = allData.filter(lambda item, ff: ff.dateTime >= today_night or ff is None)
    allData.show()
    print(allData.get_sql())
    allDataLocal = []
    for item in allData[:]:
      if item[1] is None:
        allDataLocal.append(ViewData(item[0].name, item[0].pk, 'PENDING', today_night, 0))
      else:
        allDataLocal.append(ViewData(item[0].name, item[0].pk, item[1].status, item[1].dateTime, item[1].elapsedTime))
    return allDataLocal

  def RemoveItem(self, item):
    self._removeItem(item)
    self._updateView()

  def SetStatus(self, itemPK, status, elapsedTime = 15*60, dateTime = datetime.now()):
    self._addFulfill(itemPK, status, elapsedTime, dateTime)
    self._updateView()
