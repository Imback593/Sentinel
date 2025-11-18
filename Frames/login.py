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

# --- 2. СТОРІНКА: ЛОГІН ---

class LoginWidget(QWidget):
    """
    Віджет для сторінки входу.
    """
    # Сигнали, які ми надсилаємо головному вікну
    login_successful = Signal()
    go_to_signup = Signal()

    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(50, 50, 50, 50) # Додамо відступи
        
        form_layout = QFormLayout()
        
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password) # Приховує пароль

        form_layout.addRow("Логін:", self.username_input)
        form_layout.addRow("Пароль:", self.password_input)
        
        self.login_button = QPushButton("Увійти")
        self.goto_signup_button = QPushButton("Створити акаунт")
        self.goto_signup_button.setObjectName("goto_button") 

        layout.addLayout(form_layout)
        layout.addWidget(self.login_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.goto_signup_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)
        
        # Підключення кнопок до функцій
        self.login_button.clicked.connect(self.on_login_clicked)
        self.goto_signup_button.clicked.connect(self.go_to_signup)

    @Slot()
    def on_login_clicked(self):
        """
        !! ЦЕ МАКЕТ !!
        У реальному додатку тут була б перевірка на сервері.
        """
        username = self.username_input.text()
        password = self.password_input.text()
        
        # Симулюємо успішний вхід, якщо поля не порожні
        if username and password:
            print(f"Спроба входу з логіном: {username}")
            # Надсилаємо сигнал "успіх" головному вікну
            self.login_successful.emit()
        else:
            QMessageBox.warning(self, "Помилка", "Будь ласка, введіть логін та пароль.")