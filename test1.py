import socket
import threading
HOST="127.0.0.1"
port=6767
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, port))
s.listen()

conn, addr = s.accept() 
print (conn)
print(conn, addr)
s.close()
pyinstaller --onefile - w --add-data "data.json;." --add-data "dataUsers.json;." server.py