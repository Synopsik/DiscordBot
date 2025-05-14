import discord
from discord.ext import commands
from utilities.api_utils import ask

class AgentCog(commands.Cog, name="Agent"):
    def __init__(self, bot, logger):
        self.bot = bot
        self.logger = logger

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.debug("Loaded Agent Cog")

    @commands.command(name="ask", help="Query the agent with a question.")
    async def query(self, ctx, *query: str):
        try:
            if not query:
                await ctx.send("Please provide a question to ask.")
                return
            query_text = " ".join(query)
            # Show typing indicator while processing
            async with ctx.typing():
                response = await ask(query_text, self.logger, show_thoughts=False)
                if response:
                    if isinstance(response, dict):
                        if "response" in response:
                            await ctx.send(response["response"])
                        elif "error" in response:
                            await ctx.send(f"Error: {response['error']}")
                        else:
                            await ctx.send(str(response))
                    else:
                        await ctx.send(str(response))
                else:
                    await ctx.send("Sorry, I didn't get a response from the API.")
        except Exception as e:
            self.logger.error(f"Error querying: {e}")
            await ctx.send(f"An error occurred: {str(e)}")

