import socket
import threading

nickname = input("Escolha um nome: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = input("IP do servidor:")
client.connect((ip, 55555))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            if client.fileno() == -1:
                break 
            print("Ocorreu um erro ao receber mensagem.")
            client.close()
            break

def write():
    while True:
        message = input("")
        if message.lower() == "/sair":
            client.send(f'{nickname} saiu do chat.'.encode('utf-8'))
            client.close()
            print("Você saiu do chat!")
            break
        else:
            client.send(f'{nickname}: {message}'.encode('utf-8'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

write_thread.join()
receive_thread.join()