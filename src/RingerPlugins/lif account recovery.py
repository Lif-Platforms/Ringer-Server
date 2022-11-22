from msilib.schema import Condition
from random import randint, randrange
from nylas import APIClient
import sqlite3
import threading
import colorama
from colorama import Fore
from datetime import datetime
from datetime import date
import yaml
import socket
import RingerAPI as ringer

ringer.setAppName("Recovery Server")

ringer.log(consoleLog = 'Loading Config...') 
with open('config.yml', 'r') as file:
    configFile = yaml.safe_load(file)
    ringer.log('Config Loaded!') 

def connect():
    try:
        global server
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("0.0.0.0", 20203))
        server.listen()
        ringer.log("Recovery server started")
    except:
        ringer.error("Failed to start recovery server.")
connect()

def handle(client, address):
    client.send("USERNAME".encode('ascii'))
    print('requested username')
    username = client.recv(1024).decode('ascii')
    print(username)

    client.send("EMAIL".encode('ascii'))
    email = client.recv(1024).decode('ascii')
    print(email)

    conn = sqlite3.connect('account.db')
    c = conn.cursor()

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
        email2 = item[2]
        print(email)

        if username == user and email == email2:
            print("found account")
            foundAccount = True
            break
    
    if foundAccount == True:
        client.send('SEND_CODE'.encode('ascii'))
        code = randint(10000, 99999)

        CLIENT_ID = configFile['client-id']
        CLIENT_SECRET = configFile['client-secret']
        ACCESS_TOKEN = configFile['acsess-token']

        nylas = APIClient(
            CLIENT_ID,
            CLIENT_SECRET,
            ACCESS_TOKEN,
        )

        draft = nylas.drafts.create()
        draft.subject = "Lif Account Password Reset"
        #draft.body = "<p>We just received a request to reset your password. Here is your reset code: " + str(code) + "</p>"

        with open("email.html", "r") as email:
           content = email.read()

        draft.body = content.replace("[code]", str(code)) 


        draft.to = [{'name': username, 'email': email2}]

        draft.send()
        email.close()

        while True:
            reciveCode = client.recv(1024).decode('ascii')
            if reciveCode == "SENDING...":
                reciveCode = client.recv(1024).decode('ascii')
                print(reciveCode)
                if reciveCode == str(code):
                    client.send("SEND_NEW_PASSWORD".encode('ascii'))
                    break
                else:
                    client.send("CODE_ERROR".encode('ascii'))

        while True:
            recivePassword = client.recv(1024).decode('ascii')
            if recivePassword == "SENDING...":
                recivePassword = client.recv(1024).decode('ascii')
                print(recivePassword)

                c.execute(f"""UPDATE accounts SET Password = '{recivePassword}'
                            WHERE Username = '{username}'""")
                client.send("RESET_SUCCESS".encode('ascii'))
                conn.commit()
                conn.close()

    else:
        client.send('BAD_LOGIN_ERROR'.encode('ascii'))
        ringer.log(f"Closed ({str(address)}). REASON: Invalid login credentials") 
        client.close()

while True:
    try:
        client, address = server.accept()
        print(client)
        ringer.log(f"Connected with {str(address)}")
        
        thread = threading.Thread(target=handle, args=(client, address))
        thread.start()

    except Exception as e:
        ringer.error(f'LOST CONNECTION! Trying to connect... Exception: {e}') 
        serverOnline = False
        connect()