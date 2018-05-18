# import os

# os.startfile(".\\DECtalk\\DEC\\SongofStorms.EN")
# os.system(".\\DECtalk\\DEC\\KaeporaGaebora.EN")

# --------------------------------------------------------------------------------

import ijson
from urllib.request import urlopen
import random
import json
import os

def doSomething():
    # with urlopen("http://tmi.twitch.tv/group/user/{}/chatters".format("drlupo")) as url:
    #     data = json.loads(url.read())
    #     with open("data.txt", 'w') as output:
    #         json.dump(data, output)
    with open("data.txt") as url:
        thing = list(ijson.items(url, 'chatters'))[0]
    # os.remove("data.txt")
    userlist = list()
    for part in thing['moderators']:
        userlist.append(part)
    for part in thing['staff']:
        userlist.append(part)
    for part in thing['admins']:
        userlist.append(part)
    for part in thing['global_mods']:
        userlist.append(part)
    for part in thing['viewers']:
        userlist.append(part)
    rand = random.randint(1, len(userlist))
    return userlist[rand - 1]

print("OmegaBot slaps " + doSomething() + " with an eel")