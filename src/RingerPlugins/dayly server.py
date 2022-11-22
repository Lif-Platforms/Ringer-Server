import asyncio
import sqlite3
import websockets
import hashlib
import secrets
import json
 
# create handler for each connection
 
async def handler(websocket, path):
    data = await websocket.recv()
    #client_ip = websocket.getpeername()[0]
    #print(client_ip)

    if data == "DAYLY_LOGIN":
        #requests user credentials 
        await websocket.send("USERNAME")
        username = await websocket.recv()
        await websocket.send("PASSWORD")
        password1 = await websocket.recv()

        salt = "5gz"
                        
        # Adding salt at the last of the password
        dataBase_password = password1+salt
        # Encoding the password
        hashed = hashlib.md5(dataBase_password.encode())
        print('hashed password')
        
        # Sending the Hash
        password = hashed.hexdigest()

        conn = sqlite3.connect('account.db')
        c = conn.cursor()

        c.execute("SELECT * FROM accounts")
        items = c.fetchall()

        foundAccount = False

        for item in items:
            print('seraching...')
            user = item[0]
            print(user)
            password2 = item[1]
            print(password2)

            if username == user and password == password2:
                print("found account")
                foundAccount = True
                break

        if foundAccount == True:
            await websocket.send("SUCCESS")
            requestToken = await websocket.recv()
            if requestToken == "TOKEN?":
                token = secrets.token_urlsafe(16) 
                await websocket.send(token) 

        else:
            await websocket.send("INVALID_CREDENTIALS")


    #reply = f"Data recieved as:  {data}!"
 
    #await websocket.send(reply)
 
start_server = websockets.serve(handler, "localhost", 8000)
 
 
 
asyncio.get_event_loop().run_until_complete(start_server)
 
asyncio.get_event_loop().run_forever()