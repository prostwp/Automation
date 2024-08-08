import os

file_path = "~/Downloads/pasted_text.txt"

if os.path.exists(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        print("Content of the file:", content)
else:
    print(f"File {file_path} does not exist.")
