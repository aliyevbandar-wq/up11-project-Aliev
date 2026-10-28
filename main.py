import sys
import os

os.environ["PGCLIENTENCODING"] = "utf-8"

from database import Database
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QScrollArea, QPushButton
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt

IMAGE_CACHE = {}

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
    
    product_name = product[1]  
    product_price = product[2] 
    
    img_label = QLabel()
    img_label.setFixedSize(100, 100)
    img_label.setStyleSheet("border: none; background-color: transparent;")
    
    if len(product) > 3 and product[3] is not None:
        image_name = product[3]
    else:
        image_name = f"IMG_14_{str(product[0]).zfill(3)}.png"
        
    full_image_path = f"resources/{image_name}"
    ext = os.path.splitext(image_name)[1].lower()
    
    pixmap = None
    if ext in ['.png', '.jpg', '.jpeg']:
        if full_image_path in IMAGE_CACHE:
            pixmap = IMAGE_CACHE[full_image_path]
        elif os.path.exists(full_image_path):
            pixmap = QPixmap(full_image_path)
            IMAGE_CACHE[full_image_path] = pixmap
        else:
            print(f"[ЛОГ | ОШИБКА] Файл не найден на диске: '{full_image_path}'. Используется заглушка.")

    if pixmap is None or pixmap.isNull():
        stub_path = "resources/picture.png"
        if stub_path in IMAGE_CACHE:
            pixmap = IMAGE_CACHE[stub_path]
        else:
            pixmap = QPixmap(stub_path)
            IMAGE_CACHE[stub_path] = pixmap
        
    img_label.setPixmap(pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
    img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    main_layout.addWidget(img_label)
    
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
    
    price_label = QLabel(f"{product_price} ₽")
    price_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #E74C3C; border: none; background-color: transparent;")
    price_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
    main_layout.addWidget(price_label)
    
    card.setLayout(main_layout)
    card.setFixedHeight(120)
    
    return card


class MainWindow(QMainWindow):
    def __init__(self, role_id=None, user_fio="Гость"):
        super().__init__()
        self.role_id = role_id  
        self.user_fio = user_fio  
        self.setup_ui()
        self.setup_role_interface()


    def setup_ui(self):
        self.setWindowTitle("Мир игрушек — Каталог")
        self.resize(1000, 650)  
        self.setWindowIcon(QIcon("resources/icon.ico"))
        
        self.setStyleSheet("""
            QMainWindow { background-color: #FFFFFF; }
            QWidget { font-family: 'Segoe UI', 'Calibri'; font-size: 14px; color: #000000; }
        """)
        
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(20, 15, 20, 15)
        
        top_layout = QHBoxLayout()
        top_layout.setSpacing(12) 
        top_layout.setContentsMargins(0, 0, 0, 0)
        
        logo = QLabel()
        logo.setFixedSize(100, 100)  
        logo_pixmap = QPixmap("resources/logo.png")
        if not logo_pixmap.isNull():
            logo.setPixmap(logo_pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        logo.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)       
        top_layout.addWidget(logo)
        
        title_label = QLabel("Мир игрушек — Каталог")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2C3E50; border: none;")
        top_layout.addWidget(title_label)
        
        self.role_label = QLabel()
        self.role_label.setStyleSheet("font-size: 13px; font-weight: bold; color: #7F8C8D; border: none; padding-left: 10px;")
        top_layout.addWidget(self.role_label)
        
        top_layout.addStretch()
        self.user_label = QLabel(f"👤 {self.user_fio}")
        self.user_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2C3E50; border: none; padding-right: 15px;")
        top_layout.addWidget(self.user_label)

        
        self.btn_add_product = QPushButton("Добавить товар")
        self.btn_add_product.setFixedSize(120, 35)
        self.btn_add_product.setStyleSheet("""
            QPushButton { background-color: #34495E; color: white; border-radius: 6px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #2C3E50; }
        """)
        top_layout.addWidget(self.btn_add_product)
        
        self.order_button = QPushButton("Оформить заказ")
        self.order_button.setFixedSize(130, 35)
        self.order_button.setStyleSheet("""
            QPushButton { background-color: #27AE60; color: white; border-radius: 6px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #219653; }
        """)
        
        self.manager_button = QPushButton("Заказы (менеджер)")
        self.manager_button.setFixedSize(150, 35)
        self.manager_button.setStyleSheet("""
            QPushButton { background-color: #2980B9; color: white; border-radius: 6px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #1F6391; }
        """)
        
        self.admin_button = QPushButton("Админ-панель")
        self.admin_button.setFixedSize(120, 35)
        self.admin_button.setStyleSheet("""
            QPushButton { background-color: #8E44AD; color: white; border-radius: 6px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #732D91; }
        """)
        
        top_layout.addWidget(self.order_button)
        top_layout.addWidget(self.manager_button)
        top_layout.addWidget(self.admin_button)
            
        self.btn_exit = QPushButton("Выход")
        self.btn_exit.setFixedSize(80, 35)
        self.btn_exit.setStyleSheet("""
            QPushButton { background-color: #E74C3C; color: white; border-radius: 6px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #C0392B; }
        """)
        self.btn_exit.clicked.connect(self.logout_user)
        top_layout.addWidget(self.btn_exit)

        self.btn_exit.clicked.connect(self.close)
        top_layout.addWidget(self.btn_exit)
        
        layout.addLayout(top_layout)
        layout.addSpacing(10)
        
        self.db = Database()
        self.products = self.db.get_products()
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        self.scroll_widget = QWidget()
        self.scroll_widget.setStyleSheet("background-color: transparent;")
        
        self.cards_layout = QVBoxLayout(self.scroll_widget)
        self.cards_layout.setSpacing(12)
        self.cards_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        for product in self.products:
            card_widget = create_card(product)
            self.cards_layout.addWidget(card_widget)
            
        self.scroll_area.setWidget(self.scroll_widget)
        layout.addWidget(self.scroll_area)
        self.setCentralWidget(central)

    def setup_role_interface(self):
        if self.role_id == 3:
            self.role_label.setText("Роль: Администратор")
            self.admin_button.setVisible(True)
            self.manager_button.setVisible(True)
            self.order_button.setVisible(False)
            self.btn_add_product.setVisible(True)
            
        elif self.role_id == 2:
            self.role_label.setText("Роль: Менеджер")
            self.manager_button.setVisible(True)
            self.admin_button.setVisible(False)
            self.order_button.setVisible(False)
            self.btn_add_product.setVisible(True)
            
        elif self.role_id == 1:
            self.role_label.setText("Роль: Клиент")
            self.order_button.setVisible(True)
            self.manager_button.setVisible(False)
            self.admin_button.setVisible(False)
            self.btn_add_product.setVisible(False)
            
        else:
            self.role_label.setText("Роль: Гость")
            self.order_button.setVisible(False)
            self.manager_button.setVisible(False)
            self.admin_button.setVisible(False)
            self.btn_add_product.setVisible(False)

    def logout_user(self):
        from login_window import LoginWindow
        # Создаем новый чистый объект базы данных с открытым пулом соединений
        new_db_instance = Database()
        # Передаем новую базу данных в открывающееся окно авторизации
        self.new_auth = LoginWindow(db=new_db_instance)
        self.new_auth.show()
        self.close()



    def closeEvent(self, event):
        self.db.close_all()
        event.accept()

if __name__ == "__main__":
    if sys.platform == 'win32':
        import ctypes
        myappid = 'mycompany.myproduct.subproduct.version'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    app = QApplication(sys.argv)
    
    from login_window import LoginWindow
    db_instance = Database()
    
    # Сохраняем ссылку в глобальную переменную, чтобы окно не закрывалось мгновенно
    global_auth_window = LoginWindow(db=db_instance)
    global_auth_window.show()
    
    sys.exit(app.exec())\


    