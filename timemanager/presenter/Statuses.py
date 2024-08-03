from typing import final

class ModelFulfillments:
  # The action was fulfilled at required time period
  Done: final = "DONE"

  # The action was not (yet) fulfilled at required time period
  Undone: final = "UNDONE"

  # The action is in progress
  Pending: final = "PENDING"

  def AllFulfillments():
    return {'DONE', 'UNDONE', 'PENDING'}

class ModelStatuses:
  # The action is active (fulfilled at required time period or not)
  Active: final = "ACTIVE"

  # The action is finished successfully and should not be shown as active
  Done: final = "DONE"

  # The action was cancelled and is shown among active
  Rejected: final = "REJECTED"

  # The action was cancelled and is NOT shown among active
  Removed: final = "REMOVED"

  def AllStatuses():
    return {'ACTIVE', 'DONE', 'REJECTED', 'REMOVED'}

class ViewStatuses:
  # The action was fulfilled at required time period
  Done: final = "DONE"

  # The action was not (yet) fulfilled at required time period
  Undone: final = "UNDONE"

  # The action is in progress
  Pending: final = "PENDING"

  # The action was not fullfilled at required time and shown as outdated
  Outdated: final = "OUTDATED"

  # The action was cancelled and is shown among active
  Rejected: final = "REJECTED"

  # The action was cancelled and is NOT shown among active
  Removed: final = "REMOVED"

  def AllViewStatuses():
    return {'DONE', 'UNDONE', 'PENDING', 'OUTDATED', 'REJECTED', 'REMOVED'}

def AllModelNames():
  return ModelFulfillments.AllFulfillments() | ModelStatuses.AllStatuses()