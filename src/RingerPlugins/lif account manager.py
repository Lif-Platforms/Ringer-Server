from concurrent.futures import thread
import os
import socket
import sqlite3
import threading
import RingerAPI as ringer
import time
import json

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

                #establishes a connection with the database and creates a cursor
                conn2 = sqlite3.connect('account.db')
                c2 = conn2.cursor()

                
                #fetches all lines from database 
                c2.execute("SELECT * FROM accounts")
                items = c2.fetchall()
                
                #contacts = []
                
                '''
                
                file = open("JsonFiles/contacts.json", "r")
                print("opened file")
                content = file.read()
                print(content)
                data = json.loads(content)
                print(data)
                if username not in data:
                    data.update({username:"[]"})
                extractContacts = data[username]   
                contacts = list(extractContacts)
                def scanDatabase():
                    for i in contacts:
                        if i == "[":
                            contacts.remove(i)
                            scanDatabase()
                        if i == "]":
                            contacts.remove(i)
                            scanDatabase()
                scanDatabase()
                contacts.append(str(insertName))
                print(contacts)
                file.close() 

                print(contacts)
                print(username)

                #conn2 = sqlite3.connect('account.db')
                #c2 = conn3.cursor()
                #print("connected to database")
                '''
                for item in items:
                    findUser = item[0]
                    print(item)
                    if findUser == username:
                        contacts = json.loads(item[3])
                        print("found account")
                        break

                print(contacts)

                contactsList = contacts['contacts']

                print(contactsList)
                contactsList.append(insertName) 
                print(contactsList)

                toDump = {"contacts":contactsList}
                
                c2.execute(f"""UPDATE accounts SET contacts = '{json.dumps(toDump)}'
                            WHERE Username = '{username}'""")
                
                '''
                with open("JsonFiles/contacts.json", "r") as file:
                    content = file.read() 
                    json_ = json.loads(content)
                    file.close() 
                with open("JsonFiles/contacts.json", "w") as file:
                    json_[username] = contacts
                    file.write(json.dumps(json_))
                    file.close() 
                print('updated dm in contacts')
                '''
                conn2.commit()
                conn2.close()
                client.send('SUCCESS!'.encode('ascii'))

            if message == "LIST_DM":
                '''
                addUser = False 
                with open("JsonFiles/contacts.json", "r") as file:
                    content = file.read() 
                    json_ = json.loads(content)
                    file.close() 
                    if username not in json_:
                        addUser = True 

                if addUser:
                    json_.update({username:""})
                print(content)
                Contacts = json_[username]
                '''
                conn3 = sqlite3.connect('account.db')
                c3 = conn3.cursor()

                
                #fetches all lines from database 
                c3.execute("SELECT * FROM accounts")
                items = c3.fetchall()

                for item in items:
                    findUser = item[0]
                    print(item)
                    if findUser == username:
                        contacts = json.loads(item[3])
                        print("found account")
                        break
                sendContacts = json.dumps(contacts)
                print(sendContacts)
                    
                client.send(sendContacts.encode('ascii'))
                conn3.close() 
                #client.send("DONE!".encode('ascii'))
                #print("Told client 'DONE!'")
        except Exception as e:
            print("ERROR: " + str(e))
            client.close()
            break

def recive(): #handles receiving connections and login
    while True: 
        try:
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
        except Exception as e:
            ringer.error(e)

recive()