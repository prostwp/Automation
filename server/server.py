import socket
import os

# Настройки
SOCKET_PATH = "/tmp/downloads_socket"
DOWNLOADS_DIR = os.path.expanduser("~/Downloads")

# Создание сокета
if os.path.exists(SOCKET_PATH):
    os.remove(SOCKET_PATH)

server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(SOCKET_PATH)
server.listen(1)

print(f"Сервер запущен и слушает сокет {SOCKET_PATH}")

while True:
    conn, _ = server.accept()
    try:
        # Получение команды от клиента
        command = conn.recv(1024).decode("utf-8")
        if command.startswith("LIST"):
            files = os.listdir(DOWNLOADS_DIR)
            response = "\n".join(files)
        elif command.startswith("GET"):
            filename = command.split(" ", 1)[1]
            filepath = os.path.join(DOWNLOADS_DIR, filename)
            if os.path.isfile(filepath):
                with open(filepath, "rb") as f:
                    response = f.read()
            else:
                response = b"File not found"
        else:
            response = b"Invalid command"

        conn.sendall(response)
    finally:
        conn.close()
