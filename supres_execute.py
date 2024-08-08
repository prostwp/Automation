import requests
from general import NewsChecker, Writer
import general
from sup_res_keys import keys
import webbrowser
from datetime import datetime
import ErrorHandler
from sup_res_selenium import perform_action
import pyautogui
import time

writer = Writer()

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

    try:
        today_data = data['Time Series FX (Daily)'][current_date]
        today_open = float(today_data['1. open'])
        today_close = float(today_data['4. close'])
        change_percentage = ((today_close - today_open) / today_open) * 100
        return change_percentage
    except KeyError:
        return "Данные за текущий день еще недоступны."


def write_sup(sup_res_dict):
    count_of_sup = len(sup_res_dict['Support'])
    descending_order = sorted(sup_res_dict['Support'], reverse=True)
    key = keys['support'][count_of_sup - 1]
    for i in range(1, count_of_sup + 1):
        key = key.replace("sup" + str(i), descending_order[i - 1])
    return key


def write_res(sup_res_dict):
    count_of_sup = len(sup_res_dict['Resistance'])
    ascending_order = sorted(sup_res_dict['Resistance'])
    key = keys['resistance'][count_of_sup - 1]
    for i in range(1, count_of_sup + 1):
        key = key.replace("res" + str(i), ascending_order[i - 1])
    return key


def write_trend(datastate):
    global writer
    try:
        price_change = get_price_change_percentage(datastate, "SP5UT4AK12FE7ZEQ")
        if float(price_change) > 0.1:
            writer.write(keys['trend'][0])
        elif float(price_change) < -0.1:
            writer.write(keys['trend'][1])
        else:
            writer.write(keys['trend'][2])
    except Exception:
        writer.write(keys['trend'][2])


def write_support_resistance(direction, dict_sup_res):
    if direction == "buy":
        writer.write(write_sup(dict_sup_res) if len(dict_sup_res['Support']) > 0 else '')
        writer.write(keys["if_pair_rebound"][0])
        writer.write(write_res(dict_sup_res) if len(dict_sup_res['Resistance']) > 0 else '')

    elif direction == "sell":
        writer.write(write_sup(dict_sup_res) if len(dict_sup_res['Support']) > 0 else '')
        writer.write(write_res(dict_sup_res) if len(dict_sup_res['Resistance']) > 0 else '')
        writer.write(keys["if_pair_rebound"][1])


def processing_of_drawings(drawing_data, dict_sup_res):
    direction = None
    for drawing in drawing_data:
        if drawing['toolType'] == 'text':
            split_draw_el = drawing['settings']['text'].split()
            sup_res_dict_generator(split_draw_el, dict_sup_res)

        elif drawing['toolType'] == 'arrow_line':
            direction = general.define_direction(drawing)
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
                if dict_sup_res["Broke"][0] == "resistance":
                    file.write(keys["broke"][1].replace("1999", dict_sup_res["Broke"][1]))
                    file.write("\n")
                elif dict_sup_res["Broke"][0] == "support":
                    file.write(keys["broke"][0].replace("1999", dict_sup_res["Broke"][1]))
                    file.write("\n")
            if direction == "sell" and len(dict_sup_res["Support"]):
                file.write(keys["spare_title"][1].replace("1999", min(dict_sup_res["Resistance"])))
            elif direction == "buy":
                file.write(keys["spare_title"][1].replace("1999", max(dict_sup_res["Support"])))
            file.write("\n")
            file.write(keys["spare_title"][0].replace("1999", max(dict_sup_res["Support"])))
            file.write("\n")
            file.write(keys["spare_title"][2].replace("1999", min(dict_sup_res["Resistance"])))


def remove_comma(dict_sup_res):
    for sup in range(len(dict_sup_res["Support"])):
        if ',' in dict_sup_res["Support"][sup]:
            dict_sup_res["Support"][sup] = dict_sup_res["Support"][sup].replace(',', '')
    for sup in range(len(dict_sup_res["Resistance"])):
        if ',' in dict_sup_res["Resistance"][sup]:
            dict_sup_res["Resistance"][sup] = dict_sup_res["Resistance"][sup].replace(',', '')


def sup_res_exe(drawing_data, datastate):
    dict_sup_res = {"Support": [], "Resistance": [], "Broke": [None]}
    direction = processing_of_drawings(drawing_data, dict_sup_res)
    if direction is None:
        ErrorHandler.raise_error("Невозможно определить направление")

    remove_comma(dict_sup_res)

    url = 'https://cp.octafeed.com/panel/overview-posts/create'
    webbrowser.open_new_tab(url)

    time.sleep(5)
    pyautogui.press('enter')

    writer.write_bold(keys["general_outlook"][0])

    write_trend(datastate)

    write_support_resistance(direction, dict_sup_res, )

    checker = NewsChecker(writer)
    checker.news_checker()

    writer.is_friday()

    title = generate_main_title(dict_sup_res, direction)

    generate_spare_title(dict_sup_res, direction)

    perform_action(direction, title, datastate)
