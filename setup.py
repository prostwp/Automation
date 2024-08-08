import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["os", "platform", "html_decoder", "pynput", "webbrowser", "subprocess", "time", "pyautogui",
                 "datetime"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="auto",
    version="0.1",
    description="Your application description",
    options={"build_exe": build_exe_options},
    executables=[Executable("automation_execute_file.py", base=base)]
)
