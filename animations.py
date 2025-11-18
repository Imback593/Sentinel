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