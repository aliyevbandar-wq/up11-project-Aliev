import psycopg2
from database import Database


def test_connection():
    # 3. Создаем экземпляр класса Database
    db = Database()

    # 4. Получаем соединение из пула
    conn = db.get_connection()

    if conn is None:
        print("Не удалось получить соединение из пула.")
        return

    try:
        # Открываем курсор для выполнения SQL-команд
        cursor = conn.cursor()

        # [Дополнительный шаг]: Создаем таблицу products, если её ещё нет
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                price NUMERIC(10, 2) NOT NULL
            );
        """
        )
        conn.commit()  # Фиксируем создание таблицы

        # 5. Выполняем SELECT COUNT(*) FROM products
        cursor.execute("SELECT COUNT(*) FROM products;")

        # 6. Выводим результат
        count = cursor.fetchone()[0]
        print(
            f"Успешное подключение! Количество товаров в базе 'Мир игрушек': {count}"
        )

        cursor.close()

    except Exception as e:
        print(f"Ошибка при работе с базой данных: {e}")

    finally:
        # 7. Возвращаем соединение обратно в пул
        db.release_connection(conn)

        # 8. Закрываем пул
        db.close_all()


if __name__ == "__main__":
    test_connection()
