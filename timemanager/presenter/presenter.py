from datetime import datetime, date, timedelta
from pony import orm
from timemanager.model.model import Fulfill, Items, Statuses
from .ViewData import ViewData
from .Statuses import ModelStatuses, ViewStatuses, ModelFulfillments, AllModelNames
from .PriorityHandler import PriorityHandler

class Presenter:

  def __init__(self, view) -> None:
    self.initDatabase()
    self.view = view
    self.priorityHandler = PriorityHandler()

  def initDatabase(self):
    self.initStatuses()

  def initStatuses(self):
    try:
      with orm.db_session:
        for statusLine in AllModelNames():
          status = Statuses(name=statusLine)
    except orm.TransactionIntegrityError as e:
      pass

  @orm.db_session
  def _addFulfill(self, item, statusLine, elapsedTime, dateTime):
    itemEntry = Items[item]
    statusEntry = Statuses.get(name=statusLine)
    fulfill = Fulfill(dateTime=dateTime, item=itemEntry, status=statusEntry, elapsedTime=elapsedTime)

  @orm.db_session
  def _addItem(self, itemName, statusLine, prevItemPK):
    statusLine = statusLine if not statusLine is None else ModelStatuses.Active
    priority = self.priorityHandler.GetNewItemPriority(prevItem=prevItemPK)
    statusEntry = Statuses.get(name=statusLine)
    itemEntry = Items(name=itemName, status=statusEntry, priority=priority)
    return itemEntry.pk

  @orm.db_session
  def _removeItems(self, itemPKs):
    for itemPK in itemPKs:
      self._updateItem(ViewData(itemPK, status=ModelStatuses.Removed))

  def _updateView(self):
    self.view.update()

  def AddItem(self, item: ViewData, prevItemPK = None):
    pk = self._addItem(item.itemName, item.status, prevItemPK=prevItemPK)
    self._updateView()
    return pk

  @orm.db_session
  def getDataSince(self, dateTime):
    # Select all the fulfillments, which have following properties:
    #   - Its parent item is active
    #   - It either has maximum time among fulfillments of current item,
    #     or has never been mentioned
    # These requests are then sorted by pk and chosen only those with todays fulfillment date
    allData = orm.left_join((item.pk, item.name, item.timeout, ff.pk, ff.dateTime, ff.status, item.priority)
                            for item in Items for ff in item.fulfil
                            if item.status.name == ModelStatuses.Active and
                              ((ff.dateTime == max(ff.dateTime for ff in item.fulfil)) or ff is None)).order_by(7)

    allDataLocal = []
    currentDateTime = datetime.now()
    for itemPK, itemName, itemTimeout, ffPk, ffDateTime, ffStatus, itemPriority in allData[:]:
      if ffPk is None:
        allDataLocal.append(ViewData(itemPK, itemName, ViewStatuses.Undone))
      else:
        itemDt = ffDateTime
        if itemDt < dateTime:
          if ffDateTime.date() < (currentDateTime-timedelta(seconds=itemTimeout)).date():
            allDataLocal.append(ViewData(itemPK, itemName, ViewStatuses.Outdated))
          else:
            allDataLocal.append(ViewData(itemPK, itemName, ViewStatuses.Undone))
        else:
          allDataLocal.append(ViewData(itemPK, itemName, ffStatus.name))
    return allDataLocal

  @orm.db_session
  def _getPreviousFulfillmentStatus(self, itemPK):
    todayNight = datetime.combine(date.today(), datetime.min.time())
    data = orm.select(ff for ff in Items[itemPK].fulfil if ff.dateTime >= todayNight).order_by(Fulfill.dateTime)
    if len(data) < 2:
      return ViewStatuses.Undone
    else:
      return data[:][1].status.name

  @orm.db_session
  def getDataSinceToday(self):
    today_night = datetime.combine(date.today(), datetime.min.time())
    return self.getDataSince(today_night)

  @orm.db_session
  def _getItem(self, itemPK):
    return ViewData.fromModel(item=Items[itemPK])

  @orm.db_session
  def _updateItem(self, item: ViewData):
    if item.itemPK is None:
      raise RuntimeError('Expected non-None item to update!')
    itemEntry = Items[item.itemPK]
    if item.comment is not None:
      itemEntry.comment = item.comment
    if item.itemName is not None:
      itemEntry.name = item.itemName
    if item.status is not None:
      statusEntry = Statuses.get(name=item.status)
      itemEntry.status = statusEntry
    if item.timeout is not None:
      itemEntry.timeout = item.timeout

  def RemoveItem(self, itemPK):
    self._removeItems([itemPK])
    self._updateView()

  def RemoveItems(self, itemPKs):
    self._removeItems(itemPKs)
    self._updateView()

  def SetItemDone(self, itemPK: int, status: bool, elapsedTime, dateTime: datetime):
    self._setItemDone(itemPK, status, elapsedTime, dateTime)

  @orm.db_session
  def _setItemDone(self, itemPK, status, elapsedTime, dateTime):
    if status:
      statusLine = ModelFulfillments.Done
    else:
      statusLine = self._getPreviousFulfillmentStatus(itemPK)
    self._addFulfill(itemPK, statusLine, elapsedTime, dateTime)
    self._updateView()

  def GetItem(self, itemPK):
    return self._getItem(itemPK)

  def SetItemAfter(self, itemPK, afterItemPK):
    result = self.priorityHandler.SetAfter(itemPK, afterItemPK)
    self._updateView()
    return result

  def UpdateItem(self, item: ViewData):
    self._updateItem(item)
    self._updateView()
