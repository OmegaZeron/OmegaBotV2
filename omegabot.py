import socket
# import re
import irc
import commands
# from aiohttp import web
# import socketio

#CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

# network functions go here
s = socket.socket()
s.connect((irc.HOST, irc.PORT))
s.send("PASS {}\r\n".format(irc.PASS).encode("utf-8"))
s.send("NICK {}\r\n".format(irc.NICK).encode("utf-8"))
for tag in irc.TAGS:
    s.send("CAP REQ :twitch.tv/{}\r\n".format(tag).encode("utf-8)"))
for chan in irc.CHAN:
    s.send("JOIN {}\r\n".format(chan).encode("utf-8"))

connected = False
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
            print(response)
            # EONL = response.find("End of /NAMES list")
            # JOIN = response.find("twitch.tv JOIN #")
            # if EONL == -1 and JOIN == -1:
            # (DONE IN TEST.PY) get userlist from api JSON (done here or in JS?) ex: http://tmi.twitch.tv/group/user/lirik/chatters
            if str.find(response, "PRIVMSG") != -1:
                # TODO filter USERSTATE, ROOMSTATE for slowmode etc.
                tokens = commands.tokenize(response, ";")
                badges = tokens[1]
                username = commands.tokenize(tokens[3], "=")[2]
                cmSetup = commands.tokenize(tokens[12], "#")[2]
                channel = "#" + commands.tokenize(cmSetup)[1]
                message = (commands.tokenize(cmSetup, ":")[2]).rstrip()
                print(channel + ": " + username + ": " + message)
                commands.checkMessage(s, message, username, channel, badges)
            elif str.find(response, "USERNOTICE") != -1:
                pass # TODO subscription things
            elif str.find(response, "JOIN") != -1 or str.find(response, "PART") != -1:
                pass # TODO joins and parts
            elif str.find(response, "USERSTATE") != -1:
                pass # TODO figure out if this matters
