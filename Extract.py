import string
import json
import os
import re

# Messages,  Files and other . . .
HISTORY_FILE_NOT_EXIST = "The technical code message file is not exist."
HISTORY_FILE_EMPTY = "The technical code message file is empty."
MAXIMUM_POPULAR_NUMBER = 5
POPULAR_FILE = "Popular.json"
HISTORY_FILE = "History.json"


# Extract technical codes function
def extract_technical_codes():
    if os.path.isfile(HISTORY_FILE):
        file = open(HISTORY_FILE, "r", encoding="utf-8")
        data = json.load(file)
        file.close()
        technical_codes = {}
        if data:
            for message in data["messages"]:
                text: str = message["text"]
                split_technical_code = {item.upper() for item in re.findall(r"\b[A-Za-z0-9]{10}\b", str(text).translate(str.maketrans("\n", " ", string.punctuation)))}
                for technical_code in split_technical_code:
                    if technical_code in technical_codes:
                        technical_code = technical_code.upper()
                        technical_codes[technical_code] += 1
                    else:
                        technical_codes[technical_code] = 1
            return dict(sorted({technical_code: number for technical_code, number in technical_codes.items() if number >= MAXIMUM_POPULAR_NUMBER}.items(), key=lambda x: x[1], reverse=True))
        else:
            return "empty_file"
    else:
        return "not_exist_file"


# Run the app
if __name__ == "__main__":
    data = extract_technical_codes()
    if data == "empty_file":
        print(HISTORY_FILE_EMPTY)
    elif data == "not_exist_file":
        print(HISTORY_FILE_NOT_EXIST)
    else:
        if "NNNNNNNNNN" in data.keys():
            data.pop("NNNNNNNNNN")
        file = open(POPULAR_FILE, "w")
        json.dump(data, file)
        file.close()
    os.system("PAUSE")
