import random
import irc
import math

def checkMessage(s, message, username, chan):
    if message.startswith("!tpun"):
        pun(s, chan)
    elif message.startswith("!tslot"):
        slots(s, chan)
    elif message.startswith("!troll"):
        roll(s, message, username, chan)

def me(thing):
    print("OmegaBot: " + thing)

def chat(sock, msg, chan):
    sock.send("PRIVMSG {} :{}\r\n".format(chan, msg).encode())

def checkFileCount(file):
    count = 0
    done = False
    while done == False:
        if file.readline() != "":
            count += 1
        else:
            done = True
    file.close
    return count

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
    me(output)
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
    me(final)
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
        me(final)
        chat(s, final, chan)
