import asyncio
import discord
from discord.ext import commands
from cogs.logging import get_formatted_time

class GeneralCog(commands.Cog, name="General"):
    def __init__(self, bot, logger):
        self.logger = logger
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.debug("Loaded General Cog")

    # ------------------------------------------------------------------------------------------------------
    # General
    # ------------------------------------------------------------------------------------------------------

    @commands.command(name="ping")
    async def ping(self, ctx):
        try:
            await ctx.typing() # Imitate typing for half a second
            await asyncio.sleep(0.5)
            await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms") # Then send message
        except Exception as e:
            self.logger.error(f"Error pinging: {e}")

    @commands.command(name="hello")
    async def greet(self, ctx):
        try:
            await ctx.typing() # Imitate typing for half a second
            await asyncio.sleep(0.5)
            await ctx.send("Hi!") # Then send message
        except Exception as e:
            self.logger.error(f"Error greeting: {e}")

    # ------------------------------------------------------------------------------------------------------
    # Messages
    # ------------------------------------------------------------------------------------------------------

    @commands.command(name="clear_dm")
    async def clear_dm(self, ctx):
        # I want to update this so that you can pass an optional arg for a member (self, ctx, *member)
        # this way admins can clear bot messages from users
        try:
            if isinstance(ctx.channel, discord.DMChannel): # If the channel this is called from is a DM channel
                async for message in ctx.channel.history(limit=None): # Loop through all messages
                    if message.author == self.bot.user:
                        await message.delete() # Delete all where the bot is the author
            else:
                # Not instance of DM channel
                await ctx.send("This command cannot be used in a server channel.")
        except Exception as e:
            # Something catastrophic happened
            self.logger.error(f"Error clearing direct messages: {e}")
