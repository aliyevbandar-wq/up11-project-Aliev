import os
import psycopg2
from psycopg2 import pool

# Принудительно заставляем Windows использовать UTF-8 для переменных окружения PostgreSQL
os.environ["PGCLIENTENCODING"] = "utf-8"


class Database:

    def __init__(self):
        try:
            self.connection_pool = pool.SimpleConnectionPool(
                1,
                5,
                dbname="toy_world_db",  # Имя базы данных
                user="postgres",  # Имя пользователя
                password="12345",  # Ваш пароль
                host="localhost",
                port="5432",
            )
            print("Пул соединений базы данных 'Мир игрушек' успешно создан.")
        except psycopg2.Error as e:
            print(f"Ошибка БД: {e}")
            self.connection_pool = None

    def get_connection(self):
        """Получает и возвращает свободное соединение из пула."""
        if self.connection_pool is None:
            return None
        return self.connection_pool.getconn()

    def release_connection(self, conn):
        """Возвращает использованное соединение обратно в пул."""
        if self.connection_pool and conn:
            self.connection_pool.putconn(conn)

    # ========================================================
    # ВОТ СЮДА МЫ ЕГО НАПИСАЛИ (ЗАДАНИЕ 3.1):
    # ========================================================
    def get_products(self):
        """3.1. Метод получает список всех товаров из таблицы products."""
        conn = self.get_connection()
        if conn is None:
            return []

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products;")
            return cursor.fetchall()
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return []
        finally:
            if "cursor" in locals():
                cursor.close()
            self.release_connection(conn)

    # ========================================================

    def close_all(self):
        """Закрывает все соединения в пуле перед завершением программы."""
        if self.connection_pool:
            self.connection_pool.closeall()
            print("Пул соединений закрыт.")


# Пример инициализации
if __name__ == "__main__":
    db = Database()
    print("Список игрушек:", db.get_products())
    db.close_all()
