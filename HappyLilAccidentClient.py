import discord
from discord.ext import commands


class MyClient(commands.Bot):
    def __init__(selfself, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print("Ayo ready")

