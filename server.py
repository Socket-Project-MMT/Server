# fileserver.py

import socket
import threading
import json
from typing import Hashable
import urllib.parse
import requests
import urllib

from tkinter import *
from tkinter import messagebox
import tkinter

HOST = "127.0.0.1"
port = 6767
MAX_CLIENT=100
FORMAT = "utf-8"
URL = "https://tygia.com/json.php"
# Ngày
data = "20213112"

FORMAT = "utf8"
URL = "https://tygia.com/json.php"

data = requests.get(URL).text.encode().decode('utf-8-sig')

myobject = json.loads(data)

with open("data.json", "w+", encoding="utf-8") as file:
    file.seek(0)
    json.dump(myobject, file, indent=4)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, port))
s.listen()

ipClientlist = []
dates = []
with open("data.json", "r") as openfile:
    # Reading from json file
    datafile = json.load(openfile)
# list theo gold
values = datafile["golds"]
# loc mot gia tri theo tri so co dieu kien


searchlist = []
# namelist la ten brand co dinh

namelist = []
SJC = []
array = []
# loc het danh sach theo tri so, co mot dieu kien
for entry in datafile["golds"]:
    if(entry["date"] == "20211231"):
        array.append(entry["value"])
        for entr in entry["value"]:
            if(entr["type"] == "SJC"):
                namelist.append(entr["brand"])


for entry in datafile["golds"]:
    dates.append(entry["date"])


with open("dataUsers.json", "r") as openfile:
    # Reading from json file
    HashTable = json.load(openfile)
nClient = 0
window = Tk()
window.title('Server - GOLD EXCHANGE RATE LOOOKUP')
window.geometry('330x450')
window.resizable(0, 0)

def Quit():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            # ngat kết nối client
            #client.close()
            messagebox.showinfo('Announce', 'Disconnected from ALL Clients.')
            window.destroy()

def Refresh():
    #update size và arr
    number.config(text = size)
    for i in arr:
        list.insert(END, i)

def Suspend():
    if messagebox.askokcancel("Quit", "Do you want to suspend?"):
        # ngat kết nối client
        # client.close()
        messagebox.showinfo('Announce', 'Disconnected from ALL Clients.')

        size = 0
        number.config(text = size)
        list.delete(0, END)

        win = Frame(window)
        win.pack(fill='both', expand=True)
        #win.place(x = 0, y = 400)

        def Reactivate():
            # Mở lại socket
            win.destroy()

        Button(win, width = 8, height = 2, bd = 0, bg = 'coral', fg = 'white', text = 'Reactivate', command =  Reactivate).place(relx=0.5, rely=0.5, anchor=CENTER)
size = 0
arr=('1', '2', '2')
def recvList(conn):
    mylist = []
    item = conn.recv(1024).decode(FORMAT)
    while(item != "end"):
        mylist.append(item)
        conn.sendall(item.encode(FORMAT))
        item = conn.recv(1024).decode(FORMAT)

    return mylist


def sendList(conn, list):
    for item in list:
        conn.sendall(item.encode(FORMAT))
        msg = conn.recv(1024).decode(FORMAT)
    msg = "end"
    conn.sendall(msg.encode(FORMAT))


def checkClientSignUp(username):
    if(username in HashTable):
        #connection.send(str.encode('Account existed'))
        print("false")
        return False
    else:
        print("true")
        return True


def checkClientLogIn(username, password):
    if username not in HashTable:
      return False
    else: 
      if(HashTable[username] == password):
          return True
      return False


def clientSignUp(username, password):
    global HashTable
    try:
        if(checkClientSignUp(username) == False):
            return False
        else:
            HashTable[username] = password
            print(HashTable[username])
            print('Registered : ', username)

            # write users infor to file
            infor = {
                username: password
            }

            with open("dataUsers.json", "r+") as file:
                data = json.load(file)
                data.update(infor)
                file.seek(0)
                json.dump(data, file, indent=4)
            return True

    except:
        print("Error")


def clientLogIn(username, password):

    if(checkClientLogIn(username, password) == False):
        # Response code for login failed
        print('Connection denied : ', username)
        return False
    else:
        # Response Code for Connected Client
        print('Connected : ', username)
        return True


