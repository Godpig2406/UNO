import socket

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(("127.0.0.1",9090))

def hi():
    data = "Hello Server!"
    clientSocket.send(data.encode())
    a=clientSocket.recv(1024).decode()
    if a == "Hello Client!":
        return True

def send():
    pass

def recieve():
    pass


hi()