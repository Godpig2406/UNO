import socket, threading, interpreter
    
name=input("name: ")

client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 9090))

def verify(msg):
    readable=interpreter.translate(mode='decode',text=msg)
    if readable[0] == 'admin':
        if readable[1] == name or readable[1] =='everyone':
            if readable[2] == 'output':
                print(readable[3:])
            elif readable[2] == 'input':
                write(input(readable[3:]))

def receive():
    while True:
        try:
            msg = client.recv(1024).decode()
            if msg =="name":
                client.send(name.encode())
            else:
                verify(msg)

        except:
            print("error")
            client.close()
            break

def write(msg):
    while True:
        message = f'{name}: {msg}'
        client.send(message.encode())

receive_thread = threading.Thread(target=receive)
receive_thread.start()


