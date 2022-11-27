import setup
import asyncio
import discord
from util import *
from discord.ext import commands


##############################################
#   initiating base parameters for the bot   #
##############################################

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix="$")
bot.activity = discord.Activity(type=discord.ActivityType.listening, name="$info")


#######################
#   running the bot   #
#######################

async def main():
    async with bot:
        cogs = getjson('../json/cogs.json')
        for cog in cogs:
            await bot.load_extension(cog)
        await bot.start(getEnv("BOT_TOKEN"))
asyncio.run(main())
