import requests

from general import ChartStateMethods, News, Writer
import general
import os
from sup_res_keys import keys
import webbrowser
import subprocess
from pynput.keyboard import Controller, Key
import pyautogui
import platform
from datetime import datetime, timedelta
from ErrorHandler import ErrorHandler

try:
    import pyautogui
except AssertionError:
    pass
import time

os_name = platform.system()
if os_name == "Windows":
    file_path = 'C:\\Users\\dkarnachev\\Downloads\\pasted_text.txt'
else:
    file_path = '/Users/dkarnachev/Downloads/pasted_text.txt'
keyboard = Controller()


def max_in_non_empty_list(lst):
    if lst:  # Проверяем, что список не пуст
        return max(lst)
    else:
        raise ValueError("Список не должен быть пустым")


def sup_res_dict_generator(split_draw_el, dict_sup_res):
    if "Weekly" in split_draw_el:
        split_draw_el.remove("Weekly")

    if split_draw_el[0] == "Broken":

        split_draw_el.remove("Broken")

        if split_draw_el[0] == "Support":
            dict_sup_res["Broke"] = ["support", split_draw_el[-1]]
            split_draw_el[0] = "Resistance"

        elif split_draw_el[0] == "Resistance":
            dict_sup_res["Broke"] = ["resistance", split_draw_el[-1]]
            split_draw_el[0] = "Support"

    if split_draw_el[0] == "Resistance":
        dict_sup_res["Resistance"].append(split_draw_el[-1])
    elif split_draw_el[0] == "Support":
        dict_sup_res["Support"].append(split_draw_el[-1])
    else:
        ErrorHandler.raise_error("Ошибка при генерации поддержки и сопротивления")
    return dict_sup_res


def get_price_change_percentage(symbol, api_key):
    url = f'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol={symbol[:3]}&to_symbol={symbol[3:]}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()

    current_date = datetime.now().strftime('%Y-%m-%d')

    # Получаем данные за текущий и предыдущий день
    try:
        today_data = data['Time Series FX (Daily)'][current_date]
        today_open = float(today_data['1. open'])
        today_close = float(today_data['4. close'])
        change_percentage = ((today_close - today_open) / today_open) * 100
        return change_percentage
    except KeyError:
        return "Данные за текущий день еще недоступны."


def wrire_sup(sup_res_dict):
    count_of_sup = len(sup_res_dict['Support'])
    descending_order = sorted(sup_res_dict['Support'], reverse=True)
    key = keys['support'][count_of_sup - 1]
    for i in range(1, count_of_sup + 1):
        key = key.replace("sup" + str(i), descending_order[i - 1])
    return key


def wrire_res(sup_res_dict):
    count_of_sup = len(sup_res_dict['Resistance'])
    ascending_order = sorted(sup_res_dict['Resistance'])
    key = keys['resistance'][count_of_sup - 1]
    for i in range(1, count_of_sup + 1):
        key = key.replace("res" + str(i), ascending_order[i - 1])
    return key


def write_trend(datastate, keyboard):
    try:
        price_change = get_price_change_percentage(datastate, "SP5UT4AK12FE7ZEQ")
        if float(price_change) > 0.1:
            Writer.write(keys['trend'][0], keyboard)
        elif float(price_change) < -0.1:
            Writer.write(keys['trend'][1], keyboard)
        else:
            Writer.write(keys['trend'][2], keyboard)
    except Exception:
        Writer.write(keys['trend'][0], keyboard)


def write_support_resistance(direction, dict_sup_res, keyboard):
    if direction == "buy":
        Writer.write(wrire_sup(dict_sup_res), keyboard) if len(dict_sup_res["Support"]) > 0 else time.sleep(0.1)
        Writer.write(keys["if_pair_rebound"][0], keyboard)
        Writer.write(wrire_res(dict_sup_res), keyboard) if len(dict_sup_res["Resistance"]) > 0 else time.sleep(0.1)

    elif direction == "sell":
        Writer.write(wrire_sup(dict_sup_res), keyboard) if len(dict_sup_res["Support"]) > 0 else time.sleep(0.1)
        Writer.write(wrire_res(dict_sup_res), keyboard) if len(dict_sup_res["Resistance"]) > 0 else time.sleep(0.1)
        Writer.write(keys["if_pair_rebound"][1], keyboard)


