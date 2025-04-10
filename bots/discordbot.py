import os

import asyncpg
from discord.ext import commands
import discord
from dotenv import load_dotenv
load_dotenv()

from cogs.games import GamesCog
from cogs.general import GeneralCog
from cogs.logging import LoggingCog
from cogs.mentor import MentorCog




class DiscordBot(commands.Bot):
    def __init__(self):

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
        
        db_url = os.getenv("DB_URL")
        # TODO Needs to create PostgreSQL database
        #self.db_pool = asyncpg.create_pool(dsn=db_url)
        #self.db_pool = self.loop.run_until_complete(self.db_pool)

        self.run(os.getenv("BOT_TOKEN"))

    async def setup_hook(self):
        await self.add_cog(GeneralCog(self))
        await self.add_cog(GamesCog(self))
        #self.add_cog(LoggingCog(self, self.db_pool))
        #self.add_cog(MentorCog(self, self.db_pool))

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")

    async def close(self):
        if hasattr(self, "db_pool"):
            await self.db_pool.close()
        await super().close()
