import sqlite3
import json
with open('config.json') as data_file:
    config = json.load(data_file)

conn=sqlite3.connect(config['database'], check_same_thread=False)
conn.execute('pragma foreign_keys=ON')



def dict_factory(cursor, row):
    """This is a function use to format the json when retirve from the  mysql database"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


conn.row_factory = dict_factory

conn.execute('''CREATE TABLE if not exists project
(project_id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT NOT NULL,
owner TEXT NOT NULL,
cost_estimate NUMBER NOT NULL,
status TEXT NOT NULL);''')
print("created project")
conn.execute('''CREATE TABLE if not exists item
(item_id INTEGER PRIMARY KEY AUTOINCREMENT,
type TEXT NOT NULL,
quantity NUMBER NOT NULL,
cost NUMBER NOT NULL,
project_id INTEGER NOT NULL REFERENCES project(project_id) ON DELETE CASCADE);''')
print("created item")
conn.execute('''CREATE TABLE if not exists labor
(labor_id INTEGER PRIMARY KEY AUTOINCREMENT,
type TEXT NOT NULL,
quantity NUMBER NOT NULL,
salary NUMBER NOT NULL,
project_id INTEGER NOT NULL REFERENCES project(project_id) ON DELETE CASCADE);''')
print("created labor")
conn.execute('''CREATE TABLE if not exists land
(land_id INTEGER PRIMARY KEY AUTOINCREMENT,
type TEXT NOT NULL,
location TEXT NOT NULL,
size NUMBER NOT NULL,
cost NUMBER NOT NULL,
project_id INTEGER NOT NULL REFERENCES project(project_id) ON DELETE CASCADE);''')
print("created land")
conn.execute('''CREATE TABLE if not exists transport
(transport_id INTEGER PRIMARY KEY AUTOINCREMENT,
type TEXT NOT NULL,
rental_cost NUMBER NOT NULL,
quantity NUMBER NOT NULL,
project_id INTEGER NOT NULL REFERENCES project(project_id) ON DELETE CASCADE);''')
print("created transport")

