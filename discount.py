# 1. Функция add_product(name, price, category_id)
def add_product(name, price, category_id):
    # 2. Проверка: name не пустой, price > 0, category_id — число
    if not name or str(name).strip() == "":
        print("Ошибка: Название товара не должно быть пустым")
        return False
    if not isinstance(price, (int, float)) or price <= 0:
        print("Ошибка: Цена должна быть числом строго больше нуля")
        return False
    if not isinstance(category_id, int):
        print("Ошибка: Идентификатор категории должен быть целым числом")
        return False

    connection = None
    cursor = None
    try:
        connection = pg8000.connect(
            host="localhost",
            port=5432,
            database="analysis_db",
            user="postgres",
            password="12345"
        )
        cursor = connection.cursor()
        
        # 3. try/except для INSERT (адаптировано под поля вашей таблицы products)
        try:
            query = "INSERT INTO products (наименование, базовая_цена) VALUES (%s, %s);"
            cursor.execute(query, (name, price))
        except pg8000.Error as e:
            print(f"Ошибка выполнения INSERT: {e}")
            return False

        # 4. try/except для conn.commit()
        try:
            connection.commit()
            print(f"Товар '{name}' успешно добавлен в БД!")
            return True
        except pg8000.Error as e:
            print(f"Ошибка при фиксации транзакции commit(): {e}")
            return False

    except pg8000.Error as e:
        print(f"Ошибка подключения к БД: {e}")
        return False
        
    # 5. finally для гарантированного закрытия ресурсов
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            if __name__ == "__main__":
    print("--- ЗАПУСК ТЕСТОВ ОШИБОК ВСТАВКИ ---")
    
    print("Тест 1 (пустое имя):")
    add_product("", 1000, 1)          
    
    print("\nТест 2 (цена < 0):")
    add_product("Часы", -100, 1)      
    
    print("\nТест 3 (категории нет):")
    add_product("Часы", 1000, 99999)  
    
    print("\nТест 4 (всё правильно):")
    add_product("Часы", 1000, 1)      
