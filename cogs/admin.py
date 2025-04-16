import discord
from discord.ext import commands

class AdminCog(commands.Cog, name="Admin"):
    def __init__(self, bot, logger):
        self.bot = bot
        self.logger = logger

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.debug("Loaded Admin Cog")

    @commands.command(name="clear_channel")
    async def clear_channel(self, ctx):
        try:
            if not isinstance(ctx.channel, discord.DMChannel):  # Ensure the command is not executed in a DM channel
                await ctx.channel.purge(limit=None) # Purge channel
            else:
                await ctx.send("This command cannot be used in direct messages.")
        except Exception as e:
            self.logger.error(f"Error clearing channel: {e}")