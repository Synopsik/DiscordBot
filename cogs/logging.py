import datetime
from discord.ext import commands
from utilities.database_utils import list_tables_and_columns, init_db_tables

class LoggingCog(commands.Cog, name="Logging"):
    def __init__(self, bot, conn):
        self.bot = bot
        self.db_pool = conn

    @commands.Cog.listener()
    async def on_ready(self):
        print("Log Cog Ready")
        await init_db_tables(self.db_pool)
        await list_tables_and_columns(self.db_pool)

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):


        try :
            #self.curr.execute("INSERT INTO logs (user_id, command, timestamp) VALUES (?, ?, ?)",
            #                 (ctx.author.id, ctx.command.qualified_name, datetime.datetime.utcnow().isoformat()))
            #self.conn.commit()
            print("command completed")
        except Exception as e:
            print(f"[LoggingCog] Failed to log command: {e}")


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print("Command error:", error)

        if isinstance(error, commands.CommandNotFound):
            return
        try:
            # self.curr.execute("INSERT INTO logs (user_id, command, timestamp) VALUES (?, ?, ?)",)
            print("command error")
        except Exception as e:
            print(f"[LoggingCog] Failed to log command error: {e}")


