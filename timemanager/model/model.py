from datetime import datetime

from pony import orm

db = orm.Database()

class Items(db.Entity):
  pk = orm.PrimaryKey(int, auto=True)
  name = orm.Required(str)
  fulfil = orm.Set('Fulfill')

class Fulfill(db.Entity):
  pk = orm.PrimaryKey(int, auto=True)
  dateTime = orm.Required(datetime, default=datetime.now())
  item = orm.Required(Items)
  status = orm.Required(str)
  elapsedTime = orm.Required(int)

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)
