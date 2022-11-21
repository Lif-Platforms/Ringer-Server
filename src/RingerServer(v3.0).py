
import email
from threading import Thread
import colorama
from colorama import Fore

import RingerAPI as ringer

processes = [] 

global shutdown
shutdown = False

print(Fore.WHITE + "Ringer Server v3 Loading Libraries...")
try:
    import ctypes
    import json
    import os
    import socket
    import sqlite3
    import subprocess
    import sys
    import threading
    import time
    from datetime import date, datetime
    from os import listdir
    from os.path import isfile, join
    from pydoc import cli
    from random import randint, randrange

    import yaml
    print(sys.executable)
    from subprocess import PIPE, STDOUT, Popen

    from nylas import APIClient
except Exception as e:
    print(Fore.RED + "Failed to import libraries! Exception:", e)
    exit()

global serverOnline
serverOnline = False

Swares = ["shit", "fuck", "bitch", "gay", "ass", "dick", "pussy ", 'hell ', "crap", "nigger ", "douchebag", "penis", "sod ", 'bugger', "git", "arse", "bint", "munter", "minger", "balls", "arsehole", "pissed", "bollocks", "bellend", "tit", "fanny", "snatch", "clunge", "gash", "prick", "twat", "punani", "minge", "cock", "bastard", "wanker", "cunt", "hoe"]
 


global current_time

global kickUser
kickUser = False 

ringer.setAppName("Main Server")

ringer.log(consoleLog = "Server Starting...")


ringer.log(consoleLog = 'Loading Config...') 
with open("config.yml", 'r') as file:
    configFile = yaml.safe_load(file)
    ringer.log('Config Loaded!') 

'''
def activation():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 20203))

    client.send(configFile['DAL'].encode('ascii'))
'''

host = configFile['host']
port = 20200

global tries
tries = 0


def connect():
    global server 
    global tries 
    global serverOnline
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen() 
        ringer.log('Connection sucsessful!')
        serverOnline = True
    except Exception as Error: 
        if tries < 4:
            ringer.error('Failed to connect to the internet! Trying again in 10 seconds... Exception: '+ str(Error)) 
            time.sleep(10)
            tries = tries +1 
            connect()
        else:
            ringer.error("Failed to connect to the internet! Trying again in 1 minute... Exception: " + str(Error))
            time.sleep(60)
            tries = 0 
            server.close()
            connect() 
connect()


ringer.log("Loading Plugins...")


onlyfiles = os.listdir("RingerPlugins/")
#onlyfiles = [f for f in listdir(pluginpath) if isfile(join(pluginpath, f))]

for file in onlyfiles:
    if not file.endswith(".py"):
        onlyfiles.remove(file)
    if file in configFile['denied-plugins']:
        onlyfiles.remove(file)

ringer.log("Detected plugins: " + str(onlyfiles))

def plugin_thread(file):
    args = "RingerPlugins/" + file
    processes.append(file)
    global shutdown
    p = subprocess.Popen(['python', args])
    output, error_ = p.communicate()
    if not error_:
        print(output) 
    else:
        p.terminate()
        ringer.error(f"Plugin {file} was terminated due to an error. It wrote:")
        print(error_)
    
    while True:
        if shutdown == True:
            ringer.log("Shut down process: " + file)
            processes.remove(file)
            p.terminate() 
        
        
     #exec(open(pluginpath + file).read())
    

for file in onlyfiles:
    ringer.log(f"Started Plugin: {file}...")
    pluginThread = threading.Thread(target=plugin_thread, args=(file,))
    pluginThread.start()


global conn
global c
conn = sqlite3.connect('account.db')
c = conn.cursor()


clients = []
nicknames = []
users = {}


ringer.log('Server Online!')

def brodcast(message):
    for client in clients:
        client.send(message) 

def handle(client, nickname, address, c, conn):
    global index
    global shutdown
    processes.append(nickname)
    if len(nicknames) == 1:
        client.send(f'''
    You are alone in the chat. Anything you say is between you and us.
    '''.encode('ascii'))
    else:
        client.send(f'''
    You are chatting with: {str(nicknames)[2:-2]}.
    '''.encode('ascii'))
    socket.setdefaulttimeout(5) 
    dmRequest = False

    while True:
        if shutdown == True:
            ringer.log("Shut down process: " + nickname)
            client.close() 
            processes.remove(nickname)
            break
        try:
            message = client.recv(1024).decode('ascii')

            username = message.split()[0]
            #send(message, username)
            #client.send('message sent'.encode('ascii'))

            print(username)
            
            if user := users.get(username):
                print(user)
                if message:
                    user.send(message.encode("ascii"))
            else:
               client.send("user no exist".encode('ascii'))
            #brodcast(message)
            
        except Exception as e:
            ringer.log(f"Lost Connection With: {str(address)}. Reason: " + str(e))
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            brodcast(f'''
    {nickname} left the chat
'''.encode('ascii')) 
            ringer.log(f'{nickname} left the chat.') 
            nicknames.remove(nickname)
            users.pop(nickname)
            print(users)
            #users.remove([nickname, address])
            #print(users)
            break 

