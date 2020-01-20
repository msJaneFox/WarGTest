import sqlite3
import os
from random import randint

os.remove("ships.db")
conn = sqlite3.connect("ships.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE engines
                  (engine text PRIMARY KEY, 
                  power integer, 
                  type integer)
                  """)
cursor.execute("""CREATE TABLE hulls
                  (hull text PRIMARY KEY, 
                  armor integer, 
                  type integer,
                  capacity integer)
                  """)
cursor.execute("""CREATE TABLE weapons
                  (weapon text PRIMARY KEY, 
                  reload speed integer, 
                  rotational speed integer,
                  diameter integer,
                  power volley integer,
                  count integer)
                  """)
cursor.executescript("""PRAGMA foreign_keys=on;
                  CREATE TABLE Ships
                  (ship text PRIMARY KEY,
                  weapon text, 
                  hull text,
                  engine text,
                  FOREIGN KEY (weapon) REFERENCES weapons(weapon),
                  FOREIGN KEY (hull) REFERENCES hulls(hull),
                  FOREIGN KEY (engine) REFERENCES engines(engine))
               """)


for engines in range(6):
    cursor.execute("INSERT INTO engines VALUES('engine-{0}', {1}, {2})"
                   .format(engines, randint(1, 100), randint(1, 100)))
for hulls in range(5):
    cursor.execute("INSERT INTO hulls VALUES('hull-{0}', {1}, {2}, {3})"
                   .format(hulls, randint(1, 100), randint(1, 100), randint(1, 100)))
for weapons in range(20):
    cursor.execute("INSERT INTO weapons VALUES('weapon-{0}', {1}, {2}, {3}, {4}, {5})"
                   .format(weapons, randint(1, 100), randint(1, 100), randint(1, 100), randint(1, 100), randint(1, 100)))
for ships in range(200):
    cursor.executescript("INSERT INTO Ships VALUES('ships-{}', "
                         "(SELECT weapon FROM weapons ORDER BY RANDOM() LIMIT 1), "
                         "(SELECT hull FROM hulls ORDER BY RANDOM() LIMIT 1), "
                         "(SELECT engine FROM engines ORDER BY RANDOM() LIMIT 1))".format(ships))
conn.commit()
conn.close()
