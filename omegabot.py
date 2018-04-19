import socket
import re
import irc
import commands
from aiohttp import web
import socketio

#CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

# network functions go here
s = socket.socket()
s.connect((irc.HOST, irc.PORT))
s.send("PASS {}\r\n".format(irc.PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(irc.NICK).encode("utf-8"))
for chan in irc.CHAN:
    s.send("JOIN {}\r\n".format(chan).encode("utf-8"))
for tag in irc.TAGS:
    s.send("CAP REQ :twitch.tv/{}\r\n".format(tag).encode("utf-8)"))

connected = False
while True:
    response = s.recv(1024).decode("utf-8")
    if connected == False:
        loadCheck = response.find("End of /NAMES list")
    if loadCheck != -1 and connected == False:
        connected = True
        print("Connected")
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        print("Pong")
    else:
        if connected == True:
            msg = response.find("End of /NAMES list")
            msg2 = response.find("twitch.tv JOIN #")
            if msg == -1 and msg2 == -1:
                findNick = str.find(response, "!")
                username = response[1:findNick]
                msgIndex = response[3:]
                findMsg = str.find(msgIndex, ":") + 1
                message = msgIndex[findMsg:]
                message = message.rstrip()
                chanIndex = response[3:]
                findChan = str.find(chanIndex, "#") + 3
                channel = response[findChan:findMsg + 1]
                print(channel + ": " + username + ": " + message)
                
                commands.checkMessage(s, message, username, channel)