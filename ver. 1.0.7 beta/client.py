import socket, threading, interpreter
    
name=input("name: ")

client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 9090))

def verify(msg):
    readable=interpreter.translate(mode='decode',text=msg)
    match readable[0]:
        case 'admin':
            if readable[1] == name or readable[1] =='everyone':
                if readable[2] == 'win':
                    print(readable[3:])
                elif readable[2] == 'color':
                    a=pickcolor(readable[1:])
                    write(f'color: {a}')




def pickcolor(msg):
    print(len(msg))
    a=f'{input(msg)}'
    return a

def receive():
    while True:
        try:
            msg = client.recv(1024).decode()
            if msg =="name":
                client.send(name.encode())
                print('sent')
            else:
                try:
                    verify(msg)
                except:
                    print("Verify")

        except:
            print("error")
            client.close()
            break

def write(msg):
    message = f'{name}: {msg}'
    client.send(message.encode())

receive_thread = threading.Thread(target=receive)
receive_thread.start()

