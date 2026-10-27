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

# Глобальный словарь для кэширования изображений (Домашнее задание)
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
        QWidget:hover {
            background-color: #F5F7FA;
            border: 1px solid #BDC3C7;
        }
    """)
    
    main_layout = QHBoxLayout()
    main_layout.setContentsMargins(15, 10, 15, 10)
    
    # --- ИНДЕКСЫ ДАННЫХ ИЗ ВАШЕЙ БД ---
    product_name = product[1]  
    product_price = product[2] 
    
    # --- БЛОК С ИЗОБРАЖЕНИЕМ И ЗАГЛУШКОЙ ---
    img_label = QLabel()
    img_label.setFixedSize(100, 100)
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
        if full_image_path in IMAGE_CACHE:
            pixmap = IMAGE_CACHE[full_image_path]
        elif os.path.exists(full_image_path):
            pixmap = QPixmap(full_image_path)
            IMAGE_CACHE[full_image_path] = pixmap  # Сохраняем в кэш
        else:
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
    img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    main_layout.addWidget(img_label)
    
    # --- БЛОК С ТЕКСТОВОЙ ИНФОРМАЦИЕЙ ---
    text_layout = QVBoxLayout()
    text_layout.setSpacing(4)
    
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
    main_layout.addStretch()
    
    # --- БЛОК С ЦЕНОЙ ---
    price_label = QLabel(f"{product_price} ₽")
    price_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #E74C3C; border: none; background-color: transparent;")
    price_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
    main_layout.addWidget(price_label)
    
    card.setLayout(main_layout)
    card.setFixedHeight(120)
    
    return card


# Создание класса главного окна приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Мир игрушек — Каталог")
        self.resize(850, 650)
        
        # Четкая системная иконка .ico для заголовка окна и панели задач Windows
        self.setWindowIcon(QIcon("resources/icon.ico"))
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFFFFF;
            }
            QWidget {
                font-family: 'Segoe UI', 'Calibri';
                font-size: 14px;
                color: #000000;
            }
        """)
        
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(20, 15, 20, 15)
        
        # --- ВЕРХНЯЯ ПАНЕЛЬ: ЛОГОТИП И ЗАГОЛОВОК СЛЕВА, КНОПКА СПРАВА ---
        top_layout = QHBoxLayout()
        top_layout.setSpacing(15) 
        top_layout.setContentsMargins(0, 0, 0, 0)
        
        # 1. Логотип слева (Размер увеличен до 150x150)
        logo = QLabel()
        logo.setFixedSize(150, 150)  
        logo.setStyleSheet("border: none;")
        
        logo_pixmap = QPixmap("resources/logo.png")
        if not logo_pixmap.isNull():
            logo.setPixmap(logo_pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        logo.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)       
        top_layout.addWidget(logo)
        
        # 2. Текстовый заголовок сразу после логотипа
        title_label = QLabel("Мир игрушек — Каталог")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2C3E50;
            border: none;
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        top_layout.addWidget(title_label)
        
        # Разделитель расталкивает блок (лого + заголовок) влево, а кнопку выхода вправо
        top_layout.addStretch()
        
        # 3. Кнопка выхода справа
        self.btn_exit = QPushButton("Выход")
        self.btn_exit.setFixedSize(100, 35)
        self.btn_exit.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border-radius: 6px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
            QPushButton:pressed {
                background-color: #962D22;
            }
        """)
        self.btn_exit.clicked.connect(self.close)
        top_layout.addWidget(self.btn_exit)
        
        layout.addLayout(top_layout)
        
        # Небольшой пустой отступ снизу под шапкой
        layout.addSpacing(10)
        
        # Подключение к базе данных
        self.db = Database()
        self.products = self.db.get_products()
        
        # Область прокрутки (QScrollArea)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea { 
                border: none; 
                background-color: transparent; 
            }
            QScrollBar:vertical {
                border: none;
                background: #F1F1F1;
                width: 10px;
                margin: 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #C1C1C1;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #A8A8A8;
            }
        """)
        
        self.scroll_widget = QWidget()
        self.scroll_widget.setStyleSheet("background-color: transparent;")
        
        self.cards_layout = QVBoxLayout(self.scroll_widget)
        self.cards_layout.setSpacing(12)
        self.cards_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Отрисовка карточек
        for product in self.products:
            card_widget = create_card(product)
            self.cards_layout.addWidget(card_widget)
            
        self.scroll_area.setWidget(self.scroll_widget)
        layout.addWidget(self.scroll_area)
        
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
