import socket
import os
import threading
import hashlib
import json





# Function : For each client 
def threaded_client(connection):
    connection.send(str.encode('ENTER USERNAME : ')) # Request Username
    name = connection.recv(2048)
    connection.send(str.encode('ENTER PASSWORD : ')) # Request Password
    password = connection.recv(2048)
    password = password.decode()
    name = name.decode()
    #password=hashlib.sha256(str.encode(password)).hexdigest() # Password hash using SHA256
# REGISTERATION PHASE   
# If new user,  regiter in Hashtable Dictionary  
    if name not in HashTable:
        HashTable[name]=password
        connection.send(str.encode('Registeration Successful')) 
        print('Registered : ',name)
        print("{:<8} {:<20}".format('USER','PASSWORD'))
        for k, v in HashTable.items():
            label, num = k,v
            print("{:<8} {:<20}".format(label, num))
        print("-------------------------------------------")
        #write users infor to file
        infor = {
            name: password
        }

        with open("dataUsers.json", "r+") as file:
            data = json.load(file)
            data.update(infor)
            file.seek(0)
            json.dump(data, file)
        
        
    else:
    # If already existing user, check if the entered password is correct
        if(HashTable[name] == password):
            connection.send(str.encode('Connection Successful')) # Response Code for Connected Client 
            print('Connected : ',name)
        else:
            connection.send(str.encode('Login Failed')) # Response code for login failed
            print('Connection denied : ',name)
    while True:
        break
    connection.close()


def checkClientSignUp(username, connection):
    if(username in HashTable):
        #connection.send(str.encode('Account existed'))
        return False
    return True

def checkClientLogIn(username, password, connection):
    if(HashTable[username] == password):
        
        return True
    return False
    

def clientSignUp(username, password, connection):
    try:
        #connection.send(str.encode('ENTER USERNAME : ')) # Request Username
        username = connection.recv(2048)
        #connection.send(str.encode('ENTER PASSWORD : ')) # Request Password
        password = connection.recv(2048)

        if(checkClientSignUp(username, connection) == False):
            connection.send(str.encode('Account existed'))
            clientSignUp(username, password, connection)


        HashTable[username]=password
        connection.send(str.encode('Registeration Successful')) 
        print('Registered : ',username)
        print("{:<8} {:<20}".format('USER','PASSWORD'))
        for k, v in HashTable.items():
            label, num = k,v
            print("{:<8} {:<20}".format(label, num))
        print("-------------------------------------------")
        #write users infor to file
        infor = {
            username: password
        }

        with open("dataUsers.json", "r+") as file:
            data = json.load(file)
            data.update(infor)
            file.seek(0)
            json.dump(data, file)

    except: 
        print("Error")

def clientLogIn(username, password, connection):
    #connection.send(str.encode('ENTER USERNAME : ')) # Request Username
    username = connection.recv(2048)
    #connection.send(str.encode('ENTER PASSWORD : ')) # Request Password
    password = connection.recv(2048)
    if(checkClientLogIn(username, password, connection) == False):
        connection.send(str.encode('Username or Password is incorrect')) # Response code for login failed
        print('Connection denied : ',username)
    else:
        connection.send(str.encode('Connection Successful')) # Response Code for Connected Client 
        print('Connected : ',username)
        print("{:<8} {:<20}".format('USER','PASSWORD'))
        for k, v in HashTable.items():
            label, num = k,v
            print("{:<8} {:<20}".format(label, num))
            print("-------------------------------------------")
    

# def handleServer(connection, )
# def runServer():
#     try:


#---------------------------main -----------------------
# 

# Create Socket (TCP) Connection
ServerSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM) 
host = '127.0.0.1'   
port = 60000
ThreadCount = 0

try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)

with open("dataUsers.json", "r") as openfile:
    # Reading from json file
    HashTable = json.load(openfile)


while True:
    Client, address = ServerSocket.accept()
    client_handler = threading.Thread(
        target=threaded_client,
        args=(Client,)  
    )
    client_handler.start()
    ThreadCount += 1
    print('Connection Request: ' + str(ThreadCount))

ServerSocket.close()