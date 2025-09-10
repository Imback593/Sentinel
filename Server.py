import socket 
import threading

UDATA = {
    "ip" : "127.0.0.1",
    "port" : "1080",
    "login" : "Xdev",
    "password" : "1236"
}

SOCK = socket.socket()
SOCK.bind(("127.0.0.1", 1080))
SOCK.listen(1)
connection, address = SOCK.accept()

def datalisten():
    while True:
        DATA = connection.recv(2048)
        DATA.decode()
        print(f"{address}: {DATA}")

def startserver():
    thr = threading.Thread(target=datalisten, args=())
    thr.start()

def login():
    DATA = connection.recv(512)
    DATA.decode()
    print(DATA)
    if DATA == UDATA:
        startserver()
    else: 
        pass
        
datalisten()