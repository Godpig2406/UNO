import socket

HEADER=64
FORMAT="utf-8"
PORT=5050
DISCONNECT_MSG="disconnect"
SERVER="192.168.0.22"
ADDR=(SERVER,PORT)

client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def request(message):
    print(message)

def send(msg):
    message=msg.encode(FORMAT)
    msg_length=len(message)
    send_length=str(msg_length).encode(FORMAT)
    send_length += b" " *(HEADER-len(send_length))
    client.send(send_length)
    client.send(message)
    request(client.recv(64).decode(FORMAT))

send("hello world!")
send("world!")
send("gospig")

send(DISCONNECT_MSG)