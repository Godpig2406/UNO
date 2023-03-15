import socket
import threading
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9090
BUFFER_SIZE = 1024
joined=[]
size=3

class clients:
    def __init__(self,**details):
        self.address=details["address"]
        self.id=details["id"]

    def check(self,address):
        if self.address==address:
            return True


def handle_client(client_socket, client_address):
    print(f'New player from {client_address}')
    joined.append(clients(address=client_address, id=len(joined)))

    while len(joined) <= size:
        response = f"{len(joined)}"
        client_socket.send(response.upper().encode())
        while True:
                data = client_socket.recv(BUFFER_SIZE)


    print(f'Closed connection from {client_address}')
    client_socket.close()

    for i in joined:
        if i.address == client_address:
            joined.pop(joined.index(i))
            break
    else:
        print("error")


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(3)
    print("Started")
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

start_server()




