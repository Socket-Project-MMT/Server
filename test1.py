import json

with open("dataUsers.json", "r") as openfile:
    # Reading from json file
    HashTable = json.load(openfile)
username="dang"
if(username in HashTable):
        #connection.send(str.encode('Account existed'))
        print("f")
else: 
    print("t")

print(HashTable)