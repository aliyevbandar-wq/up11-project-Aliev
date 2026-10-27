import os

def test_resources():
    print("=== ТЕСТ ПРОВЕРКИ РЕСУРСОВ ===")
    
    # Шаг 3: Проверка заглушки picture.png
    stub_path = "resources/picture.png"
    if os.path.exists(stub_path):
        print(f"☑ Успех: Заглушка '{stub_path}' найдена.")
    else:
        print(f"☒ Ошибка: Заглушка '{stub_path}' ОТСУТСТВУЕТ!")
        
    # Шаг 4: Проверка конкретного файла изображения из БД
    # На основе вашего каталога "Мир игрушек" проверяем первый файл
    product_img_path = "resources/IMG_14_001.png" 
    if os.path.exists(product_img_path):
        print(f"☑ Успех: Изображение товара '{product_img_path}' найдено.")
    else:
        print(f"☒ Ошибка: Изображение товара '{product_img_path}' ОТСУТСТВУЕТ!")

if __name__ == "__main__":
    test_resources()
