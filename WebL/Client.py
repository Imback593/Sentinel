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
            DATA = SOCKET.recv(1024)
            decoded = DATA.decode()
            if decoded == "":
                pass
            else:
                print(f"\n[SERVER]: {decoded}")

    def sending():
        while 1==1:
            SOCKET.send(input("\nНапиши шо нибудь мне: ").encode())
        

    def Login(login, password):
        login.encode()
        password.encode()
        SOCKET.send(login, password)
            
    connect("147.185.221.21", 11474)
    threading.Thread(target=listening, args=()).start()
    threading.Thread(target=sending, args=()).start()


client()



       

