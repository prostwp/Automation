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


def write_pattern_trend(trend, direction, chart_name, keyboard):
    if " ".join(chart_name) == "Pennant" and direction == 'buy':
        Writer.write(keys[trend][0], keyboard, enter=False)
    elif " ".join(chart_name) == "Pennant" and direction == 'sell':
        Writer.write(keys[trend][1], keyboard, enter=False)

    if " ".join(chart_name) == "Flag" and direction == 'buy':
        Writer.write(keys[trend][0], keyboard, enter=False)
    elif " ".join(chart_name) == "Flag" and direction == 'sell':
        Writer.write(keys[trend][1], keyboard, enter=False)

    if " ".join(chart_name) == "Double Top" and direction == 'sell':
        Writer.write(keys[trend][0], keyboard, enter=False)

    if " ".join(chart_name) == "Double Bottom" and direction == 'buy':
        Writer.write(keys[trend][1], keyboard, enter=False)

    if " ".join(chart_name) == "Head and Shoulders" and direction == 'sell':
        Writer.write(keys[trend][0], keyboard, enter=False)
    elif " ".join(chart_name) == "Head and Shoulders" and direction == 'buy':
        Writer.write(keys[trend][1], keyboard, enter=False)

    if " ".join(chart_name) == "Rectangle" and direction == 'sell':
        Writer.write(keys[trend][2], keyboard, enter=False)
    elif " ".join(chart_name) == "Rectangle" and direction == 'buy':
        Writer.write(keys[trend][2], keyboard, enter=False)

    if " ".join(chart_name) == "Triangle" and direction == 'sell':
        Writer.write(keys[trend][2], keyboard, enter=False)
    elif " ".join(chart_name) == "Triangle" and direction == 'buy':
        Writer.write(keys[trend][2], keyboard, enter=False)

    if " ".join(chart_name) == "Wedge" and direction == 'buy':
        Writer.write(keys[trend][1], keyboard, enter=False)
    elif " ".join(chart_name) == "Wedge" and direction == 'sell':
        Writer.write(keys[trend][0], keyboard, enter=False)


def chart_exe(drawing_data, timeframe, datastate, keyboard):
    split_draw_el = []
    direction, chart_name = None, None
    neckline = False
    for drawing in drawing_data:
        if drawing['toolType'] == 'text':
            split_draw_el = drawing['settings']['text'].split()
            if split_draw_el[0] in ("Pennant", "Wedge", "Flag", "Double", "Head", "Rectangle", "Triangle"):
                print(1)
                chart_name = split_draw_el
            if split_draw_el[0] in "Neckline":
                neckline = True
        elif drawing['toolType'] == 'arrow_line':
            direction = general.ChartStateMethods.define_direction(drawing)
    if chart_name is None or direction is None:
        ErrorHandler.raise_error("Невозможно определить направление или паттрен")

    url = 'https://cp.octafeed.com/panel/overview-posts/create'
    webbrowser.open_new_tab(url)

    time.sleep(5)
    pyautogui.press('enter')

    Writer.write_bold(keys["general_outlook"][0], keyboard)

    if timeframe == 1 or timeframe == 5:
        write_pattern_trend("local_trend", direction, chart_name, keyboard)
        print(2)
    else:
        write_pattern_trend("global_trend", direction, chart_name, keyboard)
    if chart_name[0] in ("Pennant", "Wedge", "Flag", "Rectangle", "Triangle"):
        write_with_rebound(direction, chart_name, keyboard)
        print(3)
    elif chart_name[0] in "Double":
        write_for_double_bottom_top(chart_name, neckline, keyboard)
    elif chart_name[0] in "Head":
        write_head_and_shoulders(chart_name, direction, keyboard)

    News.news_checker(keyboard)

    Writer.is_friday(keyboard)

    subprocess.run(
        ["node", "chart_puppeteer_script.js", f"{direction}", f"{timeframe}", f"{datastate}",
         f"{" ".join(chart_name)}"])


