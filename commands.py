import random
import irc
import math
import win32com.client

# TODO get userlist

def checkMessage(s, message, username, chan, badges):
    if tokenize(message)[1] == "!tpun":
        pun(s, chan)
    elif tokenize(message)[1] == "!tslot":
        slots(s, chan)
    elif tokenize(message)[1] == "!troll" and tokenize(message)[0] >= 3:
        roll(s, message, username, chan)
    elif tokenize(message)[1] == "!ttts" and tokenize(message)[0] >= 2:
        tts(username, message)
    elif tokenize(message)[1] == "!tban" and tokenize(message)[0] >= 2:
        ban(s, message, username, chan)

def tokenize(message, token = " "):
    output = message.split(token)
    output.insert(0, len(output))
    return output

def isMod(badge):
    if "moderator/1" in badge or "broadcaster/1" in badge:
        return True
    return False

def me(thing, place):
    print(place + ": OmegaBot: " + thing)

def chat(sock, msg, chan):
    me(msg, chan)
    sock.send("PRIVMSG {} :{}\r\n".format(chan, msg).encode())

def checkFileCount(file):
    count = 0
    done = False
    while done == False:
        if file.readline() != "":
            count += 1
        else:
            done = True
    file.close()
    return count

def tts(username, message):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.speak(username + " says " + message)

def ban(s, message, username, chan):
    tokens = tokenize(message)
    if tokens[2] == username:
        chat(s, "Yeah I'd ban them too, seems like a dingus OpieOP", chan)
    else:
        chat(s, "Now why would you want to do that? " + tokens[2] + " seems like a cool cat, unlike you, " + username + " Jebaited", chan)

def pun(s, chan):
    count = checkFileCount(open("puns.txt"))
    rand = random.randint(1, count)
    puns = open("puns.txt")
    i = 0
    while i < rand:
        i += 1
        if i == rand:
            output = puns.readline()
        else:
            puns.readline()
    puns.close()
    chat(s, output, chan)

def slots(s, chan):
    count = checkFileCount(open("slots.txt"))

    def randSlot():
        i = 0
        rand = random.randint(1, count)
        slots = open("slots.txt")
        output = ""
        while i < rand:
            i += 1
            if i == rand:
                output = slots.readline()
            else:
                slots.readline()
        slots.close()
        output = output.rstrip('\n')
        return output
        
    slot1 = randSlot()
    slot2 = randSlot()
    slot3 = randSlot()
    final = slot1 + " | " + slot2 + " | " + slot3
    chat(s, final, chan)

def roll(s, message, user, chan):
    start,roll1,roll2 = message.split()
    del start
    roll1 = int(roll1)
    roll2 = int(roll2)

    def countNumLength(num):
        digits = int(math.log10(num))+1
        return digits

    if roll1 >= 1 and countNumLength(roll1) <= 4 and roll2 >= 2 and countNumLength(roll2) <= 4:
        rand = 0
        for x in range(0, roll1):
            rand += random.randint(1, roll2)
        del x
        final = user + " rolled " + str(roll1) + " " + str(roll2) + "-sided" + (" die " if roll1 == 1 else " dice ") + "for a total of " + str(rand)
        chat(s, final, chan)
