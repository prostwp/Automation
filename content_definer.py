from ErrorHandler import ErrorHandler


class Definer:
    def __init__(self):
        self.type = ""
        self.amount_of_horizontal_line = 0

    def defining_the_pattern_type(self, draw_element, decoded_json):
        ErrorHandler.validate_data(draw_element, dict)
        if draw_element['toolType'] == 'text':
            splited_draw_el = draw_element['settings']['text'].split()

            if splited_draw_el[0] in ("Ascending", "Descending"):
                self.type = "Canal"
            elif splited_draw_el[0] in ("Pennant", "Wedge", "Flag", "Double", "Head", "Rectangle", "Triangle"):
                self.type = "Chart"
            elif splited_draw_el[0] in ("Three", "Engulfing", "Hammer", "Evening", "Morning", "Marubozu", "Doji"):
                self.type = "Candlestick"
        if draw_element['toolType'] == 'horizontal_line':
            self.amount_of_horizontal_line += 1
            if self.amount_of_horizontal_line > 1:
                self.type = "SupRes"
