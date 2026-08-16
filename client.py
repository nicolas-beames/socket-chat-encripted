import socket
import threading
import unicodedata
from types import FunctionType

import caesar_cypher

nickname = input("Escolha um nome: ")

nickname = input("Digite seu username: ")

print("Escolha uma cifra para criptografia:")
print("1 - Sem Criptografia")
print("2 - Cifra de César")
print("3 - Cifra Monoalfabética")
print("4 - Cifra de Playfair")
print("5 - Cifra de Vigenère")


selected_cipher = int(input(""))

encrypt_method: FunctionType
decrypt_method: FunctionType

match selected_cipher:
    case 1:
        # Sem criptografia
        print("Sem Criptografia")
    case 2:
        encrypt_method = caesar_cypher.encrypt
        decrypt_method = caesar_cypher.decrypt
    case 3:
        print("Cifra Monoalfabética")
    case 4:
        encrypt_method = playfair.encrypt
        decrypt_method = playfair.decrypt
    case 5:
        # Cifra de Vigenère

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = input("IP do servidor:")

cifras = ["caesar", 'monoalphabetic', "playfair", "vigenere"]

for cifra in cifras:
    print(cifra)

cypher = input("Qual cifra gostaria de usar?")
key = input("insert the key")

client.connect((ip, 55555))


def normalize_message(message: str):
    return "".join(
        [
            c
            for c in unicodedata.normalize("NFKD", message.upper())
            if not unicodedata.combining(c)
        ]
    )


def receive():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "NICK":
                client.send(nickname.encode("utf-8"))
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
            client.send(f"{nickname} saiu do chat.".encode("utf-8"))
            client.close()
            print("Você saiu do chat!")
            break
        else:
            client.send(f"{nickname}: {message}".encode("utf-8"))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

write_thread.join()
receive_thread.join()

