import socket
import irc
from commands import checkMessage, tokenize
import threading
import time
from urllib.request import urlopen
import json
import os
import atexit
# from aiohttp import web
# import socketio

def updateUserlist(channel):
    # myData = threading.local()
    # myData.terminate = False
    # while myData.terminate == False:
    print("Updating userlist")
    with urlopen("http://tmi.twitch.tv/group/user/{}/chatters".format(channel)) as url:
        data = json.loads(url.read())
        with open(".\\userlists\\" + channel + "Userlist.txt", 'w') as output:
            json.dump(data, output)
    # time.sleep(10)
    # if (channel not in activeChannels):
    #     print("Channel " + channel + " left. Exiting userlist thread")
    #     os.remove(".\\userlists\\" + channel + "Userlist.txt")
        # myData.terminate = True

def removeUserlist(channel):
    print("Channel " + channel + " left")
    os.remove(".\\userlists\\" + channel + "Userlist.txt")

def startThread(channel):
    thing = threading.Thread(target=updateUserlist, args=(channel,))
    thing.daemon = True
    thing.start()

def exitProgram():
    for channel in activeChannels:
        try:
            print("Removing file " + channel + "Userlist.txt")
            os.remove(".\\userlists\\" + channel + "Userlist.txt")
        except FileNotFoundError:
            print("File " + channel + "Userlist.txt not found")
atexit.register(exitProgram)

# network functions go here
activeChannels = []

s = socket.socket()
s.connect((irc.HOST, irc.PORT))
s.send("PASS {}\r\n".format(irc.PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(irc.NICK).encode("utf-8"))
for tag in irc.TAGS:
    s.send("CAP REQ :twitch.tv/{}\r\n".format(tag).encode("utf-8)"))
for chan in irc.CHAN:
    if chan.find("#") == -1:
        chan = "#" + chan
    s.send("JOIN {}\r\n".format(chan).encode("utf-8"))
    activeChannels.append(tokenize(chan, "#")[2])
for chan in activeChannels:
    startThread(chan)

connected = False
cTime = time.time()
while True:
    response = s.recv(1024).decode("utf-8")
    # print(response)
    if connected == False:
        loadCheck = response.find(":tmi.twitch.tv 001 omegazeron :Welcome, GLHF!")
    if loadCheck != -1 and connected == False:
        connected = True
    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
        print("Pong")
    else:
        if connected == True:
            # to check if I'm still connected
            # s.send("Ping :tmi.twitch.tv\r\n".encode("utf-8"))
            # responds with ":tmi.twitch.tv PONG tmi.twitch.tv :tmi.twitch.tv"

            # print(response)
            # (DONE IN TEST.PY) get userlist from api JSON (done here or in JS?) ex: http://tmi.twitch.tv/group/user/lirik/chatters
            if str.find(response, "PRIVMSG") != -1:
                if str.find(tokenize(response, ";")[2], "bits") != -1:
                    pass
                    # print(response)
                    # tokens = tokenize(response, ";")
                    # username = tokenize(tokens[4], "=")[2]
                    # cmSetup = tokenize(tokens[13], "#")[2]
                    # channel = tokenize(cmSetup)[1]
                    # message = tokenize(cmSetup, ":")[2]
                    # bitAmount = tokenize(tokens[2], "=")[2]
                    # print(channel + ": " + username + " used " + bitAmount + " bits!")
                else:
                    # pass
                    # TODO filter USERSTATE, ROOMSTATE for slowmode etc.
                    tokens = tokenize(response, ";")
                    badges = tokens[1]
                    username = tokenize(tokens[3], "=")[2]
                    cmSetup = tokenize(tokens[12], "#")[2]
                    channel = "#" + tokenize(cmSetup)[1]
                    message = (tokenize(cmSetup, ":")[2]).rstrip()
                    if (tokenize(message)[1] == "!tleave" and tokenize(message)[0] >= 2):
                        print("Leaving " + tokenize(message)[2])
                        activeChannels.remove(tokenize(message)[2])
                    print(channel + ": " + username + ": " + message)
                    checkMessage(s, message, username, channel, badges)
            elif str.find(response, "USERNOTICE") != -1:
                pass
                # print(response)
                # tokens = tokenize(response, ";")
                # username = tokenize(tokens[3], "=")[2]
                # channel = tokenize(tokens[18], "#")[2]
                # msgType = tokenize(tokens[8], "=")[2]
                # types: ritual (welcoming new chatters), sub, resub
                # subTime = 0
                # if msgType == "resub":
                    # subTime = tokenize(tokens[9], "=")[2]
            elif str.find(response, "JOIN") != -1 or str.find(response, "PART") != -1:
                pass # TODO joins and parts
            # elif str.find(response, "USERSTATE") != -1:
            #     pass # TODO figure out if this matters
                # print(response)

            if time.time() >= cTime + 5:
                cTime = time.time()
                for chan in activeChannels:
                    startThread(chan)