def processing_of_drawings(drawing_data, dict_sup_res):
    direction = None
    for drawing in drawing_data:
        if drawing['toolType'] == 'text':
            split_draw_el = drawing['settings']['text'].split()
            sup_res_dict_generator(split_draw_el, dict_sup_res)

        elif drawing['toolType'] == 'arrow_line':
            direction = general.ChartStateMethods.define_direction(drawing)
    print(dict_sup_res)
    return direction


def generate_main_title(dict_sup_res, direction):
    title = None
    if len(dict_sup_res["Support"]) > 0 and len(dict_sup_res["Resistance"]) > 0:
        title = keys["title"][0].replace("ren1", max(dict_sup_res["Support"])).replace("ren2",
                                                                                       min(dict_sup_res["Resistance"]))
    else:
        if direction == "buy" and len(dict_sup_res["Support"]) > 0:
            title = keys["broke"][1].replace("1999", max(dict_sup_res["Support"]))
        elif direction == "sell" and len(dict_sup_res["Resistance"]) > 0:
            title = keys["broke"][0].replace("1999", min(dict_sup_res["Resistance"]))
    if title is None:
        ErrorHandler.raise_error("Невозможно определить тайтл")
    return title

def generate_spare_title(dict_sup_res, direction):
    if len(dict_sup_res["Support"]) > 0 and len(dict_sup_res["Resistance"]) > 0:
        with open("variety.txt", "w") as file:
            if type(dict_sup_res["Broke"] is not None):
                if dict_sup_res["Broke"] == "resistance":
                    file.write(keys["broke"][1].replace("1999", dict_sup_res["Broke"][1]))
                    file.write("\n")
                elif dict_sup_res["Broke"] == "support":
                    file.write(keys["broke"][0].replace("1999", dict_sup_res["Broke"][1]))
                    file.write("\n")
            if direction == "sell" and len(dict_sup_res["Support"]):
                print(1)
                file.write(keys["bearish_title"][0].replace("1999", min(dict_sup_res["Resistance"])))
                file.write("\n")
                file.write(keys["bearish_title"][1].replace("1999", min(dict_sup_res["Resistance"])))
            elif direction == "buy":
                print(2)
                file.write(keys["bullish_title"][0].replace("1999", max(dict_sup_res["Support"])))
                file.write("\n")
                file.write(keys["bullish_title"][1].replace("1999", max(dict_sup_res["Support"])))

def supres_exe(drawing_data, datastate, keyboard):
    dict_sup_res = {"Support": [], "Resistance": [], "Broke": None}

    direction = processing_of_drawings(drawing_data, dict_sup_res)
    if direction is None:
        ErrorHandler.raise_error("Невозможно определить направление")

    url = 'https://cp.octafeed.com/panel/overview-posts/create'
    webbrowser.open_new_tab(url)

    time.sleep(5)
    pyautogui.press('enter')

    Writer.write_bold(keys["general_outlook"][0], keyboard)

    write_trend(datastate, keyboard)

    write_support_resistance(direction, dict_sup_res, keyboard)

    News.news_checker(keyboard)

    Writer.is_friday(keyboard)

    title = generate_main_title(dict_sup_res, direction)

    generate_spare_title(dict_sup_res, direction)

    subprocess.run(["node", "sup_res_puppeteer_script.js", f"{direction}", f"{title}", f"{datastate}"])

# supres_exe()
# print(generate_title({"Resistance": ["1000", "2000.00"], "Support": []}, 'sell'))

