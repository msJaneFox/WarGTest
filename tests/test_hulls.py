import nose
import sqlite3
import random
from random import randint
result = nose.run()


class TestHulls():
    def test_hulls(self):
        # Коннект к базе и выборка начальных значений
        conn = sqlite3.connect("ships.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM hulls")
        hulls = cursor.fetchall()
        cursor.execute("SELECT ship, hull FROM ships")
        ships = cursor.fetchall()

        # Обновление рандомных полей в таблице hulls
        for i in range(6):
            fields = random.sample(['armor', 'type', 'capacity'], randint(1, 2))
            for field in fields:
                cursor.execute("UPDATE hulls SET {0}={1} WHERE hull ='hull-{2}'"
                               .format(field, randint(1, 100), i))

        # Получение новых значений hulls
        cursor.execute("SELECT * FROM hulls")
        hulls_new = cursor.fetchall()

        # Обновление полей hull в таблице Ships
        for i in range(200):
            cursor.executescript("UPDATE Ships SET hull = (SELECT hull FROM hulls ORDER BY RANDOM() LIMIT 1) "
                                 "WHERE ship='ships-{}'".format(i))

        # Получение новых значений Ships
        cursor.execute("SELECT ship, hull FROM ships")
        ships_new = cursor.fetchall()

        # Проверка изменеий в таблице Ships
        for i in range(200):
            yield self.check_ships, ships_new[i], ships[i]

        # Проверка изменеий в таблице hulls
        for i in range(6):
            yield self.check_hulls, hulls_new[i], hulls[i]
        conn.close()

    def check_ships(self, new, old):
        print(new)
        assert new[0] == old[0], 'expected {0}, was {1}'.format(old[0], old[0])
        assert new[1] == old[1], 'expected {0}, was {1}'.format(old[1], old[1])

    def check_hulls(self, new, old):
        print(new)
        assert new[0] == old[0], 'expected {0}, was {1}'.format(old[0], old[0])
        assert new[1] == old[1], 'expected {0}, was {1}'.format(old[1], old[1])
