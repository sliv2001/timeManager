from datetime import datetime, date, timedelta
from typing import Any
from pony import orm
from PySide6.QtCore import QAbstractItemModel, QModelIndex, QPersistentModelIndex, Qt
from PySide6.QtGui import QColor
from timemanager.model.model import Fulfill, Items, Statuses
from .ViewData import ViewData
from .Statuses import ModelStatuses, ViewStatuses, ModelFulfillments, AllModelNames
from .PriorityHandler import PriorityHandler

class Presenter(QAbstractItemModel):

  _cache: list
  _updatedCache: bool = False

  def __init__(self, view) -> None:
    super().__init__(view)
    self.initDatabase()
    self.view = view
    self.priorityHandler = PriorityHandler()

# ////////////////////////////////////////////////////// Model-side functions ///////////////////////////////////////////////////// #

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
  def _removeItems(self, items):
    self.beginRemoveRows(QModelIndex(), items[0].itemIndex, items[-1].itemIndex)
    self._updatedCache = False
    for item in items:
      self._updateItem(item)
    self.endRemoveRows()

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
    self._updatedCache = False
    if item.itemPK is None:
      raise RuntimeError('Expected non-None item to update!')
    itemEntry = Items[item.itemPK]
    if item.comment is not None:
      itemEntry.comment = item.comment
    if item.itemName is not None:
      itemEntry.name = item.itemName
    if item.status is not None:
      self._updateStatus(item, itemEntry)
    if item.timeout is not None:
      itemEntry.timeout = item.timeout

  @orm.db_session
  def _updateStatus(self, item, itemEntry):
    if item.status == ViewStatuses.Done:
      fulfillLine = ModelFulfillments.Done
      self._addFulfill(item.itemPK, fulfillLine, item.elapsedTime, item.dateTime)
    elif item.status == ViewStatuses.Undone:
      fulfillLine = self._getPreviousFulfillmentStatus(item.itemPK)
      self._addFulfill(item.itemPK, fulfillLine, item.elapsedTime, item.dateTime)
    elif item.status == ViewStatuses.Pending:
      raise RuntimeError('Currently Pending is not supported')
    else:
      statusName = ViewStatuses.toModel(item.status)
      if statusName == ModelStatuses.Removed:
        self.beginRemoveRows(QModelIndex(), item.itemIndex, item.itemIndex)
        statusEntry = Statuses.get(name=statusName)
        itemEntry.status = statusEntry
        self.endRemoveRows()
        self._updatedCache = False
      else:
        statusEntry = Statuses.get(name=statusName)
        itemEntry.status = statusEntry

  @orm.db_session
  def _updateItems(self, items: list[ViewData]):
    for item in items:
      self._updateItem(item)

# ////////////////////////////////////////////////////// View-side functions ////////////////////////////////////////////////////// #

  def _updateView(self, topLeft = None, bottomRight = None, rolesList = None):
    self._updatedCache = False
    if topLeft is None:
      topLeft = self.createIndex(0, 0, self._getCache()[0].itemPK)
    if bottomRight is None:
      lastIndex = self.rowCount()-1
      bottomRight = QAbstractItemModel.createIndex(lastIndex, 0, self._getCache()[lastIndex].itemPK)
    self.dataChanged.emit(topLeft, bottomRight, rolesList)

  def AddItem(self, item: ViewData, prevItemPK = None):
    self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount()+1)
    pk = self._addItem(item.itemName, item.status, prevItemPK=prevItemPK)
    self._updatedCache = False
    self.endInsertRows()
    return pk

  def RemoveItem(self, item: ViewData):
    self._removeItems([item])
    # self._updateView()

  def RemoveItems(self, items: list[ViewData]):
    self._removeItems(items)
    # self._updateView()

  def SetItemDone(self, itemPK: int, status: bool, elapsedTime, dateTime: datetime):
    self._setItemDone(itemPK, status, elapsedTime, dateTime)

  @orm.db_session
  def _setItemDone(self, itemPK, status, elapsedTime, dateTime):
    if status:
      statusLine = ModelFulfillments.Done
    else:
      statusLine = self._getPreviousFulfillmentStatus(itemPK)
    self._addFulfill(itemPK, statusLine, elapsedTime, dateTime)
    # self._updateView()

  def GetItem(self, itemPK):
    return self._getItem(itemPK)

  def SetItemAfter(self, itemPK, afterItemPK):
    result = self.priorityHandler.SetAfter(itemPK, afterItemPK)
    # self._updateView()
    return result

  def UpdateItem(self, item: ViewData):
    self._updateItem(item)
    # self._updateView()

  def UpdateItems(self, items: list[ViewData]):
    self._updateItems(items)

  def _getCache(self):
    if not self._updatedCache:
      self._cache = self.getDataSinceToday()
      self._updatedCache = True
    return self._cache

# ///////////////////////////////////////////////// Redefinition of model members ///////////////////////////////////////////////// #

  def rowCount(self, parent=None):
    return len(self._getCache())

  def columnCount(self, parent=None):
    return 1 # List -> columnCount is constant 1

  def parent(self, index):
    return QModelIndex()

  def index(self, row, column, parent = None):
    if (column > 1):
      return QModelIndex()
    return self.createIndex(row, column, self._getCache()[row].itemPK)

  def data(self, index: QModelIndex | QPersistentModelIndex, role: int = ...) -> Any:
    # See this for roles description:
    # https://doc.qt.io/qt-6/qt.html#ItemDataRole-enum
    if role == Qt.ItemDataRole.DisplayRole:
      return self._getCache()[index.row()].itemName
    elif role == Qt.ItemDataRole.BackgroundRole:
      if self._getCache()[index.row()].status == ViewStatuses.Outdated:
        return QColor("Red")
      else:
        return None
    elif role == Qt.ItemDataRole.CheckStateRole:
      if self._getCache()[index.row()].status == ViewStatuses.Done:
        return Qt.CheckState.Checked
      else:
        return Qt.CheckState.Unchecked
    else:
      return None

  def flags(self, index: QModelIndex | QPersistentModelIndex) -> Qt.ItemFlag:
    # See this for item flags description:
    # https://doc.qt.io/qt-6/qt.html#ItemFlag-enum
    return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemNeverHasChildren

  def setData(self, index: QModelIndex | QPersistentModelIndex, value: Any, role: int = ...) -> bool:
    if role == Qt.ItemDataRole.CheckStateRole and value != Qt.CheckState.PartiallyChecked.value:
      self.SetItemDone(index.internalId(), value == Qt.CheckState.Checked.value, 60*15, datetime.now())
      self._updatedCache = False
      self.dataChanged.emit(index, index, [role])
      return True
    return False
