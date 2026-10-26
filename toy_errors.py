import pg8000

# 1. Функция для своей темы (Мир игрушек)
def calculate_price_toy_world(item_id, base_price):
    # 2. Проверка входных данных
    if not isinstance(item_id, int):
        print("Ошибка: item_id должен быть целым числом (int)")
        return None
    if not isinstance(base_price, (int, float)) or base_price <= 0:
        print("Ошибка: base_price должен быть числом строго больше нуля")
        return None

    connection = None
    cursor = None
    
    # 3. try/except для БД
    try:
        connection = pg8000.connect(
            host="localhost",
            port=5432,
            database="analysis_db",
            user="postgres",
            password="12345"
        )
        cursor = connection.cursor()
        
        query = "SELECT 0 AS orders_count FROM products WHERE id_товара = %s;"
        cursor.execute(query, (item_id,))
        
        # 4. try/except для fetchone()
        try:
            result = cursor.fetchone()
            if result is None:
                print("Ошибка: Товар с таким ID не найден в БД")
                return None
        except pg8000.Error as fetch_error:
            print(f"Ошибка при извлечении данных: {fetch_error}")
            return None
            
        orders_count = result if isinstance(result, (tuple, list)) else result
            
        if orders_count == 0:
            return base_price * 0.75
        else:
            return base_price

    except pg8000.Error as db_error:
        print(f"Ошибка БД: {db_error}")
        return None
        
    # 5. finally для закрытия
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# 6. Тестовый запуск с неправильными данными
if __name__ == "__main__":
    print("--- ТЕСТ ТЕМЫ 'МИР ИГРУШЕК' (ОШИБКИ) ---")
    
    print("Тест 1 (неверный тип ID):")
    calculate_price_toy_world("не_число", 500)
    
    print("\nТест 2 (отрицательная цена):")
    calculate_price_toy_world(1, -150)
