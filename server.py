import threading
import socket


host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    # checka se a lista de clientes está vazia
    # caso esteja, não há broadcast, apenas exibe
    # a mensagem para o Servidor
    print(message)
    # envia a mensagem para todos na lista de clientes
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                raise Exception(f'Usuário {client} desconectado!')
            if message.decode("utf-8").endswith("exit"):
                raise Exception(f'Usuário {client} saiu do chat!')
            broadcast(message)
            #print(message)
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast(f"{nickname.decode('utf-8')} saiu do chat ;-;".encode("ascii"))
                nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Conectado com {str(address)}")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Apelido: {nickname}!")
        broadcast(f'{nickname} entrou no chat!'.encode('utf-8'))
        client.send('Conectado!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

def write():
    while True:
        message = f'Server: {input("")}'
        broadcast(message.encode('utf-8'))
        #print(message)

print("Servidor operando!")

write_thread = threading.Thread(target=write)
write_thread.start()

try:
    receive()
except KeyboardInterrupt:
    print("Desligando...")
    broadcast("Servidor foi tirado do ar")
    for client in clients:
        client.close()
    server.close()
    print("Servidor offline")
