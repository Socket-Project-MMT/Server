import urllib.request

from json.decoder import JSONDecodeError
from json.encoder import JSONEncoder
import socket 
import threading
import json
import urllib.parse
import requests
import urllib
import codecs


FORMAT="utf8"
URL="https://tygia.com/json.php"

data=requests.get(URL).text.encode().decode('utf-8-sig')

myobject=json.loads(data)
print(type(myobject))
# print(myobject["rates"][0]["value"])
data1=myobject["rates"][0]["value"]
print(type(data1))
# print(data1)
# print(myobject)
# print("kkkk", data)





output_dict = [x for x in input_dict if x['type'] == '1']
with open("data.json", "w+", encoding="utf-8") as file:
      file.seek(0)
      json.dump(myobject, file, indent=4)

with open("data.json", "r") as openfile:
    # Reading from json file
    myobject1 = json.load(openfile)
print("k:", type(myobject1))
data2=myobject1["rates"][0]["value"]
print(type(data2))



from tkinter import *

OPTIONS = [
"Jan",
"Feb",
"Mar"
] #etc

master = Tk()

variable = StringVar(master)
variable.set(OPTIONS[0]) # default value

w = OptionMenu(master, variable, *OPTIONS)
w.pack()

mainloop()