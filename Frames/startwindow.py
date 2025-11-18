import PySide6
import sys
from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QTextEdit, QLabel, QLayout, QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt, Slot, Signal, QPoint
from PySide6.QtGui import QPainter, QPixmap

QSS_STYLE = """
QMainWindow {
    background-color: #121F30

}
QVBoxLayout {
    color: #BDBDBD
}
QLabel {
    background-color: #6D6D6D
}




"""

class animation(QMainWindow):
    def __init__(self):
        super().__init__()
        title = "Sentinel"
        self.setWindowTitle(title)  

        hlayout = QHBoxLayout()
        vlayout = QVBoxLayout()

        mainwidget = QWidget()

        hlayout.setAlignment(Qt.AlignmentFlag.AlignCenter)


        midlogo = QLabel(self)
        mmap = QPixmap("sentinel_logo_m.png")
        midlogo.setPixmap(mmap)

        leftlogo = QLabel(self)
        lmap = QPixmap("sentinel_logo_l.png")
        leftlogo.setPixmap(lmap)

        rightlogo = QLabel(self)
        rmap = QPixmap("sentinel_logo_r.png")
        rightlogo.setPixmap(rmap)

        widgets_cont = [
            leftlogo,midlogo,rightlogo
        ]


        for i in widgets_cont:
            i.setFixedSize(200, 200)
            i.setScaledContents(True)
            hlayout.addWidget(i)
        

        mainwidget.setLayout(hlayout)
        self.setCentralWidget(mainwidget)
        self.setFixedSize(400, 600)
    pass
if __name__ == "__main__":
    start = QApplication(sys.argv)
    start.setStyleSheet(QSS_STYLE)

    window = animation()
    window.show()

    sys.exit(start.exec())