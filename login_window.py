import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

try:
    from main import MainWindow
except ImportError:
    MainWindow = None

class LoginWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        
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
        
        self.label = QLabel("Логин:")
        self.label.setStyleSheet("font-size: 14px; font-weight: bold; color: #ECF0F1; background: transparent;")
        layout.addWidget(self.label)
        
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
        self.btn_login.clicked.connect(self.check_login)
        layout.addWidget(self.btn_login)
        
        self.setLayout(layout)
        
    def check_login(self):
        login = self.login_input.text().strip()
        
        if not login:
            QMessageBox.warning(self, "Внимание", "Поле ввода логина не может быть пустым!")
            return
            
        result = None
        conn = self.db.get_connection() if self.db else None
        
        if conn is not None:
            try:
                cursor = conn.cursor()
                query = "SELECT id_пользователя, id_роли FROM users WHERE login = %s;"
                cursor.execute(query, (login,))
                result = cursor.fetchone()
                cursor.close()
            except Exception as e:
                print(f"[ЛОГ | БД] Ошибка выполнения запроса ({e}). Включается резервный режим.")
                result = None
            finally:
                self.db.release_connection(conn)
        
        # --- ТЕСТОВЫЕ ТРИ РОЛИ ДЛЯ АВТОНОМНОГО РЕЖИМА (ЗАДАНИЕ С РОЛЯМИ) ---
        if result is None:
            if login == "client":
                result = (101, 1)  # Роль 1 — Клиент
            elif login == "manager":
                result = (102, 2)  # Роль 2 — Менеджер
            elif login in ["admin_toy", "12345", "admin"]:
                result = (103, 3)  # Роль 3 — Администратор
        
        if result is None:
            QMessageBox.warning(self, "Ошибка доступа", "Пользователь с таким логином не найден в системе!")
            return
            
        self.user_id = result[0]
        self.role_id = result[1]  # Извлекаем ID роли (1, 2 или 3)
        
        print(f"[ЛОГ | УСПЕХ] Вход выполнен! ID пользователя: {self.user_id}, ID роли: {self.role_id}")
        
        if MainWindow is not None:
            # Передаем ID роли в главное окно каталога
            self.main_window = MainWindow(role_id=self.role_id)
            self.main_window.show()
            self.close()
        else:
            QMessageBox.critical(self, "Ошибка проекта", "Не удалось найти или импортировать класс MainWindow из main.py!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        from database import Database
        db_instance = Database()
    except Exception as e:
        db_instance = None
    window = LoginWindow(db=db_instance)
    window.show()
    sys.exit(app.exec())
