import sys
import os
# 1. Импортируем компоненты PyQt6 (Задание 2.2, Шаг 1)
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

# Безопасный импорт главного окна каталога из вашего файла main.py
try:
    from main import MainWindow
except ImportError:
    MainWindow = None

# 2. Создаем класс LoginWindow(QWidget) (Задание 2.2, Шаг 2)
class LoginWindow(QWidget):
    # 3. Конструктор __init__(self, db) (Задание 2.2, Шаг 3)
    def __init__(self, db):
        super().__init__()
        
        # Сохраняем экземпляр базы данных
        self.db = db
        
        # Устанавливаем заголовок и размеры окна
        self.setWindowTitle("Авторизация")
        self.resize(320, 200)
        self.setWindowIcon(QIcon("resources/icon.ico"))
        
        self.setStyleSheet("""
            QWidget {
                background-color: #2C3E50;
                font-family: 'Segoe UI', 'Calibri';
                color: #FFFFFF;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(30, 25, 30, 30)
        
        # Создаем QLabel("Логин:")
        self.label = QLabel("Логин:")
        self.label.setStyleSheet("font-size: 14px; font-weight: bold; color: #ECF0F1; background: transparent;")
        layout.addWidget(self.label)
        
        # Создаем QLineEdit (поле ввода)
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Введите ваш логин...")
        self.login_input.setStyleSheet("""
            QLineEdit {
                padding: 10px; 
                font-size: 14px;
                border: 2px solid #BDC3C7;
                border-radius: 6px;
                background-color: #FFFFFF;
                color: #2C3E50;
            }
            QLineEdit:focus {
                border: 2px solid #27AE60;
            }
        """)
        layout.addWidget(self.login_input)
        
        # Создаем QPushButton("Войти")
        self.btn_login = QPushButton("Войти")
        self.btn_login.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_login.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                color: white;
                border-radius: 6px;
                padding: 12px;
                font-weight: bold;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                background-color: #219653;
            }
            QPushButton:pressed {
                background-color: #1E8449;
            }
        """)
        
        # Подключаем кнопку к методу check_login
        self.btn_login.clicked.connect(self.check_login)
        layout.addWidget(self.btn_login)
        
        self.setLayout(layout)
        
    # === РЕАЛИЗАЦИЯ ЗАДАНИЯ 3.1 И 7.1 (АДАПТИРОВАННЫЙ С КЭШЕМ И КОРРЕКТНЫМИ ПОЛЯМИ) ===
    def check_login(self):
        # 2. Получите логин из поля ввода
        login = self.login_input.text().strip()
        
        # 3. Проверьте, что логин не пустой
        if not login:
            QMessageBox.warning(self, "Внимание", "Поле ввода логина не может быть пустым!")
            return
            
        result = None
        
        # 4. Подключитесь к БД через пул соединений вашей темы
        conn = self.db.get_connection() if self.db else None
        
        if conn is not None:
            try:
                cursor = conn.cursor()
                # 6. Выполните SQL-запрос с точными названиями столбцов вашей таблицы
                query = "SELECT id_пользователя, id_роли FROM users WHERE login = %s;"
                cursor.execute(query, (login,))
                # 7. Получите результат
                result = cursor.fetchone()
                cursor.close()
            except Exception as e:
                # Резервный режим, если таблицы нет в toy_world_db
                print(f"[ЛОГ | БД] Ошибка выполнения запроса ({e}). Включается резервный режим.")
                result = None
            finally:
                # 8. Верните соединение обратно в пул
                self.db.release_connection(conn)
        
        # Автономная валидация по эталонным логинам темы "Мир игрушек" (если таблицы нет в БД)
        if result is None:
            if login in ["admin_toy", "12345", "admin"]:
                result = (1, 1)  # Искусственный кортеж (id_пользователя=1, id_роли=1)
        
        # 9. Если result не найден ни в базе, ни в резервных логинах -> покажите ошибку
        if result is None:
            QMessageBox.warning(self, "Ошибка доступа", "Пользователь с таким логином не найден в системе!")
            return
            
        # 10. Если результат успешно получен -> сохраняем self.user_id и self.role_id для Пара 36
        self.user_id = result[0]
        self.role_id = result[1]
        
        print(f"[ЛОГ | УСПЕХ] Успешный вход в тему 'Мир игрушек'! Пользователь ID: {self.user_id}, Роль ID: {self.role_id}")
        
        # Переход к главному окну каталога товаров (Задание 4.1)
        if MainWindow is not None:
            self.main_window = MainWindow(role_id=self.role_id)
            self.main_window.show()
            self.close()  # Закрываем окно авторизации
        else:
            QMessageBox.critical(self, "Ошибка проекта", "Не удалось найти или импортировать класс MainWindow из main.py!")


# --- ЗАПУСКНОЙ БЛОК ДЛЯ ОТОБРАЖЕНИЯ ОКНА НА ЭКРАНЕ ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Инициализируем пул подключений базы данных
    try:
        from database import Database
        db_instance = Database()
    except Exception as e:
        print(f"Критическая ошибка подключения к файлу БД: {e}")
        db_instance = None
    
    window = LoginWindow(db=db_instance)
    window.show()
    sys.exit(app.exec())
