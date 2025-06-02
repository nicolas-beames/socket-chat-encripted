import threading 
import socket 

port = 55555

hostName = socket.gethostname()
ipAdd = socket.gethostbyname(hostName)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ipAdd, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(message.decode('utf-8'))
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()

            nickname = nicknames[index]
            broadcast(f'{nickname} saiu do chat!'.encode('utf-8'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Conectado com as credenciais: {str(address)}")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nome do cliente: {nickname}!")
        broadcast(f'{nickname} entrou no chat!'.encode('utf-8'))
        client.send('Conectado ao servidor!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def server_input():
    while True:
        msg = input()
        broadcast(f'Servidor: {msg}'.encode('utf-8'))


print("Servidor ativo...")
print(f"IP - {ipAdd}")

input_thread = threading.Thread(target=server_input)
input_thread.start()

receive()
