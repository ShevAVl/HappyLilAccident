from discord.ext import commands
import time
import random
import discord
import DB_handler
from util import *
from pytube import YouTube, exceptions


class CommandCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def info(self, ctx):
		try:
			commandList = getjson(r'../json/commandList.json')
			if len(commandList) == 0:
				raise Exception("commandList is empty")
			output = ""
			for command in commandList:
				output += "**" + command[0] + "** - "
				'''
				the inner loop is for the cases when a command description is 
				spread between multiple lines in json - unlikely, but possible
				'''
				for i in range(1, len(command)):
					output += command[i]
				output += "\n"
			await ctx.channel.send(output)
		except IndexError as i:
			desc = "\"" + str(i) + "\" - out of bounds while iterting json"
			await nagDev(ctx, desc)
		except OSError as o:
			desc = "\"" + str(o) + "\" - failed to open json"
			await nagDev(ctx, desc)
		except Exception as e:
			desc = "\"" + str(e) + "\" - unknown exception"
			await nagDev(ctx, desc)

	@commands.command()
	async def m308(self, ctx):
		try:
			m308_num = DB_handler.getValue('num_m308')
			if int(m308_num) == 1:
				m308_num = m308_num + " time"
			else:
				m308_num = m308_num + " times"
			await ctx.channel.send('cz has mentioned m308 ' + m308_num)
		except Exception as e:
			desc = "\"" + str(e) + "\" - unknown exception"
			await nagDev(ctx, desc)

	@commands.command()
	async def setm308(self, ctx, newValue):
		try:
			if isAdmin(ctx.author.id):
				if int(newValue) < 0:
					raise ValueError
				DB_handler.setValue('num_m308', newValue)
				await ctx.channel.send('counter changed')
			else:
				await ctx.reply("Insufficient privileges for the command")
		except OSError as o:
			desc = "\"" + str(o) + "\" - failed opening json file"
			await nagDev(ctx, desc)
		except ValueError:
			await ctx.reply('need a number >= 0')
		except Exception as e:
			desc = "\"" + str(e) + "\" - unknown exception"
			await nagDev(ctx, desc)

	@commands.command()
	async def voteinfo(self, ctx):
		try:
			await ctx.channel.send('How $vote works:')
			description = "To start a vote, you need to specify a **topic** and *1* or *more* **options**.\n"
			description += "The topic and each option can be passed in one of **2** ways:\n"
			description += "\t if a parameter as a single word, separate it from other parameters with spaces\n"
			description += "\t if a parameter has multiple words, incase it in quotes \" \"\n"
			description += "**Example:**\n"
			description += "> $vote \"Are you here?\" Yes No\n"
			await ctx.channel.send(description)
		except Exception as e:
			desc = "\"" + str(e) + "\" - unknown exception"
			await nagDev(ctx, desc)

	@commands.command()
	async def vote(self, ctx, *args):
		print('in vote')
		try:
			if len(args) == 0:
				response = "no topic or options given"
				await ctx.reply(response)
				return
			if len(args[0].replace(" ", "")) == 0:
				response = "received a blank topic"
				await ctx.reply(response)
				return
			if len(args) == 1:
				response = "no voting options given"
				await ctx.reply(response)
				return
			if len(args) > 11:
				response = f"the amount of voting options is limited by *10*, received: *{len(args)}*"
				await ctx.reply(response)
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
			desc = "\"" + str(e) + "\" - unknown exception"
			await nagDev(ctx, desc)

	@commands.command()
	async def tomp4(self, ctx):
		if ctx.message.reference is None:
			await ctx.reply('call the command as a reply to the video')
			return
		try:
			sourceMsg = await ctx.fetch_message(ctx.message.reference.message_id)
			yt = YouTube(f'{sourceMsg.content}', use_oauth=False, allow_oauth_cache=False)
		except exceptions.VideoUnavailable as e:
			await ctx.reply('Video is unavailable')
			return
		except exceptions.RegexMatchError as r:
			await ctx.channel.send('No link in the replied message')
			return
		except Exception as e:
			desc = "\"" + str(e) + "\" - failed to process a yt link (unknown exception)"
			await nagDev(ctx, desc)
			return
		streams = yt.streams.filter(progressive=True)
		for stream in reversed(streams):
			if stream.filesize < 8 * 1024 * 1024:
				try:
					reply = await ctx.channel.send("Found the video, downloading")
					title = yt.title
					path = getPath('../downloaded/')
					filename = f'{title}.mp4'
					stream.download(path, filename=filename)
					await reply.edit(content='', attachments=[discord.File(path+filename)]);
					os.remove(path + filename)
					return
				except FileNotFoundError as fnfe:
					desc = "\"" + str(e) + "\" - downloaded mp4 not found"
					await nagDev(ctx, desc)
					return
				except exceptions.VideoUnavailable:
					await ctx.channel.send('Video is unavailable, cannot download')
					return
				except Exception as e:
					desc = "\"" + str(e) + "\" - failed after downloading an mp4 (unknown exception)"
					await nagDev(ctx, desc)
					return
		await ctx.reply("No file under 8 Mb found")

	@commands.command()
	async def pdth(self, ctx):
		try:
			procCode = getLobbies(getPath('../PDTracker_dir/PDTracker'))
			if procCode == 0:
				thread = await ctx.message.create_thread(name=f"PDTH lobbies", auto_archive_duration=60)
				await thread.add_user(ctx.author)
				lobbies = parseLobbies()
				reply = '';
				for lobby in lobbies:
					reply  += "```\n"
					reply += lobby + '\n'
					reply  += "```\n"
				await thread.send(content=reply)
			elif procCode == -3:
				await ctx.channel.send("No vacant lobbies found")
			else:
				desc = "Unexpected exit code for the executable"
				await nagDev(ctx, desc)
		except Exception as e:
			desc = "\"" + str(e) + "\" - unknown exception"
			await nagDev(ctx, desc)

	@commands.command()
	async def gen(self, ctx):
		try:
			msg = await ctx.channel.send('.')
			time.sleep(0.20)
			for i in range(2,4):
				await msg.edit(content='.'*i)
				time.sleep(0.20)
			await msg.edit(content=random.randint(1,100))
		except Exception as e:
			desc = "\"" + str(e) + "\" - unknown exception"
			await nagDev(ctx, desc)

async def setup(bot):
	await bot.add_cog(CommandCog(bot))