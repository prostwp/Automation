import os
from general import Writer, News
from ErrorHandler import ErrorHandler
import general
from chart_keys import keys
import webbrowser
import subprocess
from pynput.keyboard import Controller, Key
import requests
from datetime import datetime, timedelta

try:
    import pyautogui
except AssertionError:
    pass
import time

import platform

os_name = platform.system()
if os_name == "Windows":
    file_path = 'C:\\Users\\dkarnachev\\Downloads\\pasted_text.txt'
else:
    file_path = '/Users/dkarnachev/Downloads/chart_pasted_text.txt'


def write_pattern_trend(trend, direction, keyboard):
    if direction == 'buy':
        Writer.write(keys[trend][1], keyboard, enter=False)
    elif direction == 'sell':
        Writer.write(keys[trend][0], keyboard, enter=False)


def write_for_candle(chart_name, direction, keyboard):
    Writer.write(keys["display_pattern"][0].replace("Wedge", " ".join(chart_name)), keyboard, enter=False)

    if direction == "sell":
        Writer.write(keys["drop_rise"][0], keyboard)

    elif direction == "buy":
        Writer.write(keys["drop_rise"][1], keyboard)


def write_trend(timeframe, direction, candle_name, keyboard):
    if timeframe == 5 or timeframe == 15:
        write_pattern_trend("local_trend", direction, keyboard)
    else:
        write_pattern_trend("global_trend", direction, keyboard)
    write_for_candle(candle_name, direction, keyboard)


def processing_of_drawings(drawing_data):
    candle_name = None
    direction = None
    sup_res_flag = "0"
    for drawing in drawing_data:
        if drawing['toolType'] == 'text':
            split_draw_el = drawing['settings']['text'].split()
            if split_draw_el[0] in ("Three", "Engulfing", "Hammer", "Evening", "Morning", "Marubozu", "Doji"):
                candle_name = split_draw_el
            if "Resistance" in split_draw_el or "Support" in split_draw_el:
                sup_res_flag = "1"
        elif drawing['toolType'] == 'arrow_line':
            direction = general.ChartStateMethods.define_direction(drawing)
    return direction, candle_name, sup_res_flag


def candle_exe(drawing_data, timeframe, datastate, keyboard):
    direction, candle_name, sup_res_flag = processing_of_drawings(drawing_data)

    if candle_name is None or direction is None:
        ErrorHandler.raise_error("Невозможно определить направление или паттрен")

    url = 'https://cp.octafeed.com/panel/overview-posts/create'
    webbrowser.open_new_tab(url)

    time.sleep(5)
    pyautogui.press('enter')

    Writer.write_bold(keys["general_outlook"][0], keyboard)

    write_trend(timeframe, direction, candle_name, keyboard)

    News.news_checker(keyboard)

    Writer.is_friday(keyboard)
    print(sup_res_flag)
    subprocess.run(
        ["node", "candle_puppeteer_script.js", f"{direction}", f"{timeframe}", f"{datastate}",
         f"{" ".join(candle_name)}", f"{sup_res_flag}"])
