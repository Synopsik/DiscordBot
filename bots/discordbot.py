import os
from typing import Mapping

import asyncpg
from discord.ext import commands
import discord
from discord.ext.commands import Cog
from dotenv import load_dotenv
load_dotenv()

from cogs.games import GamesCog
from cogs.general import GeneralCog
from cogs.logging import LoggingCog, get_time
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

        description = "A Discord bot that does stuff."
        self.prefix = "!"
        super().__init__(command_prefix=self.prefix,
                         intents=intents,
                         description=description)

        self.run(os.getenv("BOT_TOKEN"))

    async def setup_hook(self):
        db_url = os.getenv("DB_URL")
        if db_url:
            try:
                self.db_pool = await asyncpg.create_pool(dsn=db_url)
                print("Database connection successful.")
            except OSError as e:
                print(f"Failed to connect to the database. Error: {e}")
                self.db_pool = None
        else:
            print("No DB_URL found. Skipping database connection.")

        for cog in self.cogs_list:
            print(f"[{await get_time()}] [EVENT] Loading {cog} cog")
            match cog:
                case "general":
                    await self.add_cog(GeneralCog(self))
                case "games":
                    await self.add_cog(GamesCog(self))
                case "logging":
                    if self.db_pool is not None:
                        await self.add_cog(LoggingCog(self, self.db_pool))
                case "mentor":
                    if self.db_pool is not None:
                        await self.add_cog(MentorCog(self, self.db_pool))
                case _:
                    print("Couldn't find cog.")

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")



    async def close(self):
        if self.db_pool is not None:
            if hasattr(self, "db_pool"):
                await self.db_pool.close()
        await super().close()
