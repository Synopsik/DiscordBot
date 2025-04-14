import os
from utilities.logging_utils import setup_logging
import asyncio
import asyncpg
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
load_dotenv()

from cogs.games import GamesCog
from cogs.general import GeneralCog
from cogs.logging import LoggingCog, get_formatted_time
from cogs.mentor import MentorCog


def start_bot():
    DiscordBot("general", "games", "logging")


class DiscordBot(commands.Bot):
    def __init__(self, *cogs):
        self.db_pool = None
        self.cogs_list = cogs
        # Configure intents here
        intents = discord.Intents.default()
        intents.presences = True
        intents.members = True
        intents.message_content = True
        self.logger = None
        description = "A Discord bot that does stuff."
        self.prefix = "!"
        super().__init__(command_prefix=self.prefix,
                         intents=intents,
                         description=description)

        self.run(os.getenv("BOT_TOKEN"))

    async def setup_hook(self):
        db_url = os.getenv("DB_URL")
        db_connected = False
        if db_url:
            try:
                self.db_pool = await asyncpg.create_pool(dsn=db_url)
                db_connected = True
            except OSError as e:
                print(f"Failed to connect to the database. Error: {e}")
                self.db_pool = None
        else:
            print("No DB_URL found. Skipping database connection.")

        try:
            loop = asyncio.get_running_loop()
            self.logger = setup_logging(self.db_pool, loop, __name__, logging.DEBUG, "logs")

            if db_connected:
                self.logger.debug("Database connection successful.")
        except Exception as e:
            print(f"Failed to configure logger. Error: {e}")


        for cog in self.cogs_list:
            match cog:
                case "general":
                    await self.add_cog(GeneralCog(self, self.logger))
                case "games":
                    await self.add_cog(GamesCog(self, self.logger))
                case "logging":
                    if self.db_pool is not None:
                        await self.add_cog(LoggingCog(self, self.logger))
                case "mentor":
                    if self.db_pool is not None:
                        await self.add_cog(MentorCog(self, self.db_pool, self.logger))
                case _:
                    print("Couldn't find cog.")

    async def on_ready(self):
        self.logger.debug(f"Logged in as {self.user} (ID: {self.user.id})")



    async def close(self):
        if self.db_pool is not None:
            if hasattr(self, "db_pool"):
                await self.db_pool.close()
        await super().close()
