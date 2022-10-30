import discord
from discord.ext import commands
import re # - regex
import DB_handler  # - list of functions for interaction with the DB

##############################################
#   initiating base parameters for the bot   #
##############################################
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix="$")

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
                await message.channel.send('Found match \'' + match[0] + '\' in message \'' + message.content + '\'')
                await bot.process_commands(message)
            except BaseException as e:
                print("Caught an exception " + str(e) + " while searching for m308 mentions")
        return

#######################
#   command section   #
#######################
@bot.command()
async def ctxinfo(ctx):
    '''
    $ctxinfo - debug command to output all the info about the msg context
    '''
    await ctx.send(ctx.guild)
    await ctx.send(ctx.author)
    await ctx.send(ctx.message.id)
    await ctx.send(ctx.channel.name)

@bot.command()
async def info(ctx):
    '''
    $info - bot's self introduction
    '''
    await ctx.send('Hi. I\'m a happy little accident made in place of tons of other, curricular activities')

@bot.command()
async def m308(ctx):
    '''
    $m308 - tells how many times cz mentioned m308 in all
    public channels and threads
    '''
    try:
        await ctx.channel.send('cz has mentioned m308 ' + str(DB_handler.getValue('num_m308')) + ' times')
    except BaseException as e:
        print("Caught an exception " + str(e) + "while executing command $m308")

#######################
#   running the bot   #
#######################
bot.run(DB_handler.getValue('bot_token'))
