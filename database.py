from tkinter import messagebox
import mysql.connector
from mysql.connector import Error


class Database:
    def __init__(self):
        self.config = {
            "host": "localhost",
            'database': 'shop_db',
            'user': 'root',
            'password': ''
        }
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                print("Connected")
        except Error as e:
            print(e)
            messagebox.showerror('Ошибка БД', f'Не удалось подключиться к базе данных: \n{e}')

    def fetch_one(self, query, params=None):
        cursor = self.connection.cursor(dictionary=True)

        try:
            cursor.execute(query, params or ())
            return cursor.fetchone()
        except Error as e:
            print(e)
            return None
        finally:
            cursor.close()

    def fetch_all(self, query, params=None):
        cursor = self.connection.cursor(dictionary=True)

        try:
            cursor.execute(query, params or ())
            return cursor.fetchall()
        except Error as e:
            print(e)
            return[]
        finally:
            cursor.close()
