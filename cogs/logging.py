import datetime
from discord.ext import commands

class LoggingCog(commands.Cog, name="Logging"):
    def __init__(self, bot, conn):
        self.bot = bot
        self.conn = conn
        self.curr = conn.cursor()


    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        try:
            self.curr.execute("INSERT INTO logs (user_id, command, timestamp) VALUES (?, ?, ?)",
                             (ctx.author.id, ctx.command.qualified_name, datetime.datetime.utcnow().isoformat()))
            self.conn.commit()
        except Exception as e:
            print(f"[LoggingCog] Failed to log command: {e}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        try:
            self.curr.execute("INSERT INTO logs (user_id, command, timestamp) VALUES (?, ?, ?)",)
        except Exception as e:
            print(f"[LoggingCog] Failed to log command error: {e}")

