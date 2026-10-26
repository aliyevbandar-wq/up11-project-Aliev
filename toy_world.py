import pg8000

# 1. Функция для своей темы (Мир игрушек)
def calculate_price_toy_world(item_id, base_price):
    try:
        # 2. Подключение к БД
        connection = pg8000.connect(
            host="localhost",
            port=5432,
            database="analysis_db",
            user="postgres",
            password="12345"
        )
        cursor = connection.cursor()
        
        # 3. SQL-запрос для проверки активности товара
        query = "SELECT 0 FROM products WHERE id_товара = %s;"
        cursor.execute(query, (item_id,))
        
        # 4. Получение результата
        result = cursor.fetchone()
        orders_count = result[0] if result else 0
            
        cursor.close()
        connection.close()
            
        # 5. Условие if/else для скидки 25%
        if orders_count == 0:
            return base_price * 0.75
        else:
            return base_price

    except Exception as error:
        print("Ошибка в самостоятельной работе:", error)
        return base_price

# 7. Тестовый запуск
if __name__ == "__main__":
    test_id = 1
    test_base_price = 790.0
    
    final_price = calculate_price_toy_world(test_id, test_base_price)
    
    print(f"--- Тест темы 'Мир игрушек' ---")
    print(f"Товар ID {test_id} | Базовая цена: {test_base_price} руб.")
    print(f"Итоговая цена: {final_price} руб.")
