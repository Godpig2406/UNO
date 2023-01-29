import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP = "127.0.0.1"
PORT = 8080
server.bind((IP, PORT))
server.listen()

print(f"Server started at {IP}:{PORT}")

client1, address1 = server.accept()
print(f"Player 1 connected from {address1}")

client2, address2 = server.accept()
print(f"Player 2 connected from {address2}")

client1.send(b"You are Player 1")
client2.send(b"You are Player 2")

while True:
    client1_choice = client1.recv(1024).decode()
    client2_choice = client2.recv(1024).decode()
    
    if client1_choice == "rock" and client2_choice == "scissors":
        client1.send(b"You win")
        client2.send(b"You lose")
    elif client1_choice == "paper" and client2_choice == "rock":
        client1.send(b"You win")
        client2.send(b"You lose")
    elif client1_choice == "scissors" and client2_choice == "paper":
        client1.send(b"You win")
        client2.send(b"You lose")
    else:
        client1.send(b"Draw")
        client2.send(b"Draw")

server.close()
