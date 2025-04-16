# DiscordBot

Run either:

1. Through the `main.py` file


2. Through the `main_single_file.py` file


3. Through a python console, instantiate `DiscordBot()` on its own from `bots/discordbots.py` 
    
    or store into a var `bot = DiscordBot()`

---

## Simple Bot Instructions

Instructions to run a Discord bot from a single file

Example file: `main_single_file.py`

---

### Get Discord Token

1. Login to Discord and create a private server


2. Follow [this link](https://discordpy.readthedocs.io/en/stable/discord.html) to create a bot account and get your token
  

3. Invite it to your server

---

### Setup Project

4. Create a new project directory `..\Projects\DiscordBot\`


5. * Shift+Right Click inside the new folder 
   * Select `Open PowerShell` 
   * (or Open a terminal and `cd ..\Projects\DiscordBot\`)


6. Create a virtual environment to hold our libraries `python -m venv bot-env`


7. Enter virtual environment

    `.\bot-env\Scripts\activate` on Windows

    `source bot-env/bin/activate` on Linux  


8. Install libraries `pip install -U discord.py, python-dotenv`
> [!Note]
> discord.py is used to operate bot
> 
> python-dotenv is used to interact with .env files

9. Create environment file through text editor. 
    
    When saving, as the file type select all files, then name it `.env`
```
# example .env file
BOT_TOKEN="TOKEN_EXAMPLE_CODE"
```

---

### Develop Project

10. Create project file `..\Projects\DiscordBot\main_single_file.py`


11. * Import necessary libraries
    * After importing the function `load_dotenv()` we need to call it
    * os is used to access our .env variables with dotenv
```
import discord
import os
from dotenv import load_dotenv
load_dotenv()
```

12. * Create an intents object configuration file and set the permissions for channels you need
    * Then you can instantiate your bot
```
intents = discord.Intents.default()
intents.presences = True # Allows the bot to view user presence (e.g., online/offline status)
intents.members = True # Lets the bot access member-related data (e.g., when users join or leave the server)
intents.message_content = True # Gives the bot access to read message content, such as the text within a message

# Create client bot instance
client = discord.Client(intents=intents)
```

13. Store token information from environment variable
```
# Setup token from environment,
token = os.getenv("BOT_TOKEN")

# Alternatively this can just be hardcoded
# token = "t0k3n...akljS2"
```

14. * Create an override function `on_message(message)` with the decorator `@client.event`
    * This triggers anytime a message is posted on the server or sent directly to the bot
    * Async allows this function to be called concurrently with other async calls

        [this link](https://gist.github.com/Synopsik/cfdacaf1140111cd1acc101b0c1ca968) shows a simple example
```
@client.event
async def on_message(message):
    # If the message the bot is viewing was written by the bot,
    # break out of function on_message
    if message.author == client.user:
        return
```

* We validated that the message did not originate from our bot, then we can use a case match statement to look for simple commands and process messages
```
# Begin case statement to search for bot commands
    match message.content:
        case "!ping":
            print(f"[COMMAND] {message.author} sent command {message.content}")
            await message.channel.send("Pong!")
            # To reply directly we can do this instead
            # await message.channel.reply("Pong!")
        case _:
            # Default case, print to console
            print(f"[MESSAGE] {message.author}: {message.content}")
```

15. Finally, the most important step we need to do is run our bot
```
# Run our bot once it is configured
client.run(token)
```

See `main_single_file.py` for the entire file

---

## Advanced Bot Instructions

Instead of running everything from a single file that that can get messy and confusing, we break our program up into meaningful classes that have their dedicated jobs, or **cogs**.

A cog is a class that inherits the `commands.Cog` class `from discord.ext import commands`. When creating our class we also need to include a name parameter, this will look like `CogClass(commands.Cog, name="CogName")`. Inside this class, we have overridable methods that have a context parameter that can be used to pull information from the message received, the message author, and more context information. Using cogs we can separate logic into interchangeable pieces that can be loaded and unloaded as needed.

Using OOP principles, we can create multiple instances from a single bot class that use different variations of cogs, depending on some factor. One bot instance could have general, games, mentor while another instance could be using general, music, agent.

Example file: `main.py`

---

### Setup Project

1. If not already completed, finish **Get Discord Token** steps, and **Setup Project** instructions steps from Simple Bot


2. We need to create the folder structure for our DiscordBot within
```
DiscordBot
    ├── *bots
    │   ├── *__init__.py
    │   └── *discordbot.py # Instantiate this class to start the bot
    ├── *cogs
    │   ├── *__init__.py
    │   ├── agent.py # Agent cog for AI activities
    │   ├── games.py # Fun games for users to interact with
    │   ├── *general.py # Regular commands that are needed across every bot
    │   ├── logging.py # Logs every interaction the bot registers
    │   └── mentor.py # Connects user to a mentor interface to ask specific questions
    ├─ utilities
    │   ├── __init__.py
    │   ├── database_utils.py # Functions specific to interacting with external database
    │   └── logging_utils.py # Implements the Logging class and methods that store logs in database
    ├── *main.py # Use this to start up our Advanced Bot
    ├── main_single_file.py # Previous Simple Bot example
    └── .env # Stores important keys that we want hidden from version control
```
> [!Note]
> For now, only files and folders with a `*` prefix need to be created

---

### Develop Project

---

#### main.py

3. * Our main file will be very simple,

    * all we are doing is importing the `DiscordBot()` class (that we haven't created yet)
    
    * then instantiate DiscordBot with the string parameters we want attached to the bot as cogs

```
from bots.discordbot import DiscordBot()

if __name__ == "__main__":
    DiscordBot("general")

```


---

#### discordbot.py

4. * Import the same libraries as our SimpleBot
   * Additionally, we use `commands` so that our class can inherit directly from `commands.Bot`
```
from cogs.general import GeneralCog

import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
```

5. Create our Discord bot class, using our inherited `commands.Bot` as the Parent class
```
class DiscordBot(commands.Bot):
```

6. * Set up init method in `DiscordBot()` to store important variables.  
   * We pass cogs as an optional string argument that can hold an indefinite amount of names we can use to attach cogs
   * We then configure the intents and other default config info to pass to the \_\_init__ method of the parent class
   * After we run the init method of the Bot parent class, we use Bots built-in `run()` method to start it up
```
def __init__(self, *cogs):

# Configure cogs
for cog in cogs:
    case "general":
        await self.add_cog(GeneralCog(self))
    case _:
        print("No cogs found")

# Configure intents
intents = discord.Intents.default()
intents.presences = True
intents.members = True
intents.message_content = True

# Configure description and prefix
description = "A Discord bot that does stuff."
self.prefix = "!"

# Pass variables to Parents __init__ method
super().__init__(command_prefix=self.prefix,
                 intents=intents,
                 description=description)

self.run(os.getenv("BOT_TOKEN")) # Run bot
```
7. Finally, we log our bot's name and ID to the console once it's ready

```
async def on_ready(self):
    # Called when bot is up and running
    print(f"Logged in as {self.user} (ID: {self.user.id})")
```

---

#### general.py

8. * For `general.py` we need to import the essentials to create a cog class. 
   * Optionally, we will also need asyncio for a timer in our ping command

```
import discord
from discord.ext import commands
import asyncio
```

9. * Now, lets create our `GeneralCog()` class. 
    
        Not only do we inherit `commands.Cog`, we also need to pass a name argument for the bot
   * Then we can set up our __init__ method, we are only passing the DiscordBot() class to the cog

```
class GeneralCog(commands.Cog, name="General"):
    def __init__(self, bot):
        self.bot = bot
```

10. * Just like in our SimpleBot, we need to use decorators to listen for specific events
    * In this example, we are just printing to console when our cog is loaded

```
    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.debug("Loaded General Cog")
```

11. * Finally, lets set up our ping command
    * We use the name parameter to name our command,

        the prefix configured in discordbot.py `self.prefix = "!"` is how we will call it
    * We can then use `ctx.typing()` to make it look like our bot is typing a reply
    * We sleep for half a second before our message sends
    * Then we can use our context `ctx.send()` to send our message
    * You can also use `ctx.reply` to directly reply to the user


```
    @commands.command(name="ping")
    async def ping(self, ctx):
        await ctx.typing() # Imitate typing for half a second
        await asyncio.sleep(0.5)
        await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms") # Then send message
```

---

Congratulations on making it all the way through!
    
You now have a simple bot that can reply to you with a message and its latency

There are many other command examples in this repo 
    
Feel free to clone this and start experimenting with cogs and commands