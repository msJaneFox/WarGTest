import nose
import sqlite3
import random
from random import randint
result = nose.run()


class TestWeapons():
    def test_weapons(self):
        # Коннект к базе и выборка начальных значений
        conn = sqlite3.connect("ships.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM weapons")
        weapons = cursor.fetchall()
        cursor.execute("SELECT ship, weapon FROM ships")
        ships = cursor.fetchall()

        # Обновление рандомных полей в таблице weapons
        for i in range(6):
            fields = random.sample(['reload speed', 'rotational speed', 'diameter', 'power', 'count'], randint(1, 4))
            for field in fields:
                cursor.execute("UPDATE weapons SET {0}={1} WHERE weapon ='weapon-{2}'"
                               .format(field, randint(1, 100), i))

        # Получение новых значений weapons
        cursor.execute("SELECT * FROM weapons")
        weapons_new = cursor.fetchall()

        # Обновление полей engine в таблице Ships
        for i in range(200):
            cursor.executescript("UPDATE Ships SET weapon = (SELECT weapon FROM weapons ORDER BY RANDOM() LIMIT 1) "
                                 "WHERE ship='ships-{}'".format(i))

        # Получение новых значений Ships
        cursor.execute("SELECT ship, weapon FROM ships")
        ships_new = cursor.fetchall()

        # Проверка изменеий в таблице Ships
        for i in range(200):
            yield self.check_ships, ships_new[i], ships[i]

        # Проверка изменеий в таблице weapons
        for i in range(6):
            yield self.check_weapon, weapons_new[i], weapons[i]
        conn.close()

    def check_ships(self, new, old):
        print(new)
        assert new[0] == old[0], 'expected {0}, was {1}'.format(old[0], old[0])
        assert new[1] == old[1], 'expected {0}, was {1}'.format(old[1], old[1])

    def check_weapon(self, new, old):
        print(new)
        assert new[0] == old[0], 'expected {0}, was {1}'.format(old[0], old[0])
        assert new[1] == old[1], 'expected {0}, was {1}'.format(old[1], old[1])
