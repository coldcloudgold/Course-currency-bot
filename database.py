"""Модуль для работы с бд.

Function
--------
create_db(name_db: str, name_tb: str) -> None
    функция создает базу данных
write_user_db(name_db: str, name_tb: str, message)
    функция записывает нового пользователя
"""

import sqlite3


def create_db(name_db: str, name_tb: str) -> None:
    """Функция создает базу данных и таблицу.

    Parameters
    ----------
    name_db : str
        имя базы данных
    name_tb : dict
        имя таблицы
    """
    with sqlite3.connect(f'{name_db}.db') as con:
        cur = con.cursor()
        cur.execute(f"CREATE TABLE IF NOT EXISTS {name_tb} (\
unique_id INTEGER PRIMARY KEY AUTOINCREMENT,\
user_id INTEGER,\
user_name TEXT,\
is_pay INTEGER NOT NULL DEFAULT 0)")
        con.commit()


def write_user_db(name_db: str, name_tb: str, message):
    """Функция заносит в таблицу базы данных нового пользователя.

    Parameters
    ----------
    name_db : str
        имя базы данных
    name_tb : dict
        имя таблицы
    message : message
        данные, полученные от пользователя
    """
    with sqlite3.connect(f'{name_db}.db') as con:
        cur = con.cursor()
        user_id = message.chat.id
        user_name = message.from_user.first_name
        cur.execute(f"SELECT * FROM {name_tb} WHERE user_id={user_id}")
        data = cur.fetchall()
        if data == []:
            cur.execute(
                f"INSERT INTO {name_tb} (user_id, user_name) VALUES (?, ?)", (user_id, user_name))
            con.commit()
    return data
