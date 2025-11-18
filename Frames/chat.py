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

# --- 5. СТОРІНКА: ГОЛОВНИЙ ЧАТ ---

class ChatClientWindow(QWidget):
    """
    Головне вікно чату.
    ОНОВЛЕНО: 
    - Додано кнопку "Налаштування".
    - Додано відтворення звуку при відправці.
    """
    # Новий сигнал для переходу на сторінку налаштувань
    go_to_settings = Signal()
    
    def __init__(self):
        super().__init__()
        
        self.chat_histories = {
            "# Загальний": ["Ласкаво просимо до # Загальний!"],
            "@ Друг1": ["Ви почали приватний чат з @ Друг1."],
            "@ Друг2": ["Ви почали приватний чат з @ Друг2."]
        }
        self.current_chat = None

        # --- 1. Налаштування Звуку ---
        self.sound_enabled = True # За замовчуванням увімкнено
        self.message_sound = QSoundEffect()
        
        # ВАЖЛИВО: Створіть файл 'message_sent.wav' 
        # у тій же папці, що й скрипт!
        sound_file = QUrl.fromLocalFile("message_sent.wav")
        self.message_sound.setSource(sound_file)
        self.message_sound.setVolume(0.8) # Гучність 80%
        if self.message_sound.status() == QSoundEffect.Status.Error:
            print("Помилка: Не вдалося завантажити 'message_sent.wav'. Переконайтеся, що файл існує.")

        # --- 2. Створення інтерфейсу ---
        main_layout = QHBoxLayout(self)

        # Ліва колонка (змінена)
        left_layout = QVBoxLayout()
        self.contact_list = QListWidget()
        self.contact_list.addItems(self.chat_histories.keys())
        
        # НОВА КНОПКА "Налаштування"
        self.settings_button = QPushButton("⚙️ Налаштування")
        
        left_layout.addWidget(self.contact_list)
        left_layout.addWidget(self.settings_button)
        
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        left_widget.setMaximumWidth(180)
        main_layout.addWidget(left_widget)

        # Права колонка (без змін)
        chat_layout = QVBoxLayout()
        self.message_area = QTextEdit()
        self.message_area.setReadOnly(True)
        chat_layout.addWidget(self.message_area)

        input_layout = QHBoxLayout()
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Введіть ваше повідомлення...")
        self.send_button = QPushButton("Відправити")

        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_button)
        
        chat_layout.addLayout(input_layout)
        main_layout.addLayout(chat_layout)

        # --- 3. Підключення сигналів ---
        self.send_button.clicked.connect(self.on_send_message)
        self.message_input.returnPressed.connect(self.on_send_message)
        self.contact_list.currentItemChanged.connect(self.on_contact_selected)
        
        # НОВИЙ СИГНАЛ
        self.settings_button.clicked.connect(self.go_to_settings)

        # 4. Встановлюємо чат за замовчуванням
        self.contact_list.setCurrentRow(0)

    @Slot()
    def on_contact_selected(self, current_item):
        if not current_item:
            return
        chat_name = current_item.text()
        self.current_chat = chat_name
        
        self.message_area.clear()
        history = self.chat_histories.get(chat_name, [])
        for message in history:
            self.message_area.append(message)

    @Slot()
    def on_send_message(self):
        message_text = self.message_input.text().strip()
        
        if message_text and self.current_chat:
            formatted_message = f"Я: {message_text}"
            
            self.chat_histories[self.current_chat].append(formatted_message)
            self.add_message_to_chat(formatted_message)
            self.message_input.clear()
            
            # *** ВІДТВОРЕННЯ ЗВУКУ ***
            if self.sound_enabled:
                self.message_sound.play()

    def add_message_to_chat(self, message):
        self.message_area.append(message)

    # --- НОВІ СЛОТИ для керування налаштуваннями ---
    @Slot(bool)
    def set_sound_enabled(self, enabled):
        """
        Цей метод викликається з MainWindow, 
        щоб увімкнути/вимкнути звук.
        """
        print(f"Звук встановлено на: {enabled}")
        self.sound_enabled = enabled
        
    @Slot(int)
    def set_sound_volume(self, volume_percent):
        """
        (Ми не підключили це, але ось як це зробити)
        """
        # QSoundEffect очікує гучність від 0.0 до 1.0
        self.message_sound.setVolume(volume_percent / 100.0)



