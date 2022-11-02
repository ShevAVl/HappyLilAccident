import setup
import re
import discord
from discord.ext import commands
import DB_handler
from pytube import YouTube, exceptions
from auxiliary import *


##############################################
#   initiating base parameters for the bot   #
##############################################

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix="$")
bot.activity = discord.Activity(type=discord.ActivityType.listening, name="$commands")


#####################
#   event section   #
#####################

@bot.event
async def on_ready():
    print('Bot \'{0.user}\''.format(bot) + ' is up!')
@bot.event
async def on_message(message):
    print('tracin')
    # if a message belongs to the bot - ignore
    if message.author == bot.user:
        await bot.process_commands(message)
        return
    #  if the author is the specified user - handle the message
    if message.author.id == int(DB_handler.getValue('userid_me')):
        match = re.search(r'\$?[Mm] ?308', message.content)
        # if found a pattern match
        if match:
            print('match')
            if match[0][0] == '$':
                await bot.process_commands(message)
                return
            try:
                DB_handler.incNum('num_m308')
                await bot.process_commands(message)
            except BaseException as e:
                print("Caught an exception " + str(e) + " while searching for m308 mentions")
            return
    await bot.process_commands(message)


#######################
#   command section   #
#######################

@bot.command()
async def commands(ctx):
    try:
        print('in commands')
        commandlist = getjson(r'../json/commandlist.json')
        for command in commandlist:
            output = "*" + command[0] + "* - "
            for i in range(1, len(command)):
                output += command[i]
            await ctx.channel.send(output)
    except IndexError as i:
        print("\"" + str(i) + "\" - out of bounds while executing command $m308")
        await nagDev(ctx)
    except OSError as o:
        print("\"" + str(o) + "\" - failed to open json while executing command $m308")
        await nagDev(ctx)
    except Exception as e:
        print("\"" + str(e) + "\" - an unknown exception while executing command $m308")
        await nagDev(ctx)
@bot.command()
async def m308(ctx):
    try:
        m308_num = DB_handler.getValue('num_m308')
        if int(m308_num) == 1:
            m308_num = m308_num + " time"
        else:
            m308_num = m308_num + " times"
        await ctx.channel.send('cz has mentioned m308 ' + m308_num)
    except Exception as e:
        print("Caught an exception " + str(e) + "while executing command $m308")
        await nagDev(ctx)
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
    except OSError as o:
        print("Failed opening json file: \"" + str(o) + "\"")
        await nagDev(ctx)
    except ValueError:
        await ctx.reply('need a number >= 0')
    '''
    except Exception as e:
        print("Caught an exception: \"" + str(e) + "\" while changing m308 index")
        await nagDev(ctx)
    '''
@bot.command()
async def voteinfo(ctx):
    try:
        await ctx.channel.send('How $vote works:')
        description = "To start a vote, you need to specify a topic and **1** or **more** options.\n"
        description += "The topic and each option can be passed in one of **2** ways:\n"
        description += "\t if a parameter as a single word, separate it from other parameters with spaces\n"
        description += "\t if a parameter has multiple words, incase it in quotes \" \"\n"
        description += "**Example:**\n"
        description += "> $vote \"Are you here?\" Yes No\n"
        await ctx.channel.send(description)
    except Exception as e:
        await nagDev(ctx)
@bot.command()
async def vote(ctx, *args):
    print('in vote')
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
    except Exception as e:
        print('Something went wrong during voting')
        await nagDev(ctx)
@bot.command()
async def tomp4(ctx):
    if ctx.message.reference is None:
        await ctx.reply('call the command as a reply to the video')
        return
    try:
        sourceMsg = await ctx.fetch_message(ctx.message.reference.message_id)
        yt = YouTube(f'{sourceMsg.content}', use_oauth=False, allow_oauth_cache=False)
    except exceptions.VideoUnavailable as e:
        await ctx.reply('Video is unavailable')
        return
    except re.RegexMatchError as r:
        ctx.channel.send('No link in the replied message')
        return
    except Exception as e:
        print('Oppsie, got a: \"' + (str(e) + '\"'))
        await nagDev(ctx)
        return

    streams = yt.streams.filter(progressive=True)
    for stream in reversed(streams):
        if stream.filesize < 8 * 1024 * 1024:
            try:
                await ctx.channel.send("Found the video, downloading")
                title = yt.title
                path = getPath('../downloaded/')
                filename = f'{title}.mp4'
                stream.download(path, filename=filename)
                await ctx.reply(file=discord.File(path + filename))
                #os.remove(path + filename)
                return
            except FileNotFoundError:
                print('File not found, explain')
                await nagDev(ctx)
                return
            except exceptions.VideoUnavailable:
                await ctx.reply('Video is unavailable, cannot download')
                return
            except Exception as e:
                print("*something* went wrong")
                await nagDev(ctx)
                return
    await ctx.reply("No file under 8 Mb found")
@bot.command()
async def pdth(ctx):
    await ctx.channel.send("to be implemented")


#######################
#   running the bot   #
#######################

bot.run(getEnv("BOT_TOKEN"))