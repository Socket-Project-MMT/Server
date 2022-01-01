


import json
import requests



FORMAT="utf8"
URL="https://tygia.com/json.php"

data=requests.get(URL).text.encode().decode('utf-8-sig')

myobject=json.loads(data)

with open("data.json", "w+", encoding="utf-8") as file:
      file.seek(0)
      json.dump(myobject, file, indent=4)

