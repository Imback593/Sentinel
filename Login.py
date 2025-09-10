from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget
from PyQt6.QtCore import QSize, Qt
from Client import client
import PyQt6.QtWidgets
import socket
import threading
import sys



class MainWindow(QMainWindow, client):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sentinel")
        
        self.btnlogin = QPushButton("login")
        self.ipline = QLineEdit()
        self.portline = QLineEdit()
        self.login = QLineEdit()
        self.password = QLineEdit()

        self.ipline.setPlaceholderText("Enter Ip")
        self.portline.setPlaceholderText("Enter Port")
        self.login.setPlaceholderText("Enter Login")
        self.password.setPlaceholderText("Enter Password")

        layout = QVBoxLayout()
        layout.addWidget(self.ipline)
        layout.addWidget(self.portline)
        layout.addWidget(self.login)
        layout.addWidget(self.password)
        layout.addWidget(self.btnlogin)
        

        container = QWidget()
        
        container.setLayout(layout)

        self.btnlogin.clicked.connect(self.btnauth)   
        
        self.setFixedSize(QSize(400, 600))

        self.setCentralWidget(container)


        
    
    def btnauth(self):
        try:
            client.connect(self.ipline.displayText(), self.portline.displayText())
            client.Login(self.login.displayText(), self.password.displayText())
        except:
            print("Error")            
            



application = QApplication([])

window = MainWindow()
window.show()

sys.exit(application.exec())