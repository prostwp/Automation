import platform
import time
from datetime import datetime
import re
import requests
from pynput.keyboard import Key
import pyautogui
from chart_keys import keys
from datetime import datetime, timedelta
from ErrorHandler import ErrorHandler


class ChartStateMethods:
    def __init__(self):
        self.timeframe = 0
        self.direction = ''
        self.data_state = ''
        self.broke_flag = [1]
        self.chart_name = ''
        self.neckline_flag = None
        self.content = ''

    @staticmethod
    def define_direction(draw_element):
        if draw_element['controls'][1]['y'] - draw_element['controls'][0]['y'] < 0:
            direction = "sell"
        elif draw_element['controls'][1]['y'] - draw_element['controls'][0]['y'] > 0:
            direction = "buy"
        else:
            raise Exception("Direction did not found")
        return direction

    @staticmethod
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
    @staticmethod
    def toggle_bold(keyboard):
        modifier_key = Key.ctrl if platform.system() == "Windows" else Key.cmd
        keyboard.press(modifier_key)
        keyboard.press('b')
        keyboard.release('b')
        keyboard.release(modifier_key)
        time.sleep(0.2)

    @staticmethod
    def write(text, keyboard, interval=0.00001, enter=True):
        for i in text:
            keyboard.press(i)
            keyboard.release(i)
            time.sleep(interval)
        if enter:
            pyautogui.press('enter')
        else:
            pyautogui.press('space')

    @staticmethod
    def write_bold(text, keyboard):
        Writer.toggle_bold(keyboard)  # Включаем жирный
        time.sleep(0.1)
        Writer.write(text, keyboard)  # Пишем текст
        time.sleep(0.1)
        Writer.toggle_bold(keyboard)  # Выключаем жирный
        Writer.toggle_bold(keyboard)  # Выключаем жирный

    @staticmethod
    def is_friday(keyboard):
        today = datetime.today()
        if today.weekday() == 4:
            Writer.write(keys["friday"][0], keyboard)


class News:
    @staticmethod
    def news_checker(keyboard):
        try:
            with open("news.txt", 'r') as file:
                content = file.readlines()
            if content and len(content) == 2:
                file_time = datetime.strptime(content[1], '%H:%M').time()
                current_time = datetime.now()
                threshold_time = datetime.combine(current_time.date(), file_time)
                time_difference = threshold_time - current_time
                if time_difference > timedelta(hours=1):
                    Writer.write_bold(keys["fundamental_factors"][0], keyboard)
                    Writer.write(content[0], keyboard)
                elif timedelta(0) <= time_difference <= timedelta(hours=1):
                    Writer.write_bold(keys["fundamental_factors"][0], keyboard)
                    Writer.write(content[0].replace("hour", "minute"), keyboard)
                else:
                    Writer.write(keys["no_news"][0], keyboard)
                    with open("news.txt", 'w'):
                        pass
            else:
                Writer.write(keys["no_news"][0], keyboard)
        except Exception:
            with open("news.txt", 'w'):
                pass
