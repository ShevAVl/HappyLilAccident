from discord.ext import commands
import re
import util
import DB_handler


class EventCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		print('Bot \'{0.user}\''.format(self.bot) + ' is up!')

	@commands.Cog.listener()
	async def on_message(self, message):
		# if a message belongs to the bot - ignore
		if message.author == self.bot.user:
			return
		# if the author is the specified user - handle the message
		if message.author.id == int(DB_handler.getValue('userid_cz')):
			match = re.search(r'\$?[Mm] ?308', message.content)
			# if found a pattern match
			if match:
				if match[0][0] == '$':
					return
				try:
					DB_handler.incNum('num_m308')
				except Exception as e:
					desc = 'on_message\n' + "Error: " +  str(e)
					print(desc)
					await nagDev(ctx, desc, e)

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if payload.member.name == self.bot.user.name:
			return
		if str(payload.emoji) == '🐟':
			channel = self.bot.get_channel(payload.channel_id)
			msg = await channel.fetch_message(payload.message_id)
			await msg.add_reaction('🐟')

async def setup(bot):
	await bot.add_cog(EventCog(bot))