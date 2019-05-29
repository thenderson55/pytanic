import sqlite3 as sql
from os import path

ROOT = path.dirname(path.relpath(__file__))

def create_passenger(name, age, sex, pclass, fare, survived):
  connection = sql.connect(path.join(ROOT, 'database.db'))
  cur = connection.cursor()
  cur.execute('insert into passengers (name, age, sex, pclass, fare) values (?,?,?,?,?)', (name, age, sex, pclass, fare))
  connection.commit()
  connection.close()

def get_passengers():
  connection = sql.connect(path.join(ROOT, 'database.db'))
  cur = connection.cursor()
  cur.execute('select * from passengers')
  passengers = cur.fetchall()
  return passengers

def delete_passenger(id):
  connection = sql.connect(path.join(ROOT, 'database.db'))
  cur = connection.cursor()
  cur.execute("delete from passengers where id=?", (id,), )
  connection.commit()
  connection.close()

def delete_all_passengers():
  connection = sql.connect(path.join(ROOT, 'database.db'))
  cur = connection.cursor()
  cur.execute('DELETE FROM passengers')
  connection.commit()
  connection.close()



