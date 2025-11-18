
class main_qss():
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