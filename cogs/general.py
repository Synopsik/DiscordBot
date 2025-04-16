from discord.ext import commands
from cogs.logging import get_formatted_time

class GeneralCog(commands.Cog, name="General"):
    def __init__(self, bot, logger):
        self.logger = logger
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.debug("Loaded General Cog")


    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")


    @commands.command(name="hello")
    async def greet(self, ctx):
        await ctx.send("Hi!")


    async def dm(self, ctx, message):
        try:
            await ctx.author.send(message)
            self.logger.info(f"{self.bot.user} sent a DM to {ctx.author}")
        except Exception as e:
            self.logger.error(f"Error sending direct message: {e}")