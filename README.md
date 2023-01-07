![Ringer Logo](https://github.com/Lif-Platforms/Ringer-Server/blob/main/.github/Ringerlogo.png)
# Ringer-Server
Ringer server is the server code for the Ringer messaging app. The code here is snapshot code so it may not work as intended. 

# Client Code
Ringers client code is located in another repository: https://github.com/Lif-Platforms/Ringer-Client-Windows

# Instalation and Use
Ringer server requires little setup. all you need is to clone the repository and install all of the required libraries. Also make sure you have the configuration correct. 

### Config

**host:** The address ringer will bind to. 

**email info:** Ringer server sends emails as part of the accout recovery system. To do this we use nylas. To get this feature to work, please sign up for nylas and enter your info in the email info section in the config.

**denied plugins:** Ringer plugins are python files that will be executed as a subprosses when the server starts. you can disable plugins by addding the file name into the config. Example: myPlugin.py (NOT WORKING! Needs Fix)

**current version:** This is what the server will tell the client to make sure thr client is up-to-date. If you are in the latest server code, you should not need to change this. 
