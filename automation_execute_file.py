import os
import platform
import requests
from html_decoder import Decoder
import ErrorHandler
from supres_execute import sup_res_exe
import general


def get_os_name():
    return platform.system()


def get_download_path():
    if os.name == 'nt':
        return os.path.join(os.environ['USERPROFILE'], 'Downloads')
    else:
        return os.path.join(os.path.expanduser('~'), 'Downloads')


def is_debugging_enabled(port=9222):
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


class FileManager:
    def __init__(self, path):
        self.path = path

    def file_exists(self):
        return os.path.exists(self.path) and os.path.getsize(self.path) > 0

    def read_file(self):
        with open(self.path, 'r') as file:
            return file.read()

    def delete_file(self):
        os.remove(self.path)


class DrawingProcessor:
    def __init__(self):
        self.amount_of_horizontal_line = 0

    def process_drawings(self, drawings, list_tf_datastate):
        for drawing in drawings:
            if drawing['toolType'] == 'horizontal_line':
                self.amount_of_horizontal_line += 1
                if self.amount_of_horizontal_line > 1:
                    sup_res_exe(drawings, list_tf_datastate[1])
                    break


class MainProcess:
    def __init__(self):
        self.os_name = get_os_name()
        self.download_path = get_download_path()
        self.file_path = os.path.join(self.download_path, 'pasted_text.txt')

    def run(self):
        if not is_debugging_enabled():
            ErrorHandler.raise_error("нет отладки")
        while True:
            file_manager = FileManager(self.file_path)
            if file_manager.file_exists():
                content = file_manager.read_file()
                decoded_cp_post = Decoder(content)
                list_tf_datastate = general.find_data_state_and_timeframe(content)
                try:
                    decoded_json = decoded_cp_post.decoding()
                    drawing_data = decoded_json['panels'][0]['drawings']
                    processor = DrawingProcessor()
                    processor.process_drawings(drawing_data, list_tf_datastate)
                except Exception:
                    ErrorHandler.raise_error("Невозможно декодировать файл")
                file_manager.delete_file()


if __name__ == "__main__":
    main_process = MainProcess()
    main_process.run()
