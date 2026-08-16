import socket
import threading
import unicodedata
from types import FunctionType

import caesar_cypher
import monoalphabetic
import playfair
import vigenere

nickname = input("Escolha um nome: ")

nickname = input("Digite seu username: ")

print("Escolha uma cifra para criptografia:")
print("1 - Sem Criptografia")

cifras = ["Caesar", "Monoalphabetic", "Playfair", "Vigenère"]

for i, cifra in enumerate(cifras):
    print(f"{i + 2} - {cifra}")

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
        encrypt_method = monoalphabetic.encrypt
        decrypt_method = monoalphabetic.decrypt
    case 4:
        encrypt_method = playfair.encrypt
        decrypt_method = playfair.decrypt
    case 5:
        encrypt_method = vigenere.encrypt
        decrypt_method = vigenere.decrypt

key = input("insert the key: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = input("IP do servidor:")

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
                msg = message.split(":", 1)
                if len(msg) > 1:
                    print(f"{msg[0]}: {decrypt_method(msg[1].strip(), key)}")
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
            message = normalize_message(message)
            message = encrypt_method(message, key)
            client.send(f"{nickname}: {message}".encode("utf-8"))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

write_thread.join()
receive_thread.join()