def terminal():
    global shutdown
    command = input('')
    
    if command == 'ping':
        print('Pong!')
        terminal()

    if command == 'host':
        print("Host: " + host)
        print("Port: " + str(port))
        terminal()

    if command == 'list users':
        print("users: " + str(nicknames))
        terminal()
    if command == 'shutdown':
        shutdown = True
        ringer.log("Shutting Down...")
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread, 0)
        sys.exit() 
    else:
        print('Unknown Command!')
        terminal()

ringer.log("Terminal Running!")
thread = threading.Thread(target=terminal)
thread.start()



def recive(conn, c):
    global serverOnline
    global shutdown
    processes.append("Receive")
    while True:
        if shutdown == True:
            processes.remove('Receive')
            server.close() 
            ringer.log("Shut down main receive thread")
            break
        try:
            client, address = server.accept()
            print(client)
            ringer.log(f"Connected with {str(address)}")
            client.send('LOGIN'.encode('ascii'))
            login = client.recv(1024).decode('ascii')
            if login == "CREATEACCOUNT":
                client.send("USERNAME?".encode('ascii'))
                username = client.recv(1024).decode('ascii')
                print(username)
                client.send("PASSWORD?".encode('ascii'))
                password = client.recv(1024).decode('ascii')
                client.send("EMAIL?".encode('ascii'))
                email = client.recv(1024).decode('ascii')
                print('conected to database')

                try:
                    c.execute("""CREATE TABLE accounts (
                        Username TEXT,
                        Password TEXT,
                        email TEXT,
                        contacts TEXT    
                    )
                    """)
                except:
                    pass

                print('created table')

                c.execute("SELECT * FROM accounts")
                items = c.fetchall()

                continueCreation = True

                for item in items:
                    findUser = item[0]
                    if findUser == username:
                        client.send('ERROR_ACOUNT_EXSISTING'.encode('ascii'))
                        continueCreation = False  
                        break

                for item in items:
                    findUser = item[2]
                    if findUser == email:
                        client.send('ERROR_ACOUNT_EXSISTING'.encode('ascii'))
                        continueCreation = False  
                        break
                
                if continueCreation == True:
                    data = (username, password, email, '[]')

                    c.execute(f"INSERT INTO accounts VALUES (?,?,?,?)", data)
                    print('executed data')

                    conn.commit()
                    print('saved data')

                        
                    client.send('ACCOUNTCREATED'.encode('ascii'))
                    

            elif login == "LIF_LOGIN":
                #f = open("Banned.txt",  "r")
                #if login in f.read():
                    #client.send("BANNED!".encode("ascii"))
                    #client.close()
                #else:
                client.send('USERNAME'.encode('ascii'))
                nickname = client.recv(1024).decode('ascii')

                checkUser = nickname.lower()

                if any(word in checkUser for word in Swares):
                    with open("Banned.txt", 'a') as file1:
                        file1.write(nickname + " \n")
                        file1.close()

                word_list = []
                f = open('Banned.txt')
                word_list2 = f.read().split()
                for item in word_list2:
                    if item in word_list:
                        continue
                    else:
                        word_list.append(item)
                word_list.sort()
                print(word_list) 

                banned = False

                for word in word_list:
                    if nickname == word:
                        client.send("BANNED!".encode('ascii'))
                        client.close()
                        banned = True

                f.close()

                if banned == False:
                    client.send("PASSWORD".encode('ascii'))
                    password = client.recv(1024).decode('ascii')

                    c = conn.cursor()
                    print('conected to database')

                    c.execute("SELECT * FROM accounts")
                    items = c.fetchall()
                    conn.commit()
                    print('data accsessed')
                    print(items)
                    foundAccount = False

                    for item in items:
                        print('seraching...')
                        user = item[0]
                        print(user)
                        passwrd = item[1]
                        print(passwrd)

                        if nickname == user and password == passwrd:
                            print("found account")
                            foundAccount = True
                            break

                    if foundAccount == True: 
                        print("login good")
                        client.send("LOGIN_GOOD".encode('ascii'))
                        nicknames.append(nickname)
                        clients.append(client)
                        data = {nickname: client}
                        users.update(data)
                        print(users)
                        ringer.log(f'{nickname} joined the chat!')
                        brodcast(f'''
    {nickname} joined the chat!
'''.encode('ascii'))    
                
                        thread = threading.Thread(target=handle, args=(client, nickname, address, conn, c))
                        thread.start()

                    
                    else:
                        client.send('BAD_LOGIN_ERROR'.encode('ascii'))
                        ringer.log(f"Closed ({str(address)}). REASON: Invalid login credentials") 
                        client.close()

            elif login == "ANOUCEMENT!":
                try:
                    f = open("Anouncement.txt", "r")
                    Anoucement = f.read()
                    client.send(Anoucement.encode('ascii'))
                    f.close()
                except:
                    client.send("An Error Accrued".encode('ascii'))

            elif login == "Check_Version":
                ringerVersion = configFile['current_version']
                client.send(f"{ringerVersion}".encode('ascii'))
                client.close()

            else:
                client.send('BAD_LOGIN_ERROR'.encode('ascii'))
                ringer.log(f"Closed ({str(address)}). REASON: Invalid login credentials") 
                client.close()
            
        except Exception as e:
            ringer.error(f'LOST CONNECTION! Trying to connect... Exception: {e}') 
            serverOnline = False
            connect() 
recive(conn, c) 