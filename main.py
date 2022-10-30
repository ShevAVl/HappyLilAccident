import discord
from discord.ext import commands
import re  # - regex
import DB_handler  # - list of functions for interaction with the DB
#import HappyLilAccidentClient

##############################################
#   initiating base parameters for the bot   #
##############################################
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix="$")
bot.activity = discord.Activity(type=discord.ActivityType.listening, name="$commands")

#bot = HappyLilAccidentClient(intents=intents, command_prefix="$")

#####################
#   event section   #
#####################
@bot.event
async def on_ready():
    '''
    a signal that is bot is up and ready to accept input
    '''
    print('Bot \'{0.user}\''.format(bot) + ' is up!')
async def on_message(message):
    '''
    a general function to process all and any messages (might need a rewamp)
    '''
    # if a message belongs to the bot - ignore
    if message.author == bot.user:
        await bot.process_commands(message)
        return
    #  if the author is the specified user - handle the message
    if message.author.id == int(DB_handler.getValue('userid_me')):
        match = re.search(r'\$?[Mm] ?308', message.content)
        # if found a pattern match
        if match:
            if match[0][0] == '$':
                await bot.process_commands(message)
                return
            try:
                DB_handler.incNum('num_m308')
                #await message.channel.send('Found match \'' + match[0] + '\' in message \'' + message.content + '\'')
                await bot.process_commands(message)
            except BaseException as e:
                print("Caught an exception " + str(e) + " while searching for m308 mentions")
        return

#######################
#   command section   #
#######################
@bot.command()
async def commands(ctx):
    '''
    $commands - outputs the list of all supported commands
    '''
    await ctx.channel.send("*$commands* - list of all commands")
    await ctx.channel.send("*$info* - bot's self introduction")
    await ctx.channel.send("*$m308* - schizo index")
    await ctx.channel.send("*$ctxinfo* - bedug command for msg ctx info")
    await ctx.channel.send("*$vote* - starts a vote with received parameters")
    await ctx.channel.send("*$voteinfo* - in-depth description of how $vote works")
@bot.command()
async def ctxinfo(ctx):
    '''
    $ctxinfo - debug command to output all the info about the msg context
    '''
    print('ctxinfo invoked')
    await ctx.channel.send(ctx.guild)
    await ctx.channel.send(ctx.author)
    await ctx.channel.send(ctx.message.id)
    await ctx.channel.send(ctx.channel.name)
@bot.command()
async def info(ctx):
    '''
    $info - bot's self introduction
    '''
    await ctx.channel.send('Hi. I\'m a happy little accident made in place of tons of other, curricular activities')
@bot.command()
async def m308(ctx):
    '''
    $m308 - tells how many times cz mentioned m308 in all
    public channels and threads
    '''
    try:
        m308_num = DB_handler.getValue('num_m308')
        if int(m308_num) == 1:
            m308_num = m308_num + " time"
        else:
            m308_num = m308_num + " times"
        await ctx.channel.send('cz has mentioned m308 ' + m308_num)
    except BaseException as e:
        print("Caught an exception " + str(e) + "while executing command $m308")
        user = ctx.guild.fetch_member(DB_handler.getValue('userid_me'))
        await ctx.channel.send(f"{user.mention} go check the logs")
@bot.command()
async def setm308(ctx, newValue):
    try:
        if isAdmin(ctx.author.id):
            if int(newValue) < 0:
                raise ValueError
            DB_handler.setValue('num_m308', newValue)
            await ctx.channel.send('counter changed')
        else:
            await ctx.reply("Insufficient privileges, can't touch that command")
    except ValueError:
        await ctx.reply('need a number >= 0')
    except Exception as e:
        print("Caught an exception " + str(e) + "while changing m308 index")
        user = ctx.guild.fetch_member(DB_handler.getValue('userid_me'))
        await ctx.channel.send(f"{user.mention} go check the logs")

###########################
#   auxiliary functions   #
###########################

def isAdmin(userid):
    try:
        if str(userid) == DB_handler.getValue('userid_me') or userid == DB_handler.getValue('userid_lost'):
            print('yep, admin id')
            return True
        else:
            print('no, not an admin id')
            return False
    except Exception:
        print('couldn\'t fetch the ids')
        return False

@bot.command()
async def dm(ctx):
    await ctx.author.send("hi")

@bot.command()
async def voteinfo(ctx):
    try:
        await ctx.channel.send('How $vote works:')
        description = "To start a vote, you need to specify a topic and **1** or **more** options.\n"
        description += "The topic and each option can be passed in one of *2* ways:\n"
        description += "\t if a parameter as a single word, just separate it from other parameters with spaces, no quotes needed\n"
        description += "\t if a parameter has multiple words, incase it in quotes \" \"\n"
        description += "**Example:**\n"
        description += "> $vote \"Are you here?\" Yes No\n"
        await ctx.channel.send(description)
    except Exception as e:
        user = ctx.guild.fetch_member(DB_handler.getValue('userid_me'))
        await ctx.channel.send(f"{user.mention} go check the logs")
@bot.command()
async def vote(ctx, *args):
    try:
        if len(args) == 0:
            response = "topic, options - where's all that?"
            await ctx.channel.send(f"{ctx.author.mention}, " + response)
            return
        if len(args[0].replace(" ", "")) == 0:
            response = "can't accept a blank topic"
            await ctx.channel.send(f"{ctx.author.mention}, " + response)
            return
        if len(args) == 1:
            response = "can't see a single voting option"
            await ctx.channel.send(f"{ctx.author.mention}, " + response)
            return

        argsNum = len(args)
        for i in range(1, argsNum):
            if len(args[i].replace(" ", "")) == 0:
                response = f"option #{i} is blank, can't have that"
                await ctx.channel.send(f"{ctx.author.mention}, " + response)
                return

        topic = args[0]
        await ctx.channel.send(f"**{topic}**")
        for i in range(1, argsNum):
            await ctx.channel.send(f"> {i}) {args[i]}")
    except BaseException as e:
        user = ctx.guild.fetch_member(DB_handler.getValue('userid_me'))
        await ctx.channel.send(f"{user.mention} go check the logs")



#######################
#   running the bot   #
#######################
bot.run(DB_handler.getValue('bot_token'))
