import psycopg2

def check_login(login):
    db_params = {
        "dbname": "toy_world_db",
        "user": "postgres",
        "password": "1234",  # Сюда нужно написать ВАШ реальный пароль от СУБД pgAdmin
        "host": "localhost",
        "port": "5432"
    }
    
    try:
        # Устанавливаем соединение с сервером
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        
        # Запрос к БД
        query = "SELECT fio FROM users WHERE login = %s;"
        cursor.execute(query, (login,))
        user_record = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        # Ветвление алгоритма
        if user_record:
            return f"Вход разрешён. Добро пожаловать, {user_record[0]}!"
        else:
            return "Ошибка: неверный логин"
            
    except Exception as error:
        # Если база недоступна на паре, делаем симуляцию по вашей блок-схеме:
        if login == "admin_toy":
            return "Вход разрешён (Режим симуляции: admin_toy)"
        else:
            return "Ошибка: неверный логин (Режим симуляции)"

# Проверочный запуск функции
if __name__ == "__main__":
    print(check_login("admin_toy"))  # Должно выдать: Вход разрешён
    print(check_login("unknown_user"))  # Должно выдать: Ошибка: неверный логин
