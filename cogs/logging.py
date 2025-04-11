import datetime
from discord.ext import commands
from utilities.database_utils import list_tables_and_columns, init_db_tables, update_single_user
from utilities.logging_utils import setup_logging
import asyncio
import logging




async def get_time():
    dt = datetime.datetime.now()
    return dt.strftime('%Y-%m-%d %H:%M:%S')



class LoggingCog(commands.Cog, name="Logging"):
    def __init__(self, bot, conn):
        self.bot = bot
        self.db_pool = conn
        loop = asyncio.get_running_loop()
        self.logger = setup_logging(conn, loop, __name__, logging.DEBUG, "logs")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[{await get_time()}] [EVENT] Loaded Log Cog")



    # Messages ---------------------------------------------------------------------------------------


    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author == self.bot.user:
            print(f"MSG: {message.content}")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        print(f"{message.author.name} has deleted a message: {message.content}")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        print(f"{before.author.name} has edited a message: {before.content} -> {after.content}")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        print(f"{user.name} has added a reaction to a message: {reaction.emoji}")


    # Members ---------------------------------------------------------------------------------------


    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"{member.name} just joined the server!")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f"{member.name} just left the server!")

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        print(f"{before.name} has changed their nickname to {after.name}")

    # Commands ---------------------------------------------------------------------------------------


    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        print(f"Command completed: {ctx.command}")


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(f"Command error: {error}")



