import os
import platform

os_name = platform.system()
if os_name == "Windows":
    file_path = 'C:\\Users\\dkarnachev\\Downloads\\pasted_text.txt'
else:
    file_path = '/Users/dkarnachev/Downloads/pasted_text.txt'
class ErrorHandler:

    def __init__(self):
        pass  # Конструктор может оставаться пустым, если не нужно инициализировать никаких переменных
    
    @staticmethod
    def validate_data( data, expected_type):
        if not isinstance(data, expected_type) or not data:
            raise TypeError(f"Provided data: {data} is not of type {expected_type.__name__} or is empty")

    @staticmethod
    def raise_error( message):
        if os.path.exists(file_path):
            os.remove(file_path)
        raise Exception(message)