def Search(conn):

    global namelist
    global dates
    sendList(conn, namelist)
    nameBrand=[]
    sendList(conn, dates)
    global datafile
    infor = ["", ""]
    infor = recvList(conn)
    response = ["", ""]
    for entry in datafile["golds"]:
        if(entry["date"] == infor[0]):
            array.append(entry["value"])
            for entr in entry["value"]:
                if(entr["type"] == "SJC"):
                    nameBrand.append(entr["brand"])
                    SJC.append(entr)
    for entry in SJC:
        if(entry["brand"] == infor[1]):
            response[0]=entry["buy"]
            response[1]=entry["sell"]
    SJC.clear()
    infor.clear()
    sendList(conn, response)
    print(response)
    Search(conn)


def handleClient(conn: socket, addr):
  
    username = ""
    password = ""
    columnnum = 3
    msg = ""
    option = ""

    try:

        mylist = recvList(conn)
        option = mylist[0]
        username = mylist[1]
        password = mylist[2]
        if(option == "signin"):
            with open("dataUsers.json", "r") as openfile:
                # Reading from json file
                HashTable = json.load(openfile)
            checkLogin = clientLogIn(username, password)
            if(checkLogin == True):
                msg = "signinsuccess"
                conn.sendall(msg.encode(FORMAT))
                newClient={
                  "username": username, 
                  "connname": conn
                }
                ipClientlist.append(username)
                # search function
                Search(conn)
                # for user in ipClientlist:
                #   Label(window, text = user, width="220").grid(row=10, column=columnnum)
                #   columnnum+=1
            else:
              msg= "signinfail"
              conn.sendall(msg.encode(FORMAT))
              handleClient(conn, addr)

        if(option == "signup"):
            checksignup = clientSignUp(username, password)
            print("checksignup: ", checksignup)
            if(checksignup == True):

                checkLogin = clientLogIn(username, password)
                if(checkLogin == True):

                    msg = "signupsuccess"
                    conn.sendall(msg.encode(FORMAT))
                    ipClientlist.append(username)
                    Search(conn)

            else:
                msg = "signupfail"
                conn.sendall(msg.encode(FORMAT))
                # for user in ipClientlist:
                #   Label(window, text = user, width="220").grid(row=3, column=columnnum)
                #   columnnum+=1
        conn.close()

    except ImportError:
        pass  # May not be available everywhere.
        print("Client ", addr, "finished")
        print("Connection ", conn, "closed")
        conn.close()
        # pass


def mymain():

    Active_frame.destroy()
    Button(window, width = 8, height = 2, bd = 0, fg = 'white', bg = 'coral', text = 'Suspend', command =  Suspend).place(x = 240, y = 400)

    print("Waiting for client")
    inform = ""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, port))
    s.listen()
    global nClient
    while(nClient <= MAX_CLIENT):
        try:
            conn, addr = s.accept()
            print(conn, addr)
            thr = threading.Thread(target=handleClient, args=(conn, addr))
            thr.daemon = True  # neu true, neu main end thi kill all thread
            thr.start()
        except:
            print("Error")
        nClient += 1


# --------------- main------------------
Label(window, text = 'Number of connected Clients:', font =('arial', 12, 'italic')).place(x = 0, y = 1)
number = Label(window, text = size, font =('arial', 13), fg = 'tomato')
number.place(x = 219, y = 1)

list = Listbox(window, width = 330, height = 21, font =('arial', 10))
list.place(x = 0, y = 25)

Button(window, width = 8, height = 2, bd = 0, fg = 'white', bg = 'coral', text = 'Refresh', command =  Refresh).place(x = 30, y = 400)
Button(window, width = 8, height = 2, bd = 0, fg = 'white', bg = 'coral', text = 'Quit', command =  Quit).place(x = 135, y = 400)
# Khoi dong
Active_frame = Frame(window)
Active_frame.pack(fill='both', expand=True)

Button(Active_frame, width = 8, height = 2, bd = 0, fg = 'white', bg = 'coral', text = 'A C T I V A T E ', command=threading.Thread(target=mymain).start).place(relx=0.5, rely=0.5, anchor=CENTER)
Button(Active_frame, width = 8, height = 2, bd = 0, fg = 'white', bg = 'coral', text = 'RE A C T I V A T E ', command=threading.Thread(target=mymain).start).place(relx=0.5, rely=0.5, anchor=CENTER)
window.protocol("WM_DELETE_WINDOW", Quit)


# signin_but = Button(window, padx=10, bd=5, fg='black', font=('arial', 16, 'bold'),
                    # text='Khởi động', bg='#ffffff', command=threading.Thread(target=mymain).start).grid(row=10)

s.close()
window.mainloop()
# Tạo một frame đè lên window chính ,