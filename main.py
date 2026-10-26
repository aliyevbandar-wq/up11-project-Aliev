import sys
# Импорты графических компонентов PyQt6
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt

# Создание класса главного окна приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 1. Базовые параметры окна под тему «Мир игрушек»
        self.setWindowTitle("Мир игрушек — Каталог")
        self.resize(800, 600)
        
        # ИКОНКА В УГЛУ ОКНА
        self.setWindowIcon(QIcon("resources/Мир игрушек.ico"))
        
        # 2. Настройка корпоративного стиля приложения
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFFFFF;
            }
            QWidget {
                font-family: 'Calibri';
                font-size: 14px;
                color: #000000;
            }
        """)
        
        # 3. Создание центрального виджета и вертикального слоя
        central = QWidget()
        layout = QVBoxLayout()
        
        # --- ЗАДАНИЕ 4.1: Добавление графического логотипа ---
        logo = QLabel()
        # Используем точное имя горизонтального логотипа из вашей папки resources
        logo.setPixmap(QPixmap("resources/Мир игрушек.png"))  
        logo.setScaledContents(False)                         # Сохраняем пропорции
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)       # Центрируем картинку
        layout.addWidget(logo)
        
        # --- ЗАДАНИЕ 7.1 (Самостоятельная работа): Текстовый заголовок темы ---
        title_label = QLabel("Мир игрушек — Каталог")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #000000;
            margin-top: 15px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter) # Выравнивание по центру
        layout.addWidget(title_label)
        
        # Добавляем пустой промежуток снизу, чтобы элементы прижались к верху окна
        layout.addStretch()
        
        # Привязка слоя к центральному виджету формы
        central.setLayout(layout)
        self.setCentralWidget(central)

# Точка входа в программу и запуск графического цикла
if __name__ == "__main__":
    # Фикс для Windows, чтобы иконка корректно отображалась на панели задач отдельным приложением
    if sys.platform == 'win32':
        import ctypes
        myappid = 'mycompany.myproduct.subproduct.version'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
