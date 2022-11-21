import os
import socket
import threading
from datetime import datetime
import colorama
from colorama import Fore
from datetime import date
import os

def log(consoleLog):
    global current_time
    global current_date
    now = datetime.now()
    current_date = date.today() 
    try:
        current_time = now.strftime("%H:%M:%S")
    except:
        current_time = ":UNKNOWN:"

    print(Fore.WHITE + f"[LOG {current_date} {current_time}][Installer Server]: {consoleLog}")

def error(errorLog):
    global current_time
    global current_date
    now = datetime.now()
    current_date = date.today() 
    try:
        current_time = now.strftime("%H:%M:%S")
    except:
        current_time = ":UNKNOWN:"

    print(Fore.RED + f"[ERROR][{current_date}][{current_time}][Installer Server]: {errorLog}" + Fore.WHITE)

def warning(warnLog):
    global current_time
    global current_date
    now = datetime.now()
    current_date = date.today() 
    try:
        current_time = now.strftime("%H:%M:%S")
    except:
        current_time = ":UNKNOWN:"

    print(Fore.YELLOW + f"[WARN][{current_date}][{current_time}][Installer Server]: {warnLog}" + Fore.WHITE)

global current_time

log("Installer Server Starting...")

host = "0.0.0.0"
port = 20202

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen() 

log("Installer Server Online")

def handle():
    global current_time
    while True:
        message = client.recv(1024).decode('UTF-8')

        if message == "Size?":
            print('sending size')
            size = os.path.getsize('C:\\Users\\btb5s\\Desktop\Ringer Files\\Temp\\Ringer.zip')
            client.send(str(size).encode('ascii'))

        if message == "Software":
            print('sending app')
            filename='C:\\Users\\btb5s\\Desktop\Ringer Files\\Temp\\Ringer.zip' #In the same folder or path is this file running must the file you want to tranfser to be
            f = open(filename,'rb')
            l = f.read(1024*16)
            while (l):
                client.send(l)
                #print('Sent ',repr(l))
                l = f.read(1024*16)
            f.close()
            client.send('Done!'.encode('UTF-8'))
            #print('Done sending')
            log( f"Sent software to user: {str(address)}")
            client.close()
            break

        if message == "App":
            print('sending app')
            filename='C:\\Users\\btb5s\\Desktop\Ringer Files\\Temp\\Ringer.exe' #In the same folder or path is this file running must the file you want to tranfser to be
            f = open(filename,'rb')
            l = f.read(1024*16)
            while (l):
                client.send(l)
                print('Sent ',repr(l))
                l = f.read(1024*16)
            f.close()
            client.send('Done!'.encode('UTF-8'))
            print('Done sending')
            client.close()

        if message == "botImage":
            print("sending image")
            filename='C:\\Users\\btb5s\\Desktop\Ringer Files\\Temp\\Ringer-Bot.png' #In the same folder or path is this file running must the file you want to tranfser to be
            f = open(filename,'rb')
            l = f.read(1024*16)
            while (l):
                client.send(l)
                print('Sent ',repr(l))
                l = f.read(1024*16)
            f.close()
            client.send('Done!'.encode('UTF-8'))
            print('Done sending')
            client.close()

        if message == "sendButton":
            print("sending button")
            filename='C:\\Users\\btb5s\\Desktop\Ringer Files\\Temp\\sendButton.png' #In the same folder or path is this file running must the file you want to tranfser to be
            f = open(filename,'rb')
            l = f.read(1024*16)
            while (l):
                client.send(l)
                print('Sent ',repr(l))
                l = f.read(1024*16)
            f.close()
            client.send('Done!'.encode('UTF-8'))
            print('Done sending')
            client.close()

        if message == "ringerIcon":
            print("sending icon")
            filename='C:\\Users\\btb5s\\Desktop\Ringer Files\\Temp\\Ringer-Icon.ico' #In the same folder or path is this file running must the file you want to tranfser to be
            f = open(filename,'rb')
            l = f.read(1024*16)
            while (l):
                client.send(l)
                print('Sent ',repr(l))
                l = f.read(1024*16)
            f.close()
            client.send('Done!'.encode('UTF-8'))
            print('Done sending')
            client.close()
    
while True:
    client, address = server.accept()

    thread = threading.Thread(target=handle)
    thread.start()


    