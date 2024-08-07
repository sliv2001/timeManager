from datetime import datetime

from pony import orm

db = orm.Database()

class Statuses(db.Entity):
  pk = orm.PrimaryKey(int, auto=True)
  name = orm.Required(str, unique=True)
  items = orm.Set('Items')
  fulfill = orm.Set('Fulfill')

class Items(db.Entity):
  pk = orm.PrimaryKey(int, auto=True)
  name = orm.Required(str)
  status = orm.Required(Statuses)
  fulfil = orm.Set('Fulfill')
  timeout = orm.Optional(int, default = 24*3600)
  comment = orm.Optional(str)
  priority = orm.Required(int, unique=True)

class Fulfill(db.Entity):
  pk = orm.PrimaryKey(int, auto=True)
  dateTime = orm.Required(datetime, default=datetime.now())
  item = orm.Required(Items)
  status = orm.Required(Statuses)
  elapsedTime = orm.Required(int)

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
