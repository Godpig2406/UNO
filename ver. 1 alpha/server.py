import socket
import threading

class port:
    def __init__(self, **property):
        self.id=dict()
        self.size=property["size"]
        self.address=property["address"]
        self.server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.address)

    def hello(self):
        self.recieve()

    def join(self):
        while True:
            conn, addr = self.server.accept()
            break
            

    def send(self,**message):
        pass

    def recieve(self):
        pass

engine=port(address=("127.0.0.1",9090),size=3)
engine.join()

