import platform
import time
from datetime import datetime, timedelta
import re
from pynput.keyboard import Key, Controller
import pyautogui
from sup_res_keys import keys
import ErrorHandler


def define_direction(draw_element):
    if draw_element['controls'][1]['y'] - draw_element['controls'][0]['y'] < 0:
        return "sell"
    elif draw_element['controls'][1]['y'] - draw_element['controls'][0]['y'] > 0:
        return "buy"
    else:
        raise Exception("Direction did not found")


def find_data_state_and_timeframe(content):
    try:
        data_state_match = re.search(r'data-symbol="([A-Z]{6})"', content)
        timeframe_match = re.search(r'data-timeframe="(60|300|900|1800|3600)"', content)
        if data_state_match and timeframe_match:
            currency_pair = data_state_match.group(1)
            data_state = currency_pair

            currency_timeframe = timeframe_match.group(1)
            timeframe = int(currency_timeframe) / 60
            return timeframe, data_state
        else:
            ErrorHandler.raise_error("Валютная пара или таймфрейм не найдены в файле")
    except Exception as e:
        ErrorHandler.raise_error(f"Ошибка при обработке файла: {e}")


class Writer:
    def __init__(self):
        self.keyboard = Controller()

    def toggle_bold(self):
        modifier_key = Key.ctrl if platform.system() == "Windows" else Key.cmd
        self.keyboard.press(modifier_key)
        self.keyboard.press('b')
        self.keyboard.release('b')
        self.keyboard.release(modifier_key)
        time.sleep(0.2)

    def write(self, text, interval=0.008, enter=True):
        for i in text:
            self.keyboard.press(i)
            self.keyboard.release(i)
            time.sleep(interval)
        if enter:
            pyautogui.press('enter')
        else:
            pyautogui.press('space')

    def write_bold(self, text):
        self.toggle_bold()
        time.sleep(0.1)
        self.write(text)
        time.sleep(0.1)
        self.toggle_bold()  # жирный шрифт почему-то выключается только если 2 раза метод вызвать
        self.toggle_bold()

    def is_friday(self):
        today = datetime.today()
        if today.weekday() == 4:
            Writer.write(keys["friday"][0])


class NewsChecker:
    def __init__(self, writer):
        self.writer = writer

    def news_checker(self):
        try:
            with open("news.txt", 'r') as file:
                content = file.readlines()
            if content and len(content) == 2:
                file_time = datetime.strptime(content[1], '%H:%M').time()
                current_time = datetime.now()
                threshold_time = datetime.combine(current_time.date(), file_time)
                time_difference = threshold_time - current_time
                if time_difference > timedelta(hours=1):
                    self.writer.write_bold(keys["fundamental_factors"][0])
                    self.writer.write(content[0])
                elif timedelta(0) <= time_difference <= timedelta(hours=1):
                    self.writer.write_bold(keys["fundamental_factors"][0])
                    self.writer.write(content[0].replace("hour", "minute"))
                else:
                    self.writer.write(keys["no_news"][0])
                    with open("news.txt", 'w'):
                        pass
            else:
                self.writer.write(keys["no_news"][0])
        except Exception:
            with open("news.txt", 'w'):
                pass

