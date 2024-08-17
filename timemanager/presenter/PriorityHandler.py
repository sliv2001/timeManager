from pony import orm
from timemanager.model.model import Fulfill, Items, Statuses

class PriorityHandler:
  priorityStep: int

  def __init__(self) -> None:
    self.priorityStep = 10000

  @orm.db_session
  def _getLowestPriority(self) -> int:
    leastPriority = orm.max(item.priority for item in Items)
    return leastPriority if not leastPriority is None else 0

  @orm.db_session
  def _calculateItemPriority(self, prevItem) -> int:
    # Important: 0 is highest priority
    if not prevItem is None:
      beforePriority = self._getItemPriority(prevItem)
      afterPriority  = self._getMostPriorityAfter(beforePriority)
      if beforePriority == None: # This is first item
        if afterPriority == None: # This is the only item
          priority = 0
        else:
          priority = afterPriority // 2
      else:
        if afterPriority == None: # This is last item
          priority = beforePriority + self.priorityStep
        else:
          priority = (beforePriority + afterPriority) // 2
    else:
      priority = self._getLowestPriority() + self.priorityStep
    return priority

  @orm.db_session
  def _getItemPriority(self, itemPK: int) -> int:
    return Items[itemPK].priority

  @orm.db_session
  def _getMostPriorityAfter(self, priority: int) -> int:
    afterPriority = orm.min(item.priority for item in Items if item.priority > priority)
    return afterPriority

  @orm.db_session
  def _updatePriority(self, itemPK, afterItemPK):
    itemEntry = Items[itemPK]
    itemEntry.priority = self._calculateItemPriority(prevItem=afterItemPK)

  def GetNewItemPriority(self, prevItem):
    return self._calculateItemPriority(prevItem)

  def SetAfter(self, itemPK, afterItemPK):
    self._updatePriority(itemPK, afterItemPK)
