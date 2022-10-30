import discord
from discord.ext import commands
import DB_handler

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix='$')

@bot.command()
async def ctxinfo(ctx):
    await ctx.send(ctx.guild)
    await ctx.send(ctx.author)
    await ctx.send(ctx.message.id)
    await ctx.send(ctx.channel.name)

@bot.command()
async def info(ctx):
    await ctx.send('Hi. I\'m a happy little accident made in place of tons of other, curricular activities')

@bot.command()
async def m308(ctx):
    try:
        await ctx.channel.send('cz has mentioned m308 ' + str(DB_handler.getValue('num_m308')) + ' times')
    except BaseException as e:
        print("Caught an exception " + str(e) + "while executing command $m308")

bot.run(DB_handler.getValue('bot_token'))
