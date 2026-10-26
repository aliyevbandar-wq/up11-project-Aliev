import pg8000
# Импортируем функцию из созданного ранее файла discount.py
from discount import calculate_price

try:
    # 1. Подключитесь к БД, получите курсор
    connection = pg8000.connect(
        host="localhost",
        port=5432,
        database="analysis_db",
        user="postgres",
        password="12345"
    )
    cursor = connection.cursor()
    
    # 2. Выполните SELECT (адаптировано под точные названия колонок вашей БД)
    query = "SELECT id_товара, наименование, базовая_цена FROM products;"
    cursor.execute(query)
    
    # 3. Получите все строки: cursor.fetchall()
    products = cursor.fetchall()
    
    # 4. В цикле for пройдитесь по каждой строке
    for row in products:
        # Извлекаем данные из кортежа строки (для pg8000 элементы строки доступны по индексам)
        product_id = row[0]
        name = row[1]
        price = float(row[2]) # Преобразуем numeric из БД в число с плавающей точкой
        
        # 5. Для каждого вызовите calculate_price(product_id, price)
        final_price = calculate_price(product_id, price)
        
        # 6. Выведите результат через print
        print(f"ID: {product_id} | {name} | Базовая: {price} руб. | Итоговая: {final_price} руб.")
        
    # Закрываем ресурсы после окончания цикла
    cursor.close()
    connection.close()

except Exception as error:
    print("Ошибка при обработке списка товаров:", error)
