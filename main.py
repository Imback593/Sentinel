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

# --- 1. КОЛЬОРОВА ПАЛІТРА (QSS) ---
# #121F30 - Основний фон
# #1B3751 - Вторинний фон (поля вводу)
# #30B795 - Акцент (кнопки)
# #E0E0E0 - Текст (Додано для читабельності)
# -------------------------------------
QSS_STYLE = """
/* Загальний стиль для всіх віджетів */
QWidget {
    background-color: #121F30;
    color: #E0E0E0;
    font-family: Arial, sans-serif;
    font-size: 14px;
}

/* Окремо для головних вікон, щоб уникнути багів */
QMainWindow, QStackedWidget {
    background-color: #121F30;
}

/* Текст для лейблів (напр. "Логін:", "Пароль:") */
QLabel {
    color: #E0E0E0;
    padding-top: 5px; /* Невеликий відступ */
}

/* Поля вводу, чат-історія та список контактів */
QLineEdit, QTextEdit, QListWidget {
    background-color: #1B3751; /* Вторинний фон */
    color: #E0E0E0;
    border: 1px solid #30B795; /* Рамка кольору акценту */
    border-radius: 4px;
    padding: 5px;
}

/* Ефект при виборі поля вводу */
QLineEdit:focus, QTextEdit:focus {
    border: 1px solid #FFFFFF; /* Біла рамка при фокусі */
}

/* Забираємо яскраву рамку у вікна історії чату */
QTextEdit[readOnly="true"] {
    border-color: #1B3751;
}

/* Елементи списку контактів */
QListWidget::item {
    padding: 6px;
}
QListWidget::item:selected {
    background-color: #30B795; /* Фон акценту */
    color: #121F30; /* Темний текст */
}

/* Головні кнопки */
QPushButton {
    background-color: #30B795;
    color: #121F30; /* Темний текст на яскравій кнопці */
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: bold;
}

/* Ефект при наведенні */
QPushButton:hover {
    background-color: #38D3A8; /* Трохи світліший */
}

/* Ефект при натисканні */
QPushButton:pressed {
    background-color: #2BA080; /* Трохи темніший */
}

/*
   Окремий стиль для кнопок "Створити акаунт" / "Вже є акаунт?".
   Ми робимо їх схожими на посилання.
   Це працює завдяки 'setObjectName' у коді.
*/
QPushButton#goto_button {
    background-color: transparent; /* Прозорий фон */
    color: #30B795;
    font-weight: normal;
    text-decoration: underline;
}
QPushButton#goto_button:hover {
    color: #38D3A8;
}
"""

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

# --- 3. СТОРІНКА: РЕЄСТРАЦІЯ ---

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

# --- 6. КОМПОНЕНТ: АНІМОВАНИЙ STACKED WIDGET ---

class AnimatedStackedWidget(QStackedWidget):
    """
    QStackedWidget, який підтримує анімацію переходу між сторінками.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.animation_duration = 200 # Мілісекунди
        self.animation_type = QEasingCurve.Type.OutCubic # Тип кривої анімації
        self.animation_direction = Qt.LayoutDirection.RightToLeft # Типовий напрямок
        self._is_animating = False
        self._previous_index = 0 # Зберігаємо попередній індекс

    @Slot(int)
    @Slot(QWidget)
    def setCurrentIndex(self, index):
        """
        Перевизначаємо метод setCurrentIndex для додавання анімації.
        Можна передати індекс або об'єкт віджета.
        """
        if self._is_animating:
            return

        if isinstance(index, QWidget):
            new_widget = index
            index = self.indexOf(new_widget)
        else:
            new_widget = self.widget(index)

        old_index = self.currentIndex()
        if index == old_index or index < 0 or index >= self.count():
            super().setCurrentIndex(index)
            return

        self._previous_index = old_index
        old_widget = self.widget(old_index)
        
        # Визначаємо напрямок анімації
        if index > old_index:
            self.animation_direction = Qt.LayoutDirection.LeftToRight
        else:
            self.animation_direction = Qt.LayoutDirection.RightToLeft

        # Розміщуємо новий віджет так, щоб він виїжджав збоку
        # і встановлюємо його поверх старого
        new_widget.setGeometry(0, 0, self.width(), self.height())
        new_widget.raise_() 
        
        # Визначаємо початкову та кінцеву позицію нового віджета
        start_x = 0
        end_x = 0

        if self.animation_direction == Qt.LayoutDirection.LeftToRight:
            start_x = self.width() 
            end_x = 0
        else: # RightToLeft
            start_x = -self.width() 
            end_x = 0
        
        start_point = QPoint(start_x, 0)
        end_point = QPoint(end_x, 0)
        
        new_widget.move(start_point) 

        # Створюємо анімацію
        self.animation = QPropertyAnimation(new_widget, b"pos", self)
        self.animation.setDuration(self.animation_duration)
        self.animation.setEasingCurve(self.animation_type)
        self.animation.setStartValue(start_point)
        self.animation.setEndValue(end_point)
        
        self._is_animating = True
        self.animation.finished.connect(self._animation_finished)
        
        # Важливо: зміна індексу має відбутися *до* запуску анімації,
        # щоб QStackedWidget коректно оновив свій стан
        super().setCurrentIndex(index)
        
        self.animation.start()
        
    @Slot()
    def _animation_finished(self):
        """
        Слот, який викликається після завершення анімації.
        """
        self._is_animating = False
        # Переконайтеся, що старий віджет схований
        self.widget(self._previous_index).hide()
        self.widget(self._previous_index).move(0, 0)
        self.currentWidget().show()
        self.currentWidget().raise_()
        self.currentWidget().move(0, 0)

    def setAnimationDirection(self, direction):
        if direction in [Qt.LayoutDirection.LeftToRight, Qt.LayoutDirection.RightToLeft]:
            self.animation_direction = direction

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
    app.setStyleSheet(QSS_STYLE)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())