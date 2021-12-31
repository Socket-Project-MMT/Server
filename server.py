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
FORMAT="utf8"
URL="https://tygia.com/json.php"
# URL=
# 
# 


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, port))
s.listen()

ipClientlist = []
length=len(ipClientlist)

with open("data.json", "r") as openfile:
    # Reading from json file
    datafile = json.load(openfile)

values=datafile["rates"][0]["value"]
sjclist=values["code"]

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
    print("recv f", item)
    conn.sendall(item.encode(FORMAT))
    item=conn.recv(1024).decode(FORMAT)

  return mylist
def sendList(conn, list):
    for item in list:
        conn.sendall(item.encode(FORMAT))
        msg=conn.recv(1024).decode(FORMAT)
        print("msg", msg)
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
              json.dump(data, file)
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
        newclient = {
          username: password
        }
        msg="signinsuccess"
        conn.sendall(msg.encode(FORMAT))
        ipClientlist.append(newclient)
        #search function
        
        for user, password in ipClientlist.items(): 
          Label(window, text= "kkkk", width="220").grid(column=columnnum, row=3)
          columnnum+=1

    if(option=="signup"):
      checksignup = clientSignUp(username, password, conn)
      if(checksignup == True):

        checkLogin = clientLogIn(username, password, conn)
        if(checkLogin==True):
          newclient = {
            username: password
          }
          msg="signupsuccess"
          conn.sendall(msg.encode(FORMAT))
        ipClientlist.append(newclient)
      else: 
        msg="signupfail"
        conn.sendall(msg.encode(FORMAT))
        handleClient(conn, addr)
        # for user, password in ipClientlist.items(): 
        #   Label(window, text= user, width="220").grid(column=columnnum, row=3)
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
  while(nClient<=10):
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