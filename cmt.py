import requests


def is_chrome_debugging(port=9222):
    url = f"http://localhost:9222/json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Chrome is running with debugging enabled on port", port)
            return True
        else:
            print("Chrome is not running on port", port)
            return False
    except requests.ConnectionError:
        print("No connection could be made to port 111", port)
        return False

is_chrome_debugging()