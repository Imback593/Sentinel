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

# --- 4. СТОРІНКА: НАЛАШТУВАННЯ ТА ПРОФІЛЬ ---

class SettingsProfileWidget(QWidget):
    """
    Нова сторінка для налаштувань та профілю.
    Використовує QTabWidget для організації.
    """
    # Сигнал для повернення в чат
    go_to_chat = Signal()
    
    # Сигнал для зміни налаштувань звуку
    sound_setting_changed = Signal(bool)

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout(self)
        
        # Створюємо вкладки
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # --- Вкладка 1: Профіль ---
        self.profile_tab = QWidget()
        profile_layout = QVBoxLayout(self.profile_tab)
        
        profile_group = QGroupBox("Ваш Профіль")
        form_layout = QFormLayout()
        
        self.username_input = QLineEdit("Ваш_Логін")
        self.email_input = QLineEdit("user@example.com")
        self.email_input.setReadOnly(True) # Email нібито не можна змінити
        
        form_layout.addRow("Ім'я користувача:", self.username_input)
        form_layout.addRow("Email:", self.email_input)
        
        self.avatar_button = QPushButton("Змінити аватар (Макет)")
        
        profile_group.setLayout(form_layout)
        profile_layout.addWidget(profile_group)
        profile_layout.addWidget(self.avatar_button)
        profile_layout.addStretch()

        # --- Вкладка 2: Налаштування ---
        self.settings_tab = QWidget()
        settings_layout = QVBoxLayout(self.settings_tab)
        
        sound_group = QGroupBox("Налаштування звуку")
        sound_layout = QVBoxLayout(sound_group)
        
        self.sound_checkbox = QCheckBox("Увімкнути звуки повідомлень")
        self.sound_checkbox.setChecked(True)
        
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setValue(80)
        
        sound_layout.addWidget(self.sound_checkbox)
        sound_layout.addWidget(QLabel("Гучність:"))
        sound_layout.addWidget(self.volume_slider)
        
        settings_layout.addWidget(sound_group)
        settings_layout.addStretch()

        # Додаємо вкладки до менеджера
        self.tabs.addTab(self.profile_tab, "Профіль")
        self.tabs.addTab(self.settings_tab, "Налаштування")

        # --- Кнопки Збереження / Повернення ---
        button_layout = QHBoxLayout()
        button_layout.addStretch() # Відступ
        self.save_button = QPushButton("Зберегти та Повернутись")
        button_layout.addWidget(self.save_button)
        
        main_layout.addLayout(button_layout)
        
        # --- Підключення сигналів ---
        self.save_button.clicked.connect(self.on_save_and_return)
        self.sound_checkbox.stateChanged.connect(self.on_sound_check_changed)

    @Slot()
    def on_save_and_return(self):
        """
        Тут має бути логіка збереження (на сервер).
        Поки що просто повертаємось у чат.
        """
        print("Налаштування збережено (симуляція).")
        # Повідомляємо головне вікно, що треба повернутись у чат
        self.go_to_chat.emit()

    @Slot(int)
    def on_sound_check_changed(self, state):
        """
        Повідомляємо головне вікно про зміну налаштування звуку.
        """
        is_enabled = state == Qt.CheckState.Checked.value
        self.sound_setting_changed.emit(is_enabled)