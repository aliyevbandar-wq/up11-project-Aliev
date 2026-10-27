from database import Database

def test_get_products():
    # Создаем экземпляр Database
    db = Database()
    
    try:
        # Вызываем метод get_products()
        products = db.get_products()
        
        # Выводим результат и количество
        print(f"Результат метода get_products(): {products}")
        print(f"Количество полученных товаров: {len(products)}")
        
    except Exception as e:
        print(f"Произошла ошибка при тестировании метода: {e}")
    finally:
        # Закрываем пул
        db.close_all()

if __name__ == "__main__":
    test_get_products()
