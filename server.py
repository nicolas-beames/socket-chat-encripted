import socket
import threading

PORT = 55555


class ChatServer:
    def __init__(self, port: int = PORT) -> None:
        self.port = port
        self.host_ip = socket.gethostbyname(socket.gethostname())

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host_ip, self.port))
        self.server.listen()

        self.clients: dict[socket.socket, str] = {}
        self.lock = threading.Lock()
        self.running = True

    def broadcast(self, message: bytes, exclude: socket.socket | None = None):
        print(message.decode("utf-8", errors="replace"))

        with self.lock:
            targets = list(self.clients.keys())

        for client in targets:
            if client is exclude:
                continue
            try:
                client.send(message)
            except OSError:
                self.disconnect(client, notify=False)

    def disconnect(self, client: socket.socket, notify: bool = True):
        with self.lock:
            nickname = self.clients.pop(client, None)

        if nickname is None:
            return

        try:
            client.close()
        except OSError:
            pass

        if notify:
            self.broadcast(f"{nickname} saiu do chat".encode("utf-8"))

    def handle(self, client: socket.socket):
        while self.running:
            try:
                message = client.recv(1024)
            except OSError:
                break

            if not message:
                break

            if message.decode("utf-8", errors="replace").strip().endswith("exit"):
                break

            self.broadcast(message)

        self.disconnect(client)

    def receive(self):
        while self.running:
            try:
                client, address = self.server.accept()
            except OSError:
                break

            print(f"Conectado com {address}")

            try:
                client.send("NICK".encode("utf-8"))
                nickname = client.recv(1024).decode("utf-8")
            except OSError:
                client.close()
                continue

            with self.lock:
                self.clients[client] = nickname

            print(f"Apelido: {nickname}")
            self.broadcast(
                f"{nickname} entrou no chat!".encode("utf-8"), exclude=client
            )
            client.send("Conectado!".encode("utf-8"))

            threading.Thread(target=self.handle, args=(client,), daemon=True).start()

    def write(self):
        while self.running:
            try:
                text = input("")
            except OSError:
                break
            self.broadcast(f"Server: {text}".encode("utf-8"))

    def shutdown(self):
        self.running = False
        self.broadcast("Servidor foi tirado do ar".encode("utf-8"))

        with self.lock:
            clients = list(self.clients.keys())
        for client in clients:
            client.close()

        self.server.close()
        print("Servidor offline")

    def start(self):
        print(f"Servidor operando em {self.host_ip}:{self.port}!")
        threading.Thread(target=self.write, daemon=True).start()

        try:
            self.receive()
        except KeyboardInterrupt:
            print("\nDesligando...")
        finally:
            # pass
            self.shutdown()


if __name__ == "__main__":
    ChatServer().start()
