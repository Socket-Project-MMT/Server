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
FORMAT="utf-8"
URL="https://tygia.com/json.php"
# Ngày 
DATE="20213112"


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, port))
s.listen()

ipClientlist = []
length=len(ipClientlist)
dates=[]
with open("data.json", "r") as openfile:
    # Reading from json file
    datafile = json.load(openfile)
#list theo gold
values=datafile["golds"]
# loc mot gia tri theo tri so co dieu kien


searchlist=[]
# namelist la ten brand co dinh

namelist=[]
SJC=[]
array=[]
# loc het danh sach theo tri so, cos mot dieu kien
for entry in datafile["golds"]:
  if(entry["date"]==DATE):
    array.append(entry["value"])
    for entr in entry["value"]:
      if(entr["type"]=="SJC"):
        namelist.append(entr["brand"])
        #SJC.append(entr)
# print("type sjc", namelist)
# array la mang vang theo ngay
for entry in SJC:
  if(entry["brand"]==msg):
    print(entry["buy"])
for entry in datafile["golds"]:
  dates.append(entry["date"])
# for entry in namelist:
#   if(entry=="SJC"):
#     SJC.append(entry)


with open("dataUsers.json", "r") as openfile:
    # Reading from json file
    HashTable = json.load(openfile)
print("Hash:",HashTable)
nClient=0
window = Tk()
window.title("TY GIA SERVER")
window.geometry('700x350')

def recvList(conn):
  mylist=[]
  item=conn.recv(1024).decode(FORMAT)
  while(item!="end"):
    mylist.append(item)
    conn.sendall(item.encode(FORMAT))
    item=conn.recv(1024).decode(FORMAT)

  return mylist
def sendList(conn, list):
    for item in list:
        conn.sendall(item.encode(FORMAT))
        msg=conn.recv(1024).decode(FORMAT)
    msg="end"
    conn.sendall(msg.encode(FORMAT))
def checkClientSignUp(username):
    if(username in HashTable):
        #connection.send(str.encode('Account existed'))
        return False
    else: 
      return True

def checkClientLogIn(username, password):
    if(HashTable[username] == password):
        return True
    return False
    

def clientSignUp(username, password, connection):
    global HashTable
    try:
        if(checkClientSignUp(username) == False):
            return False
        else: 
          HashTable[username]=password

          print('Registered : ',username)
          
          #write users infor to file
          infor = {
              username: password
          }

          with open("dataUsers.json", "r+") as file:
              data = json.load(file)
              data.update(infor)
              file.seek(0)
              json.dump(data, file, intent=4)
          return True

    except: 
        print("Error")

def clientLogIn(username, password, connection):

    if(checkClientLogIn(username, password) == False):
         # Response code for login failed
        print('Connection denied : ',username)
        return False
    else:
        # Response Code for Connected Client 
        print('Connected : ',username)
        return True
def Search(conn):

  global namelist
  global dates
  sendList(conn, namelist)
  sendList(conn, dates) 
  global datafile
  infor=["", ""]
  infor=recvList(conn)

  response=[]
  for entry in datafile["golds"]:
    if(entry["date"]==infor[0]):
      array.append(entry["value"])
      for entr in entry["value"]:
        if(entr["type"]=="SJC"):
          namelist.append(entr["brand"])
          SJC.append(entr)
  for entry in SJC:
    if(entry["brand"]==infor[1]):
      response.append(entry["buy"])
      response.append(entry["sell"])
  sendList(conn, response)
  print(response)

def handleClient(conn: socket, addr):
  username=""
  password=""
  columnnum=3
  msg=""
  option=""

  try:
    # test=conn.recv(1024).decode(FORMAT)
    # print(test)
    mylist=recvList(conn)
    print("mylist:",mylist)
    option=mylist[0]
    username=mylist[1]
    password=mylist[2]
    if(option=="signin"):
      with open("dataUsers.json", "r") as openfile:
    # Reading from json file
        HashTable = json.load(openfile)
      checkLogin = clientLogIn(username, password, conn)
      if(checkLogin==True):
        msg="signinsuccess"
        conn.sendall(msg.encode(FORMAT))
        ipClientlist.append(username)
        #search function
        Search(conn)
        # for user in ipClientlist: 
        #   Label(window, text = user, width="220").grid(row=10, column=columnnum)
        #   columnnum+=1

    if(option=="signup"):
      checksignup = clientSignUp(username, password, conn)
      if(checksignup == True):

        checkLogin = clientLogIn(username, password, conn)
        if(checkLogin==True):
          
          msg="signupsuccess"
          conn.sendall(msg.encode(FORMAT))
          Search(conn)
          ipClientlist.append(username)
      else: 
        msg="signupfail"
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
  print("Waiting for client")
  inform=""
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((HOST, port))
  s.listen()
  global nClient
  while(nClient<=100):
    try: 
      conn, addr = s.accept()
      print(conn, addr)
      thr= threading.Thread(target=handleClient, args=(conn, addr))
      thr.daemon=True # neu true, neu main end thi kill all thread
      thr.start()
    except: 
      print("Error")
    nClient+=1




# --------------- main------------------


Label(window, text = "Tên đăng nhập", bg = 'red').grid(row = 4, column = 0)

# Label(window, text=ipClientlist[0], width="220").grid(column=1, row=0)

print("kkkk")


signin_but = Button(window, padx = 10, bd = 5, fg = 'black', font = ('arial', 16, 'bold'), text = 'Đăng nhập', bg = '#ffffff', command = threading.Thread(target=mymain).start).grid(row = 10)

print("kk")
print("end")
s.close()
window.mainloop()