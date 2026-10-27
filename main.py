import sys
import os

# Принудительно заставляем Windows использовать UTF-8 для PostgreSQL
os.environ["PGCLIENTENCODING"] = "utf-8"

# Импортируем класс Database из вашего файла database.py
from database import Database

# Импорты графических компонентов PyQt6
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QScrollArea, QPushButton
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt

# --- Глобальный словарь для кэширования изображений (Домашнее задание) ---
IMAGE_CACHE = {}

# --- Функция создания карточки товара "Мир игрушек" ---
def create_card(product):
    card = QWidget()
    card.setStyleSheet("""
        QWidget {
            background-color: #F9F9F9;
            border: 1px solid #E0E0E0;
            border-radius: 8px;
        }
    """)
    
    main_layout = QHBoxLayout()
    
    # --- ИНДЕКСЫ ДАННЫХ ИЗ ВАШЕЙ БД ---
    product_name = product[1]  
    product_price = product[2] 
    
    # --- БЛОК С ИЗОБРАЖЕНИЕМ И ЗАГЛУШКОЙ ---
    img_label = QLabel()
    img_label.setFixedWidth(100)  # Ширина под масштабирование 100x100
    img_label.setStyleSheet("border: none; background-color: transparent;")
    
    # 1. Проверка на None для image_path и автогенерация имени файла по ID, если поля нет
    if len(product) > 3 and product[3] is not None:
        image_name = product[3]
    else:
        image_name = f"IMG_14_{str(product[0]).zfill(3)}.png"
        
    full_image_path = f"resources/{image_name}"
    ext = os.path.splitext(image_name)[1].lower()
    
    pixmap = None
    
    # 3. Дополнительно: Проверка допустимого формата файла (PNG, JPG)
    if ext in ['.png', '.jpg', '.jpeg']:
        # 3. Дополнительно: Кэширование изображений (проверяем, загружался ли файл ранее)
        if full_image_path in IMAGE_CACHE:
            pixmap = IMAGE_CACHE[full_image_path]
        elif os.path.exists(full_image_path):
            pixmap = QPixmap(full_image_path)
            IMAGE_CACHE[full_image_path] = pixmap  # Сохраняем в кэш
        else:
            # 1. Логирование ненайденных файлов в консоль
            print(f"[ЛОГ | ОШИБКА] Файл не найден на диске: '{full_image_path}'. Используется заглушка.")
    else:
        print(f"[ЛОГ | ПРЕДУПРЕЖДЕНИЕ] Неподдерживаемый формат файла: '{image_name}'")

    # Если картинка не загрузилась или отсутствует, ставим picture.png
    if pixmap is None or pixmap.isNull():
        stub_path = "resources/picture.png"
        if stub_path in IMAGE_CACHE:
            pixmap = IMAGE_CACHE[stub_path]
        else:
            pixmap = QPixmap(stub_path)
            IMAGE_CACHE[stub_path] = pixmap
        
    # Масштабирование до размеров 100x100 по условию задания
    img_label.setPixmap(pixmap.scaled(
        100, 
        100, 
        Qt.AspectRatioMode.KeepAspectRatio, 
        Qt.TransformationMode.SmoothTransformation
    ))
    main_layout.addWidget(img_label)
    
    # --- БЛОК С ТЕКСТОВОЙ ИНФОРМАЦИЕЙ ---
    text_layout = QVBoxLayout()
    
    name_label = QLabel(f"<b>Игрушка:</b> {product_name}")
    name_label.setStyleSheet("font-size: 16px; color: #2C3E50; border: none; background-color: transparent;")
    
    category_label = QLabel("<b>Категория:</b> Детские товары / Игрушки")
    category_label.setStyleSheet("color: #7F8C8D; font-size: 12px; border: none; background-color: transparent;")
    
    stock_label = QLabel("<b>Возраст:</b> 3+ | В наличии")
    stock_label.setStyleSheet("color: #27AE60; font-size: 12px; border: none; background-color: transparent;")
    
    material_label = QLabel("<b>Материал:</b> Эко-мех, гипоаллергенный наполнитель")
    material_label.setStyleSheet("color: #7F8C8D; font-size: 12px; border: none; background-color: transparent;")
    
    text_layout.addWidget(name_label)
    text_layout.addWidget(category_label)
    text_layout.addWidget(stock_label)
    text_layout.addWidget(material_label)
    
    main_layout.addLayout(text_layout)
    
    # --- БЛОК С ЦЕНОЙ ---
    price_label = QLabel(f"{product_price} ₽")
    price_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #E74C3C; border: none; background-color: transparent;")
    price_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
    main_layout.addWidget(price_label)
    
    card.setLayout(main_layout)
    card.setFixedHeight(110)
    
    return card


# Создание класса главного окна приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Мир игрушек — Каталог")
        self.resize(800, 600)
        
        self.setWindowIcon(QIcon("resources/IMG_14_001.png"))
        
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
        
        central = QWidget()
        layout = QVBoxLayout()
        
        # --- ВЕРХНЯЯ ПАНЕЛЬ С КНОПКОЙ ВЫХОДА И ВЫРОВНЕННЫМ ЛОГОТИПОМ ---
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 10, 0, 10)
        
        # Левый невидимый блок-заглушка для удержания логотипа строго по центру
        left_spacer = QWidget()
        left_spacer.setFixedWidth(90)  # Ширина совпадает с кнопкой выхода
        top_layout.addWidget(left_spacer)
        
        top_layout.addStretch()
        
        # Логотип (центрируется за счёт stretch-интервалов и левого виджета)
        logo = QLabel()
        logo.setPixmap(QPixmap("resources/IMG_14_001.png").scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))  
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)       
        top_layout.addWidget(logo)
        
        top_layout.addStretch()
        
        # Кнопка выхода справа
        self.btn_exit = QPushButton("Выход")
        self.btn_exit.setFixedSize(90, 35)
        self.btn_exit.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border-radius: 5px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        self.btn_exit.clicked.connect(self.close)
        top_layout.addWidget(self.btn_exit)
        
        layout.addLayout(top_layout)
        
        title_label = QLabel("Мир игрушек — Каталог")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #000000;
            margin-top: 10px;
            margin-bottom: 10px;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        layout.addWidget(title_label)
        
        # Подключение к базе данных
        self.db = Database()

        # Получаем товары
        self.products = self.db.get_products()
        
        # Область прокрутки (QScrollArea)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        self.scroll_widget = QWidget()
        self.scroll_widget.setStyleSheet("background-color: transparent;")
        
        self.cards_layout = QVBoxLayout(self.scroll_widget)
        self.cards_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Отрисовка карточек
        for product in self.products:
            card_widget = create_card(product)
            self.cards_layout.addWidget(card_widget)
            
        self.scroll_area.setWidget(self.scroll_widget)
        layout.addWidget(self.scroll_area)
        
        central.setLayout(layout)
        self.setCentralWidget(central)

    def closeEvent(self, event):
        self.db.close_all()
        event.accept()

if __name__ == "__main__":
    if sys.platform == 'win32':
        import ctypes
        myappid = 'mycompany.myproduct.subproduct.version'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
     
    sys.exit(app.exec())
