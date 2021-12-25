# fileserver.py

from json.decoder import JSONDecodeError
from json.encoder import JSONEncoder
import socket 
import threading
import json
import urllib.parse
import requests



HOST = "127.0.0.1"
port = 6767
FORMAT="utf8"
URL="https://tygia.com/json.php"
#URL="https://www.dongabank.com.vn/exchange/export"

def handleClient(conn: socket, addr):
  print("Client address: ", addr)
  print("conn: ", conn.getsockname())
  try:
    # if hasattr(socket, "TCP_KEEPIDLE") and hasattr(socket, "TCP_KEEPINTVL") and hasattr(socket, "TCP_KEEPCNT"):
    #   from socket import IPPROTO_TCP, SO_KEEPALIVE, TCP_KEEPIDLE, TCP_KEEPINTVL, TCP_KEEPCNT
    #   conn.setsockopt(socket.SOL_SOCKET, SO_KEEPALIVE, 1)
    #   conn.setsockopt(IPPROTO_TCP, TCP_KEEPIDLE, 1)
    #   conn.setsockopt(IPPROTO_TCP, TCP_KEEPINTVL, 1)
    #   conn.setsockopt(IPPROTO_TCP, TCP_KEEPCNT, 1)
    msg = None
    print("Say Hi! to client!")
    msg = input("You: ")
    conn.sendall(msg.encode(FORMAT))
    while(msg != "End"):
      msg = conn.recv(1024).decode(FORMAT)
      print("Client: ", msg)
      msg = input("You: ")
      if(msg=="EndAll"):
        print("")
      conn.sendall(msg.encode(FORMAT))
      print("Client ", addr, "finished")
      print("Connection ", conn, "closed")
      conn.close()
  except ImportError:
    pass  # May not be available everywhere.
    print("Client ", addr, "finished")
    print("ulatr")
    print("Connection ", conn, "closed")
    conn.close()
    # pass
    
  

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, port))
s.listen()
print("I'm server, ", HOST)
print("Server listening on port", port)
print("Waiting for client")
data=requests.get(URL)
print("kkkk")
print("KK: ", str(data))
kk=json.loads(data)
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
nClient=0

while(nClient<=1000):
  try: 
    conn, addr = s.accept()
    thr= threading.Thread(target=handleClient, args=(conn, addr))
    thr.daemon=True # neu true, neu main end thi kill all thread
    thr.start()
  except: 
    print("Error")
  nClient+=1



print("end")
s.close()
