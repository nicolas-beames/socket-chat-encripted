import socket
import threading
import unicodedata
from typing import Callable

import caesar_cypher
import monoalphabetic
import playfair
import vigenere

DEBUG_MODE = False
PORT = 55555

CIPHERS: dict[int, tuple[str, Callable, Callable]] = {
    1: ("Sem Criptografia", lambda m, k: m, lambda m, k: m),
    2: ("Caesar", caesar_cypher.encrypt, caesar_cypher.decrypt),
    3: ("Monoalphabetic", monoalphabetic.encrypt, monoalphabetic.decrypt),
    4: ("Playfair", playfair.encrypt, playfair.decrypt),
    5: ("Vigenère", vigenere.Vigenere().encrypt, vigenere.Vigenere().decrypt),
}


def normalize_message(message: str) -> str:
    return "".join(
        c
        for c in unicodedata.normalize("NFKD", message.upper())
        if not unicodedata.combining(c)
    )


def choose_cipher() -> tuple[int, Callable, Callable]:
    print("Escolha uma cifra para criptografia:")
    for code, (name, *_) in CIPHERS.items():
        print(f"{code} - {name}")

    while True:
        try:
            option = int(input(""))
            _, encrypt, decrypt = CIPHERS[option]
            return option, encrypt, decrypt
        except ValueError:
            print("Digite uma opção válida.")


class ChatClient:
    def __init__(self):
        self.nickname = input("Digite seu username: ")
        option, self.encrypt, self.decrypt = choose_cipher()
        if option != 1:
            self.key = input("Digite a chave: ").upper()

        ip = input("IP (ou nome) do servidor: ")
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip, PORT))

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode("utf-8")
                print(message)
            except OSError:
                break

            if not message:
                break

            if message == "NICK":
                self.client.send(self.nickname.encode("utf-8"))
                continue

            sender, sep, payload = message.partition(":")
            if sep and payload.strip():
                try:
                    print(f"{sender}: {self.decrypt(payload.strip(), self.key)}")
                except Exception:
                    print(message)
            else:
                print(message)

        print("Conexão com o servidor encerrada.")

    def write(self):
        while True:
            try:
                message = input("")
            except EOFError:
                break

            if message.lower() == "/sair":
                try:
                    self.client.send(f"{self.nickname} saiu do chat.".encode("utf-8"))
                except OSError:
                    pass
                print("Você saiu do chat!")
                break

            normalized = normalize_message(message)
            encrypted = self.encrypt(normalized, self.key)
            try:
                self.client.send(f"{self.nickname}: {encrypted}".encode("utf-8"))
            except OSError:
                print("Falha ao enviar mensagem. Conexão perdida.")
                break

        self.client.close()

    def start(self):
        threading.Thread(target=self.receive, daemon=True).start()
        write_thread = threading.Thread(target=self.write, daemon=True)
        write_thread.start()

        try:
            write_thread.join()
        except KeyboardInterrupt:
            print("\nEncerrando client...")
        finally:
            self.client.close()


if __name__ == "__main__":
    ChatClient().start()
