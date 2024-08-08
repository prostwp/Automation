import socket

# Настройки
SOCKET_PATH = "/tmp/downloads_socket"

def list_files():
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.connect(SOCKET_PATH)
        client.sendall(b"LIST")
        response = client.recv(4096).decode("utf-8")
        print("Files in Downloads folder:\n", response)

def get_file(filename):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.connect(SOCKET_PATH)
        client.sendall(f"GET {filename}".encode("utf-8"))
        response = client.recv(4096)
        if response.startswith(b"File not found"):
            print("File not found")
        else:
            with open(filename, "wb") as f:
                f.write(response)
            print(f"File {filename} downloaded")

# Примеры использования
list_files()
get_file("pasted_text.txt")
