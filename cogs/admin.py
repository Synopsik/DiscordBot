import discord
from discord.ext import commands

class AdminCog(commands.Cog, name="Admin"):
    def __init__(self, bot, logger):
        self.bot = bot
        self.logger = logger

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.debug("Loaded Admin Cog")

    @commands.command(name="clear_dm")
    async def clear_dm(self, ctx, member: discord.Member):
        if member.name == 'synopsik':
            dm_channel = await member.create_dm()  # Get or create the DM channel with the member
            async for message in dm_channel.history(limit=None):  # Fetch all message history in the DM
                if message.author == self.bot.user:  # Check if the message was sent by the bot
                    await message.delete()  # Delete the message
        else:
            print(member.name)