import nose
import sqlite3
import random
from random import randint
result = nose.run()


class TestEngines():
    def test_engines(self):
        # Коннект к базе и выборка начальных значений
        conn = sqlite3.connect("ships.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM engines")
        engines = cursor.fetchall()
        cursor.execute("SELECT ship, engine FROM ships")
        ships = cursor.fetchall()

        # Обновление рандомных полей в таблице engines
        for i in range(6):
            fields = random.sample(['power', 'type'], 1)
            for field in fields:
                cursor.execute("UPDATE engines SET {0}={1} WHERE engine ='engine-{2}'"
                               .format(field, randint(1, 100), i))

        # Получение новых значений engines
        cursor.execute("SELECT * FROM engines")
        engines_new = cursor.fetchall()

        # Обновление полей engine в таблице Ships
        for i in range(200):
            cursor.executescript("UPDATE Ships SET engine = (SELECT engine FROM engines ORDER BY RANDOM() LIMIT 1) "
                                 "WHERE ship='ships-{}'".format(i))

        # Получение новых значений Ships
        cursor.execute("SELECT ship, engine FROM ships")
        ships_new = cursor.fetchall()

        # Проверка изменеий в таблице Ships
        for i in range(200):
            yield self.check_ships, ships_new[i], ships[i]

        # Проверка изменеий в таблице engines
        for i in range(6):
            yield self.check_engines, engines_new[i], engines[i]
        conn.close()

    def check_ships(self, new, old):
        print(new)
        assert new[0] == old[0], 'expected {0}, was {1}'.format(old[0], old[0])
        assert new[1] == old[1], 'expected {0}, was {1}'.format(old[1], old[1])

    def check_engines(self, new, old):
        print(new)
        assert new[0] == old[0], 'expected {0}, was {1}'.format(old[0], old[0])
        assert new[1] == old[1], 'expected {0}, was {1}'.format(old[1], old[1])
