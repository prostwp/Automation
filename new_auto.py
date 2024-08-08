import socket
import os
import platform
import time

import requests
from html_decoder import Decoder
from ErrorHandler import ErrorHandler
from chart_execute import chart_exe
from supres_execute import supres_exe
from candle_execute import candle_exe
import general
from pynput.keyboard import Controller
import subprocess

# Определите путь к сокету сервера
SOCKET_PATH = "/tmp/downloads_socket"

# Определите путь к файлу
def get_download_path():
    if os.name == 'nt':  # Для Windows
        return os.path.join(os.environ['USERPROFILE'], 'Downloads')
    else:
        return os.path.join(os.path.expanduser('~'), 'Downloads')

downloads_path = get_download_path()
file_path = os.path.join(downloads_path, 'pasted_text.txt')

amount_of_horizontal_line = 0
keyboard = Controller()

def is_chrome_debugging(port=9222):
    url = f"http://localhost:{port}/json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Chrome is running with debugging enabled on port", port)
            return True
        else:
            print("Chrome is not running on port", port)
            return False
    except requests.ConnectionError:
        print("No connection could be made to port", port)
        return False


def get_file_from_server(filename):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.connect(SOCKET_PATH)
        client.sendall(f"GET {filename}".encode("utf-8"))

        # Чтение данных из сокета
        file_data = bytearray()
        while True:
            chunk = client.recv(4096)
            if not chunk:
                break
            file_data.extend(chunk)

        if file_data.startswith(b"File not found"):
            print("File not found")
            return None
        return file_data


def delete_file_on_server(filename):
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.connect(SOCKET_PATH)
        client.sendall(f"DELETE {filename}".encode("utf-8"))
        response = client.recv(4096)
        if response.startswith(b"File not found"):
            print("File not found")
        else:
            print("File deleted")

if is_chrome_debugging():
    while True:
        print('Checking for file...')
        file_data = get_file_from_server('pasted_text.txt')
        if file_data:
            with open(file_path, 'wb') as file:
                file.write(file_data)
            print('Processing file...')
            try:
                with open(file_path, 'r') as file:
                    content = file.read()
                    decoded_cp_post = Decoder(content)
                    list_tf_datastate = general.ChartStateMethods.find_data_state_and_timeframe(content)

                decoded_json = decoded_cp_post.decoding(file_path)
                drawing_data = decoded_json['panels'][0]['drawings']

                for drawing in drawing_data:
                    if drawing['toolType'] == 'text':
                        split_draw_el = drawing['settings']['text'].split()
                        if split_draw_el[0] in (
                            "Three", "Engulfing", "Hammer", "Evening", "Morning", "Marubozu", "Doji"):
                            candle_exe(drawing_data, list_tf_datastate[0], list_tf_datastate[1], keyboard)
                            break
                        elif split_draw_el[0] in (
                            "Pennant", "Wedge", "Flag", "Double", "Head", "Rectangle", "Triangle"):
                            chart_exe(drawing_data, list_tf_datastate[0], list_tf_datastate[1], keyboard)
                            break
                        elif split_draw_el[0] in ("Ascending", "Descending"):
                            print("Canal")
                            break
                    elif drawing['toolType'] == 'horizontal_line':
                        amount_of_horizontal_line += 1
                        if amount_of_horizontal_line > 1:
                            supres_exe(drawing_data, list_tf_datastate[1], keyboard)
                            print("SupRes")
                            break
            except Exception:
                ErrorHandler.raise_error("Невозможно декодировать файл")

            delete_file_on_server('pasted_text.txt')
        else:
            print("Waiting for new file...")
        time.sleep(10)  # Пауза между попытками получения нового файла
