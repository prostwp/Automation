import os


def get_download_path():
    if os.name == 'nt':
        download_path = os.path.join(os.environ['USERPROFILE'], 'Downloads')
    else:
        download_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    return download_path


def validate_data(data, expected_type):
    if not isinstance(data, expected_type) or not data:
        raise TypeError(f"Provided data: {data} is not of type {expected_type.__name__} or is empty")


def raise_error(message):
    global file_path
    if os.path.exists(file_path):
        os.remove(file_path)
    raise Exception(message)


downloads_path = get_download_path()
file_path = os.path.join(downloads_path, 'pasted_text.txt')

