from typing import final

class Statuses:

  class Fulfillments:
    # The action was fulfilled at required time period
    Done: final = "DONE"

    # The action was not (yet) fulfilled at required time period
    Undone: final = "UNDONE"

  # The action is active (fulfilled at required time period or not)
  Active: final = "ACTIVE"

  # The action is finished successfully and should not be shown as active
  Done: final = "DONE"

  # The action was not fullfilled at required time and shown as outdated
  Outdated: final = "OUTDATED"

  # The action is in progress
  Pending: final = "PENDING"

  # The action was cancelled and is shown among active
  Rejected: final = "REJECTED"

  # The action was cancelled and is NOT shown among active
  Removed: final = "REMOVED"

  def AllModelStatuses():
    return ['ACTIVE', 'DONE', 'OUTDATED', 'PENDING', 'REJECTED', 'REMOVED']

  def AllModelFulfillments():
    return ['DONE', 'UNDONE']

  def AllViewStatuses():
    return ['DONE', 'UNDONE', 'OUTDATED', 'PENDING', 'REJECTED', 'REMOVED']