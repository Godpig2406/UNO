import socket
import threading

HEADER=64
PORT=5050
SERVER=socket.gethostbyname(socket.gethostname())
ADDR=(SERVER, PORT)
FORMAT="utf-8"
DISCONNECT_MSG="disconnect"
LIST=[]


server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)



def handle_client(conn, addr):
    print("New Player",addr)

    connected = True
    while connected:
        msg_length=conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length=int(msg_length)
            msg=conn.recv(msg_length).decode(FORMAT)
            if msg==DISCONNECT_MSG:
                connected = False
            print(addr,msg)
            conn.send("recieved".encode(FORMAT))
    
    conn.close()


def start():
    server.listen()
    print(SERVER)
    while True:
        conn, addr = server.accept()
        thread=threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print("active connection:",threading.active_count()-1)


print("Start Game")
start()
