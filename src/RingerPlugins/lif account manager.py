from concurrent.futures import thread
from glob import glob
import os
import socket
import sqlite3
import threading
import RingerAPI as ringer
import time

ringer.setAppName("Account Manager") 
ringer.log("Server Starting...")

host = "0.0.0.0"
port = 20205

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

def handle(client, username):
    while True:
        try:
            message = client.recv(1024).decode('ascii')

            if message == "ADD_DM":
                print('dm request recived')
                client.send("DM_NAME?".encode('ascii'))
                print('requested dm name')
                name = client.recv(1024).decode('ascii')

                insertName = name.replace("ADD_DM", "")

                    
                print("Name: " + insertName)

                conn2 = sqlite3.connect('account.db')
                c2 = conn2.cursor()

                c2.execute("SELECT * FROM accounts")
                items = c2.fetchall()

                contacts = []


                for item in items:
                    findUser = item[0]
                    print(item)
                    if findUser == username:
                        contacts = list(item[3])
                        print("found account")
                        break
                            
                contacts.append(insertName)
                print(contacts)

                c2.execute(f"""UPDATE accounts SET contacts = '{str(contacts)}'
                                WHERE Username = '{username}'
                """)

                print('updated dm in contacts')

                conn2.commit()

                conn2.close()

                client.send('SUCCESS!'.encode('ascii'))
        except:
            client.close()

def recive():
    while True: 
        client, address = server.accept()
        conn = sqlite3.connect('account.db')
        c = conn.cursor()

        print(client)
        ringer.log(f"Connected with {str(address)}")
        #retrieve username 
        client.send("USERNAME".encode('ascii'))
        username = client.recv(1024).decode('ascii')
        #retrieve password
        client.send("PASSWORD".encode('ascii'))
        password = client.recv(1024).decode('ascii')

        c.execute("SELECT * FROM accounts")
        items = c.fetchall()

        foundAccount = False

        for item in items:
            print('seraching...')
            user = item[0]
            print(user)
            passwrd = item[1]
            print(passwrd)

            if username == user and password == passwrd:
                print("found account")
                foundAccount = True
                break

        if foundAccount == True:
            client.send("LOGIN_GOOD".encode('ascii'))
            handleThread = threading.Thread(target=handle, args=(client, username))
            handleThread.start()
            conn.close()
        else:
            client.send('ACCOUNT_NOT_FOUND'.encode('ascii'))
            conn.close()

recive()


        