from discord.ext import commands

class MentorCog(commands.Cog, name="Mentor"):
    def __init__(self, bot, logger):
        self.logger = logger
        self.bot = bot
        self.subjects = ["Science", "Math", "English", "CompSci"]

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.debug("Loaded Mentor Cog")

    @commands.command(name="subjects")
    async def select_subject(self, ctx):
        message = f"The currently available subjects are:"

        # List out currently available subjects
        for index, subject in enumerate(self.subjects):
            message += f"\n{index + 1}. {subject}"

        # Imitate typing, then reply and log message
        general_cog = self.bot.get_cog("General")
        if general_cog:
            await general_cog.dm(ctx, message)
            self.logger.info(message)
        else:
            self.logger.error("General Cog not found!")