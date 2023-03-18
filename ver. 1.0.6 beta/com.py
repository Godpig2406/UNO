import socket, threading

ADMINPASS="admin"
HOST = "127.0.0.1"
PORT =  9090
connected=dict()
class server:
    def __init__(self, **values):
        self.size = values["size"]
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((values["host"],values["port"]))
        self.server.listen()

    def broadcast(self, msg):
        for client in connected.keys():
                client.send(msg.encode())

    def handle(self, client):
        while True:
            try:
                msg=client.recv(1024)
                self.broadcast(msg.decode())
            except:
                client.close()
                name=connected[client]
                del connected[client]
                self.broadcast(f'{name} left!')
                break

    def recieve(self):
        while len(connected) < self.size+1:
            client, address = self.server.accept()
            print(f"connect {str(address)}")
            name=self.verify(client)
            if name != ADMINPASS:
                connected.update({client: name})
            self.broadcast(f"{name} joined")

            thread=threading.Thread(target=self.handle, args=(client,))
            thread.start()


    def verify(self, client):
        while True:
            client.send("name".encode())
            name=client.recv(1024).decode()
            return name


class infiltrate:
    def __init__(self, **values):
        self.name = ADMINPASS
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((values["host"], values["port"]))

    def receive(self):
        while True:
            try:
                msg = self.client.recv(1024).decode()
                if msg =="name":
                    self.client.send(self.name.encode())
                else:
                    print(msg)
            except:
                print("error")
                self.client.close()
                break

    def write(self,content):
        message = f'{self.name}: {content}'
        self.client.send(message.encode())


def start(size):
    game_server = server(size= size, host = HOST, port =PORT)
    game_thread = threading.Thread(target=game_server.recieve)
    game_thread.start()

    fake=infiltrate(host=HOST, port=PORT)
    fake_thread = threading.Thread(target=fake.receive)
    fake_thread.start()
    return fake