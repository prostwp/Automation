from html_decoder import Decoder
import os
import platform
from ErrorHandler import ErrorHandler
from chart_execute import chart_exe
from supres_execute import supres_exe
from candle_execute import candle_exe
import general
from pynput.keyboard import Controller
from pathlib import Path


# os_name = platform.system()
# if os_name == "Windows":
#     file_path = 'C:\\Users\\dkarnachev\\Downloads\\pasted_text.txt'
# else:
#     file_path = '/Users/dkarnachev/Downloads/pasted_text.txt'
def get_download_path():
    if os.name == 'nt':  # Для Windows
        download_path = os.path.join(os.environ['USERPROFILE'], 'Downloads')
    else:
        download_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    return download_path


downloads_path = get_download_path()
file_path = os.path.join(downloads_path, 'pasted_text.txt')

amount_of_horizontal_line = 0
keyboard = Controller()

while True:
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r') as file:
            content = file.read()
            decoded_cp_post = Decoder(content)
            list_tf_datastate = general.ChartStateMethods.find_data_state_and_timeframe(content)
        try:
            decoded_json = decoded_cp_post.decoding(file_path)
            drawing_data = decoded_json['panels'][0]['drawings']

            for drawing in drawing_data:
                if drawing['toolType'] == 'text':
                    split_draw_el = drawing['settings']['text'].split()
                    if split_draw_el[0] in ("Three", "Engulfing", "Hammer", "Evening", "Morning", "Marubozu", "Doji"):
                        candle_exe(drawing_data, list_tf_datastate[0], list_tf_datastate[1], keyboard)
                        break
                    elif split_draw_el[0] in ("Pennant", "Wedge", "Flag", "Double", "Head", "Rectangle", "Triangle"):
                        chart_exe(drawing_data, list_tf_datastate[0], list_tf_datastate[1], keyboard)
                        break
                    elif split_draw_el[0] in ("Three", "Engulfing", "Hammer", "Evening", "Morning", "Marubozu", "Doji"):
                        candle_exe(drawing_data, list_tf_datastate[0], list_tf_datastate[1], keyboard)
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
        os.remove(file_path)
