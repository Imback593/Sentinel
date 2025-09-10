import socket 
import threading

SOCKET = socket.socket()

class client():
    
    def connect(ip, port):
        CONNECTIP = ip
        PORT = port   
        SOCKET.connect((f"{CONNECTIP}", int(PORT)))
        print(f"[CLIENT] Connecting to {CONNECTIP}")
    
    def listening():
        while True:
            DATA = SOCKET.recv(1024).decode()
            print(f"[SERVER]: {DATA}")

    def Login(login, password):
        login.encode()
        password.encode()
        SOCKET.send(login, password)
            

    def start_messenger():
        thrlisten = threading.Thread(target=listening, args=())
        thrsending = threading.Thread(target=sending, args=())
        thrlisten.start()
        thrsending.start()


client()



       

