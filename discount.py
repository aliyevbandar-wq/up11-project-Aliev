import pg8000

# ЗАДАНИЕ 4.1: Функция расчета цены с точечной обработкой ошибок БД
def calculate_price(product_id, base_price):
    # 1. Обернули блок подключения к БД в try:
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
        cursor.execute(query, (product_id,))
        
        result = cursor.fetchone()
        
        if result:
            orders_count = result if isinstance(result, (tuple, list)) else result
        else:
            orders_count = 0
            
        cursor.close()
        connection.close()
            
        if orders_count == 0:
            return base_price * 0.75
        else:
            return base_price

    # 2. Добавили перехват конкретной ошибки базы данных pg8000.Error
    except pg8000.Error as e:
        # 3. Выводим сообщение об ошибке БД и возвращаем None по заданию
        print(f"Ошибка БД: {e}")
        return None
        
    # Дополнительный общий перехват на случай других ошибок Python (например, деление на ноль)
    except Exception as e:
        print(f"Другая ошибка: {e}")
        return base_price

# ЗАДАНИЕ 3.2: Тестовый запуск
if __name__ == "__main__":
    final_price = calculate_price(1, 1000)
    print(f"Итоговая цена товара №1: {final_price} руб.")
