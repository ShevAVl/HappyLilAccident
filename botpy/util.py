import json
import os
import datetime
from PDTH_data_types import *


'''Non-discord related functions for general purposes''' # Will move it to a new client class in a separate block

now = datetime.datetime.now().strftime("%Y.%m.%d, %H:%M")

def getEnv(key):
    return os.environ.get(key)

def getPath(path):
    return os.path.join(os.path.dirname(__file__), path)

def getjson(path):
    jsonPath = os.path.join(os.path.dirname(__file__), path)
    with open(jsonPath) as f:
        output = json.load(f)
    return output

def getLobbies(path):
    status = os.system(path)
    return status

def parseLobbies():
    f = open(getPath("../lobbies.txt"), "r")
    lobbies = []
    line = f.readline().rstrip('\n')
    while line:
        values = []
        for i in range (1,6):
            values.append(line)
            line = f.readline().rstrip('\n')
        values[0]=difficulties[values[0]]
        values[1]=maps[values[1]]
        values[4]=states[values[4]]
        lobby = f"{values[1]}\n"
        lobby += f"{values[0]}\n"
        lobby += f"Players: {values[2]}\n"
        lobby += f"Owner: {values[3]}\n"
        lobby += f"State: {values[4]}\n"
        lobbies.append(lobby)
    f.close
    return lobbies

def isAdmin(userid):
    users = getjson(r"../json/privilegedUsers.json")
    users = users.values()
    for user in users:
        if user == userid:
             return True
    return False

async def nagDev(ctx, desc=''):
    # no logging.
    report = f"Time: {now}\n"
    report += f"Server: {ctx.guild.name}\n"
    report += f"Command: {ctx.invoked_with}\n"
    if len(desc) != 0:
        report += f"Context: {desc}"
    print(report)