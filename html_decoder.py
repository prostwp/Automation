import base64
import json
import general
from ErrorHandler import raise_error


class Decoder:
    def __init__(self, content):
        self.content = content

    def decoding(self):
        try:
            general.find_data_state_and_timeframe(self.content)
            base64_str_index = self.content.find("base64,") + len("base64,")
            base64_str_end_index = self.content.find('"', base64_str_index)
            base64_image_str = self.content[base64_str_index:base64_str_end_index]

            image_data = base64.b64decode(base64_image_str)

            data_state_index = self.content.find('data-state="') + len('data-state="')
            data_state_end_index = self.content.find('"', data_state_index)
            data_state_str = self.content[data_state_index:data_state_end_index]

            data_state = base64.b64decode(data_state_str).decode('utf-8')
            json_data_state = json.loads(data_state)

            print("Файлы успешно декодированы и сохранены.")
            return json_data_state
        except Exception as e:
            raise_error(f"Ошибка при обработке файла: {e}")