# while True:
#     if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
#
#         gen = keys["general_outlook"][0]
#         print(gen)
#         key = keys
#         # levels = SupResAutomation()
#         decoded_json = levels.decoding(file_path)
#         drawing_data = decoded_json['panels'][0]['drawings']
#         for drawing in drawing_data:
#             levels.sup_res_dict_generator(drawing)
#         if decoded_json:
#             url = 'https://cp.octafeed.com/panel/overview-posts/create'
#
#             webbrowser.open(url)
#
#             # handler = VKeyHandler()
#             # handler.wait_for_v_key()
#             time.sleep(5)
#
#             # toggle_bold()
#
#             pyautogui.press('enter')
#             #
#
#             # toggle_bold()
#             # write(key["general_outlook"][0])
#             write_bold(key["general_outlook"][0])
#             # time.sleep(0.2)
#             # toggle_bold()
#             # time.sleep(0.2)
#             print(levels.data_state)
#             # if levels.data_state != "BTCUSD" and levels.data_state != "XAUUSD" and levels.data_state != "USDCAD" and levels.data_state != "GBPJPY":
#
#             else:
#                 write(key['trend'][0])
#             # write(key['trend'][0])
#             if levels.direction == "buy":
#                 write(wrire_sup(levels.dict_sup_res)) if len(levels.dict_sup_res["Support"]) > 0 else time.sleep(0.1)
#                 write(key["if_pair_rebound"][0])
#                 write(wrire_res(levels.dict_sup_res)) if len(levels.dict_sup_res["Resistance"]) > 0 else time.sleep(0.1)
#
#             elif levels.direction == "sell":
#                 write(wrire_sup(levels.dict_sup_res)) if len(levels.dict_sup_res["Support"]) > 0 else time.sleep(0.1)
#                 write(wrire_res(levels.dict_sup_res)) if len(levels.dict_sup_res["Resistance"]) > 0 else time.sleep(0.1)
#                 write(key["if_pair_rebound"][1])
#
#             with open("news.txt", "r") as content:
#                 try:
#                     with open(file_path, 'r') as file:
#                         content = file.readlines()
#                     if content and len(content) == 2:
#                         file_time = datetime.strptime(content[1], '%H:%M').time()
#                         current_time = datetime.now()
#                         threshold_time = datetime.combine(current_time.date(), file_time)
#                         time_difference = threshold_time - current_time
#                         write_bold(key["fundamental_factors"][0])
#                         # write(key["fundamental_factors"][0])
#                         # toggle_bold()
#                         if time_difference > timedelta(hours=1):
#                             write(content[0])
#                         elif timedelta(0) <= time_difference <= timedelta(hours=1):
#                             write(content[0].replace("hour", "minute"))
#                         else:
#                             with open(file_path, 'w') as file:
#                                 pass
#                     else:
#                         write(key["no_news"][0])
#                 except FileNotFoundError:
#                     print("File not found.")
#             today = datetime.today()
#             if today.weekday() == 4:
#                 write(keys["friday"][0])
#             time.sleep(2)
#             print(f"{levels.direction}" == 'sell')
#             with open("range.txt", "w") as file:
#                 file.write(
#                     max(levels.dict_sup_res["Support"]) if len(levels.dict_sup_res["Support"]) > 0 else time.sleep(0.1))
#                 file.write("\n")
#                 file.write(min(levels.dict_sup_res["Resistance"]) if len(
#                     levels.dict_sup_res["Resistance"]) > 0 else time.sleep(0.1))
#             with open("variety.txt", "w") as file:
#                 if type(levels.broke_flag is list()):
#                     if levels.broke_flag[0] == "resistance":
#                         file.write(keys["broke"][1].replace("1999", levels.broke_flag[1]))
#                         file.write("\n")
#                     elif levels.broke_flag[0] == "support":
#                         file.write(keys["broke"][0].replace("1999", levels.broke_flag[1]))
#                         file.write("\n")
#                 if levels.direction == "sell":
#                     print(1)
#                     file.write(keys["bearish_title"][0].replace("1999", min(levels.dict_sup_res["Resistance"])))
#                     file.write("\n")
#                     file.write(keys["bearish_title"][1].replace("1999", min(levels.dict_sup_res["Resistance"])))
#                 elif levels.direction == "buy":
#                     print(2)
#                     file.write(keys["bullish_title"][0].replace("1999", max(levels.dict_sup_res["Support"]) if len(
#                         levels.dict_sup_res["Support"]) > 0 else time.sleep(
#                         0.1)))
#                     file.write("\n")
#                     file.write(keys["bullish_title"][1].replace("1999", max(levels.dict_sup_res["Support"])) if len(
#                         levels.dict_sup_res["Support"]) > 0 else time.sleep(0.1))
#             print(3)
#             subprocess.run(["node", "chart_puppeteer_script.js", f"{levels.direction}"])
#             print(4)
#         os.remove(file_path)
