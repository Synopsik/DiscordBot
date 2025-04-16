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
    async def clear_dm(self, ctx): # I want to update this so that you can pass an optional arg for a member
        try:
            if isinstance(ctx.channel, discord.DMChannel):
                async for message in ctx.channel.history(limit=None):
                    if message.author == self.bot.user:
                        await message.delete()
            else:
                await ctx.send("This command cannot be used in a server channel.")
        except Exception as e:
            self.logger.error(f"Error clearing direct messages: {e}")

    @commands.command(name="clear_channel")
    async def clear_channel(self, ctx): # I want to update this so that you can pass an optional arg for a member
        try:
            if not isinstance(ctx.channel, discord.DMChannel):  # Ensure the command is not executed in a DM channel
                await ctx.channel.purge(limit=None) # Purge channel
            else:
                await ctx.send("This command cannot be used in direct messages.")
        except Exception as e:
            self.logger.error(f"Error clearing channel: {e}")