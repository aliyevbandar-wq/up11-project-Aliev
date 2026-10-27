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

    # --- ЗАДАНИЕ 6.1: Метод для получения товаров темы "Мир игрушек" ---
    def get_products(self):
        """Получает список всех товаров из таблицы products (Мир игрушек)."""
        conn = self.get_connection()
        if conn is None:
            return []

        products_list = []
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products;")
            products_list = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(f"Ошибка при получении списка товаров: {e}")
        finally:
            self.release_connection(conn)

        return products_list

    def close_all(self):
        """Закрывает все соединения в пуле перед завершением программы."""
        if self.connection_pool:
            self.connection_pool.closeall()
            print("Пул соединений закрыт.")


# Тестирование метода самостоятельно
if __name__ == "__main__":
    db = Database()
    # Проверяем работу метода
    print("Список игрушек из базы данных:", db.get_products())
    db.close_all()
