import socket, threading, interpreter
    
name=input("name: ")

client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 9090))

def receive():
    while True:
        try:
            msg = client.recv(1024).decode()
            if msg =="name":
                client.send(name.encode())
            else:
                print(msg)
        except:
            print("error")
            client.close()
            break

def write():
    while True:
        message = f'{name}: {input("")}'
        client.send(message.encode())

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
