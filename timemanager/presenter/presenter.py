from datetime import datetime, date
from pony import orm
from timemanager.model.model import Fulfill, Items, Statuses
from .ViewData import ViewData
from .Statuses import Statuses as PresenterStatuses

class Presenter:
  def __init__(self, view) -> None:
    self.initDatabase()
    self.view = view

  def initDatabase(self):
    self.initStatuses()

  def initStatuses(self):
    try:
      with orm.db_session:
        for statusLine in PresenterStatuses.AllStatuses():
          status = Statuses(name=statusLine)
    except orm.TransactionIntegrityError as e:
      pass

  @orm.db_session
  def _addFulfill(self, item, statusLine, elapsedTime, dateTime = datetime.now()):
    itemEntry = Items[item]
    statusEntry = Statuses.get(name=statusLine)
    fulfill = Fulfill(dateTime=dateTime, item=itemEntry, status=statusEntry, elapsedTime=elapsedTime)

  @orm.db_session
  def _addItem(self, itemName, statusLine):
    statusEntry = Statuses.get(name=statusLine)
    itemEntry = Items(name=itemName, status=statusEntry)
    return itemEntry.pk

  @orm.db_session
  def _removeItems(self, itemPKs):
    statusEntry = Statuses.get(name=PresenterStatuses.Removed)
    for itemPK in itemPKs:
      Items[itemPK].status = statusEntry

  def _updateView(self):
    self.view.update()

  def AddItem(self, itemName, statusLine = PresenterStatuses.Active):
    pk = self._addItem(itemName, statusLine)
    self._updateView()
    return pk

  @orm.db_session
  def getDataSince(self, dateTime):
    # Select all the fulfillments, which have following properties:
    #   - Its parent item is active
    #   - It either has maximum time among fulfillments of current item,
    #     or has never been mentioned
    # These requests are then sorted by pk and chosen only those with todays fulfillment date
    allData = orm.left_join((item, ff) for item in Items for ff in item.fulfil
                            if item.status.name == PresenterStatuses.Active and
                              ((ff.dateTime == max(ff.dateTime for ff in item.fulfil)) or ff is None)).order_by(1)
    allDataLocal = []
    for item in allData[:]:
      if item[1] is None:
        allDataLocal.append(ViewData(item[0].pk, item[0].name, PresenterStatuses.Pending, dateTime, 0, item[0].timeout, item[0].comment))
      elif item[1].dateTime < dateTime:
        allDataLocal.append(ViewData(item[0].pk, item[0].name, PresenterStatuses.Pending, item[1].dateTime, 0, item[0].timeout, item[0].comment))
      else:
        allDataLocal.append(ViewData(item[0].pk, item[0].name, item[1].status.name, item[1].dateTime, item[1].elapsedTime, item[0].timeout, item[0].comment))
    return allDataLocal

  @orm.db_session
  def getDataSinceToday(self):
    today_night = datetime.combine(date.today(), datetime.min.time())
    return self.getDataSince(today_night)

  @orm.db_session
  def _updateComment(self, itemPK, comment):
    item = Items[itemPK]
    item.comment = comment

  def RemoveItem(self, itemPK):
    self._removeItems([itemPK])
    self._updateView()

  def RemoveItems(self, itemPKs):
    self._removeItems(itemPKs)
    self._updateView()

  def SetStatus(self, itemPK, statusLine, elapsedTime = 15*60, dateTime = datetime.now()):
    self._addFulfill(itemPK, statusLine, elapsedTime, dateTime)
    self._updateView()

  def UpdateComment(self, itemPK, comment):
    self._updateComment(itemPK, comment)
    self._updateView()
