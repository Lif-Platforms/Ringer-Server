from inspect import currentframe
from pydoc import cli
import threading
import socket
import time
from datetime import datetime
import sys
from datetime import date
import colorama
from colorama import Fore

def log(consoleLog):
    global current_time
    global current_date
    now = datetime.now()
    current_date = date.today() 
    try:
        current_time = now.strftime("%H:%M:%S")
    except:
        current_time = ":UNKNOWN:"

    print(Fore.WHITE + f"[LOG {current_date} {current_time}][Vc Server]: {consoleLog}")

def error(errorLog):
    global current_time
    global current_date
    now = datetime.now()
    current_date = date.today() 
    try:
        current_time = now.strftime("%H:%M:%S")
    except:
        current_time = ":UNKNOWN:"

    print(Fore.RED + f"[ERROR {current_date} {current_time}][Vc Server]: {errorLog}" + Fore.WHITE)

def warning(warnLog):
    global current_time
    global current_date
    now = datetime.now()
    current_date = date.today() 
    try:
        current_time = now.strftime("%H:%M:%S")
    except:
        current_time = ":UNKNOWN:"

    print(Fore.YELLOW + f"[WARN {current_date} {current_time}][Vc Server]: {warnLog}" + Fore.WHITE)

global current_time

def on_server_stop():
    log("Stopping Vc Server")
    sys.exit()


host = '0.0.0.0'
port = 5000

server = socket.socket() 
server.bind((host, port)) 
server.listen()

log('Voice call server started and online!')

clientsInVC = []

def handleVC(fromConnection):
    log("User conected to VC server.")
    while True:
        try:
            data = fromConnection.recv(4096)
            for client in clientsInVC:
                if client != fromConnection:
                    client.send(data)
        except:
            client.close()
            clientsInVC.remove(conn)

while True:
    conn, addr = server.accept()
    clientsInVC.append(conn)
    thread = threading.Thread(target=handleVC, args=(conn, ))
    thread.start()
