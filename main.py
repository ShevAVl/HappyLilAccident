import discord
from discord.ext import commands
import os
import re
#import DB_handler  # - list of functions for intecraction with the DB

##############################################
#   initiating base parameters for the bot   #
##############################################
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(intents=intents, command_prefix="$")


# client = discord.Client(intents=intents)

# a simple welcome message in console
@client.event
async def on_ready():
    print('Bot \'{0.user}\''.format(client) + ' is up!')


# catching messages from a specified user to find any mentions of m308
# (could make a standalone function)
'''@client.event
async def on_message(message):
    # if a message belongs to the bot - ignore
    if message.author == client.user:
        await client.process_commands(message)
        return
    #  if the author is the specified user - handle the message
    if message.author.id == int(os.getenv("id_me")):  # os.getenv("id_cz")
        match = re.search(r'\$?[Mm] ?308', message.content)
        # if found a pattern match
        if match:
            if match[0][0] == '$':
                await client.process_commands(message)
                return
            try:
                DB_handler.incNum('num_m308')
                await message.channel.send('Found match \'' + match[0] + '\' in message \'' + message.content + '\'')
                await client.process_commands(message)
            except BaseException as e:
                print("Caught an exception " + str(e) + " while searching for m308 mentions")
        return


#######################
#   command section   #
#######################
@client.command()
async def m308(ctx):
    if type(DB_handler.getValue('num_m308')) == int:
        await ctx.channel.send('cz has mentioned m308 ' + str(DB_handler.getValue('num_m308')) + ' times')
    else:
        print('an exception while executing command $m308')


#######################
#   running the bot   #
#######################
'''
client.run("MTAzNTA0Nzk5NDEwNzY0NjAwMg.G73TGD.ysdzNOMGDh8hJsn0nBQLyBIyxGpzWSli9MI4u0")