import socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 9090
BUFFER_SIZE = 1024

class me:
    def __init__(self,id):
        self.id=id

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_HOST, SERVER_PORT))

client_socket.send("hi".encode())

response = client_socket.recv(BUFFER_SIZE).decode()
print(f'Recieved response: {response}')
player=me(int(response))

while True:
    data = input('Enter data to send (or type "exit" to quit): ').strip()
    if data == 'exit':
        break
    client_socket.send(data.encode())

    response = client_socket.recv(BUFFER_SIZE)
    print(f'Recieved response: {response.decode()}')

client_socket.close()

