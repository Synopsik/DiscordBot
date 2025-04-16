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
    DiscordBot("general", "games", "logging", "mentor")


class DiscordBot(commands.Bot):
    def __init__(self, *cogs):
        self.db_pool = None
        self.logger = None
        self.cogs_list = cogs
        self.prefix = "!"
        description = "A Discord bot that does stuff."
        # Configure intents here
        intents = discord.Intents.default()
        intents.presences = True
        intents.members = True
        intents.message_content = True
        # Make sure we are running the Parent init method
        super().__init__(command_prefix=self.prefix,
                         intents=intents,
                         description=description)
        # Run bot through init method after configuring
        self.run(os.getenv("BOT_TOKEN"))


    async def setup_hook(self):
        # Get db url from .env
        db_url = os.getenv("DB_URL")
        db_connected = False
        if db_url:
            try:
                # If db_url is valid try connecting to the db
                self.db_pool = await asyncpg.create_pool(dsn=db_url)
                # Set db_connected true so when our logger init's we can display status
                db_connected = True
            except OSError as e:
                # Otherwise failed and db_connected stays false
                print(f"Failed to connect to the database. Error: {e}")
                self.db_pool = None
        else:
            print("No DB_URL found. Skipping database connection.")

        try:
            # Get a reference to the current async loop
            loop = asyncio.get_running_loop()
            # Init logger
            self.logger = setup_logging(self.db_pool, loop, __name__, logging.DEBUG, "logs")
            #
            if db_connected:
                # Log message if successful
                self.logger.debug("Successfully configured logger.")
        except Exception as e:
            print(f"Failed to configure logger. Error: {e}")

        # From our cogs_list on init, loop through and use case matching to check for cogs
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
                        await self.add_cog(MentorCog(self, self.logger))
                case _:
                    # Default case: if no names matches, no cog is added
                    self.logger.error(f"Cog {cog} not found.")


    async def on_ready(self):
        # Called when bot is up and running
        self.logger.debug(f"Logged in as {self.user} (ID: {self.user.id})")


    async def close(self):
        # When the bot closes out, if there is an active connection to db_pool
        if self.db_pool is not None:
            if hasattr(self, "db_pool"):
                # We make sure the connection to db is closed
                self.logger.debug("Close database connection")
                await self.db_pool.close()
        await super().close()
