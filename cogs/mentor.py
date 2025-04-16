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
        try:
            # Get list of currently available subjects
            for index, subject in enumerate(self.subjects):
                message += f"\n{index + 1}. {subject}"
            # Send DM to user and log it
            await ctx.author.send(message)
            self.logger.info(message)
        except Exception as e:
            self.logger.error(f"General Cog not found: {e}")