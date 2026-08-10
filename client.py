import socket
import threading


class CaesarCypher:

    max_value = 1114111

    @staticmethod
    def encrypt(msg: str, key: int) -> str:
        ascii_msg = list(map(ord, msg))
        ascii_msg = list(map(lambda x: (x + key) % CaesarCypher.max_value, ascii_msg))
        msg = "".join(map(chr, ascii_msg))
        return msg

    @staticmethod
    def decrypt(msg: str, key: int) -> str:
        ascii_msg = list(map(ord, msg))
        ascii_msg = list(map(lambda x: (x - key) % CaesarCypher.max_value, ascii_msg))
        msg = "".join(map(chr, ascii_msg))
        return msg


nickname = input("Escolha um nome: ")

nickname = input("Digite seu username: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = input("IP do servidor:")
client.connect((ip, 3000))

encryption_key = input("Chave de criptografia: ")

print(ip)


def receive():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "NICK":
                client.send(nickname.encode("utf-8"))
            else:
                sender = message.split(":")[0]
                decrypted_msg = CaesarCypher.decrypt(
                    message.split(" ", maxsplit=1)[1], int(encryption_key)
                )
                print(f"{sender}: {decrypted_msg}")
                # print(message)
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
            encrypted_msg = CaesarCypher.encrypt(message, int(encryption_key))
            client.send(f"{nickname}: {encrypted_msg}".encode("utf-8"))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

write_thread.join()
receive_thread.join()
