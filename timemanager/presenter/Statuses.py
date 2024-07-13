from typing import final

class Statuses:
  Active: final = "ACTIVE"
  Done: final = "DONE"
  Outdated: final = "OUTDATED"
  Pending: final = "PENDING"
  Rejected: final = "REJECTED"
  Removed: final = "REMOVED"

  def AllStatuses():
    return ['ACTIVE', 'DONE', 'OUTDATED', 'PENDING', 'REJECTED', "REMOVED"]
