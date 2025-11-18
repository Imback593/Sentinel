import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QTextEdit,
    QLineEdit, QPushButton, QListWidget,
    QLabel, QFormLayout, QStackedWidget,
    QMessageBox, QCheckBox, QSlider, QTabWidget,
    QGroupBox
)
from PySide6.QtCore import (
    Slot, Signal, Qt, QPropertyAnimation, QRect, 
    QPoint, QEasingCurve, QUrl
)
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtGui import QPainter

from QSS import main_qss
from Frames.signup import SignUpWidget
from Frames.login import LoginWidget
from Frames.settings_profile import SettingsProfileWidget
from Frames.chat import ChatClientWindow
from animations import AnimatedStackedWidget



# --- 7. ГОЛОВНИЙ КОНТРОЛЕР ВІКНА ---

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Мій Супер-Чат")
        self.setGeometry(100, 100, 700, 500)

        # *** ВИКОРИСТОВУЄМО AnimatedStackedWidget ***
        self.stack = AnimatedStackedWidget() 
        self.setCentralWidget(self.stack)

        # --- 1. Створюємо екземпляри наших сторінок ---
        self.login_page = LoginWidget()
        self.signup_page = SignUpWidget()
        self.chat_page = ChatClientWindow()
        self.settings_page = SettingsProfileWidget() # <-- НОВА СТОРІНКА

        # --- 2. Додаємо сторінки до "стопки" ---
        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.signup_page)
        self.stack.addWidget(self.chat_page)
        self.stack.addWidget(self.settings_page) # <-- ДОДАНО

        # --- 3. Підключення сигналів від сторінок до слотів контролера ---
        
        # Зі сторінки Логіну
        self.login_page.login_successful.connect(self.show_chat)
        self.login_page.go_to_signup.connect(self.show_signup)
        
        # Зі сторінки Реєстрації
        self.signup_page.signup_successful.connect(self.show_chat)
        self.signup_page.go_to_login.connect(self.show_login)
        
        # Зі сторінки Чату
        self.chat_page.go_to_settings.connect(self.show_settings)
        
        # Зі сторінки Налаштувань
        self.settings_page.go_to_chat.connect(self.show_chat)
        
        # --- 4. Підключення "наскрізних" налаштувань ---
        self.settings_page.sound_setting_changed.connect(
            self.chat_page.set_sound_enabled
        )

        # Початковий екран
        self.show_login()

    @Slot()
    def show_login(self):
        self.setWindowTitle("Вхід")
        self.stack.setAnimationDirection(Qt.LayoutDirection.RightToLeft) 
        self.stack.setCurrentWidget(self.login_page)
        self.setFixedSize(450, 300)

    @Slot()
    def show_signup(self):
        self.setWindowTitle("Реєстрація")
        self.stack.setAnimationDirection(Qt.LayoutDirection.LeftToRight) 
        self.stack.setCurrentWidget(self.signup_page)
        self.setFixedSize(450, 350) 

    @Slot()
    def show_chat(self):
        self.setWindowTitle("Мій Супер-Чат")
        self.stack.setCurrentWidget(self.chat_page) 
        self.setFixedSize(700, 500) 

    @Slot()
    def show_settings(self):
        self.setWindowTitle("Налаштування та Профіль")
        self.stack.setAnimationDirection(Qt.LayoutDirection.LeftToRight) 
        self.stack.setCurrentWidget(self.settings_page)
        self.setFixedSize(500, 400)


# --- 8. ТОЧКА ВХОДУ В ПРОГРАМУ ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # *** ЗАСТОСОВУЄМО СТИЛЬ ***
    app.setStyleSheet(main_qss.QSS_STYLE)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())