def write_with_rebound(direction, chart_name, keyboard):
    Writer.write(keys["display_pattern"][0].replace("Wedge", " ".join(chart_name)), keyboard)

    if direction == "sell":
        Writer.write(keys["sell_rebound"][0].replace("Wedge", " ".join(chart_name)), keyboard)

    elif direction == 'buy':
        Writer.write(keys["buy_rebound"][0].replace("Wedge", " ".join(chart_name)), keyboard)


def write_for_double_bottom_top(chart_name, neckline_status, keyboard):
    Writer.write(keys["display_pattern"][0].replace("Wedge", " ".join(chart_name)), keyboard, enter=False)

    if chart_name[1] == "Top":
        Writer.write(keys["drop_rise"][0], keyboard)
        if neckline_status:
            Writer.write(keys["neckline"][0], keyboard)

    elif chart_name[1] == "Bottom":
        Writer.write(keys["drop_rise"][1], keyboard)
        if neckline_status:
            Writer.write(keys["neckline"][1], keyboard)


def write_head_and_shoulders(chart_name, direction, keyboard):
    Writer.write(keys["display_pattern"][0].replace("Wedge", " ".join(chart_name)), keyboard)
    if direction == 'buy':
        Writer.write(keys["neckline"][1], keyboard)
    elif direction == 'sell':
        Writer.write(keys["neckline"][0], keyboard)

# while True:
#     if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
#
#         chart = ChartAutomation()
#         decoded_json = chart.decoding(file_path)
#         chart.find_data_state_and_timeframe()
#         print(chart.timeframe)
#         drawing_data = decoded_json['panels'][0]['drawings']
#         for drawing in drawing_data:
#             chart.defining_the_pattern_name(drawing)
#             chart.define_direction(drawing)
#         print(" ".join(chart.chart_name))
#         print(len(" ".join(chart.chart_name)))
#         # chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
#
#         if decoded_json:
#             url = 'https://cp.octafeed.com/panel/overview-posts/create'
#             webbrowser.open_new_tab(url)
#
#             time.sleep(5)
#
#             # toggle_bold()
#
#             pyautogui.press('enter')
#
#             write_bold(keys["general_outlook"][0])
#
#             if chart.timeframe == 1 or chart.timeframe == 5 and chart.chart_name[0]:
#                 write_pattern_trend("local_trend")
#             else:
#                 write_pattern_trend("global_trend")
#
#             if chart.chart_name[0] in ("Pennant", "Wedge", "Flag", "Rectangle", "Triangle"):
#                 write_with_rebound()
#             elif chart.chart_name[0] in "Double":
#                 write_for_double_bottom_top(chart.neckline_flag)
#             elif chart.chart_name[0] in "Head":
#                 write_head_and_shoulders()
#
#             with open("news.txt", "r") as content:
#                 try:
#                     with open("news.txt", 'r') as file:
#                         content = file.readlines()
#                     if content and len(content) == 2:
#                         file_time = datetime.strptime(content[1], '%H:%M').time()
#                         current_time = datetime.now()
#                         threshold_time = datetime.combine(current_time.date(), file_time)
#                         time_difference = threshold_time - current_time
#                         write_bold(keys["fundamental_factors"][0])
#
#                         # toggle_bold()
#                         if time_difference > timedelta(hours=1):
#                             write(content[0])
#                         elif timedelta(0) <= time_difference <= timedelta(hours=1):
#                             write(content[0].replace("hour", "minute"))
#                         else:
#                             with open("news.txt", 'w') as file:
#                                 pass
#                     else:
#                         write(keys["no_news"][0])
#                 except FileNotFoundError:
#                     print("File not found.")
#             today = datetime.today()
#             if today.weekday() == 4:
#                 write(keys["friday"][0])
#
#             print(chart.data_state)
#             subprocess.run(
#                 ["node", "chart_puppeteer_script.js", f"{chart.direction}", f"{chart.timeframe}", f"{chart.data_state}",
#                  f"{" ".join(chart.chart_name)}"])
#         os.remove(file_path)