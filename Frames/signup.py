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

# --- 2. СТОРІНКА: РЕЄСТРАЦІЇ ---

class SignUpWidget(QWidget):
    """
    Віджет для сторінки реєстрації.
    """
    signup_successful = Signal()
    go_to_login = Signal()

    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(50, 50, 50, 50)
        
        form_layout = QFormLayout()
        
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)

        form_layout.addRow("Вигадайте логін:", self.username_input)
        form_layout.addRow("Вигадайте пароль:", self.password_input)
        form_layout.addRow("Підтвердіть пароль:", self.confirm_password_input)
        
        self.signup_button = QPushButton("Зареєструватися")
        self.goto_login_button = QPushButton("Вже є акаунт? Увійти")
        self.goto_login_button.setObjectName("goto_button")

        layout.addLayout(form_layout)
        layout.addWidget(self.signup_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.goto_login_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)
        
        # Підключення
        self.signup_button.clicked.connect(self.on_signup_clicked)
        self.goto_login_button.clicked.connect(self.go_to_login)

    @Slot()
    def on_signup_clicked(self):
        """
        !! ЦЕ МАКЕТ !!
        Симулюємо успішну реєстрацію.
        """
        username = self.username_input.text()
        password = self.password_input.text()
        confirm = self.confirm_password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Помилка", "Поля не можуть бути порожніми.")
            return

        if password != confirm:
            QMessageBox.warning(self, "Помилка", "Паролі не збігаються.")
            return
        
        print(f"Створення акаунту для: {username}")
        # Надсилаємо сигнал "успіх" (що перекине нас на екран чату)
        self.signup_successful.emit()