# DiscordBot

Run either

> through the main.py file

or

> through the main_simple.py file

or    

> through a python console,
> 
> instantiate DiscordBot() on its own from bots/discordbots.py or store into a var `bot = DiscordBot()`

## Simple Bot Instructions

Instructions to run a Discord bot from a single file

### Get Discord Token

1. Login to Discord and create a private server

1. Follow [this link](https://discordpy.readthedocs.io/en/stable/discord.html) to create a bot account and get your token
  
3. Invite it to your server

### Setup Project

1. Create a project directory ..\Projects\DiscordBot\

2. Open a terminal and move to directory `cd ..\Projects\DiscordBot\`

3. Create a virtual environment to hold our libraries `python -m venv bot-env`

4. Enter virtual environment `.\bot-env\Scripts\activate` on Windows, `source bot-env/bin/activate` on Linux  

5. Install libraries `pip install -U discord.py, python-dotenv`
> [!Note]
> discord.py is used to operate bot
> 
> python-dotenv is used to interact with .env files

6. Create environment file through text editor, save as all files and name it .env
```
# example .env file
BOT_TOKEN="TOKEN_EXAMPLE_CODE"
```

### Develop Project

1. Create project file ..\Projects\DiscordBot\main_simple.py


2. Import necessary libraries, after importing the function load_dotenv() we need to call it, os is used to access our .env variables with dotenv
```
import discord
import os
from dotenv import load_dotenv
load_dotenv()
```

3. Create an intents object configuration file and set the permissions for channels you need, then you can instantiate your bot
```
intents = discord.Intents.default()
intents.presences = True # Allows the bot to view user presence (e.g., online/offline status)
intents.members = True # Lets the bot access member-related data (e.g., when users join or leave the server)
intents.message_content = True # Gives the bot access to read message content, such as the text within a message

# Create client bot instance
client = discord.Client(intents=intents)
```

4. Store token information from environment variable
```
# Setup token from environment,
# Alternatively this can be hardcoded
# token = "t0k3n...akljS2"
token = os.getenv("BOT_TOKEN")
```

5. Create an override function with the decorator `@client.event`, `on_message(message)` triggers anytime a message is posted on the server or sent directly to the bot
```
@client.event
async def on_message(message):
    # If the message the bot is viewing was written by the bot,
    # break out of function on_message
    if message.author == client.user:
        return
```

Once we validated that the message is not our own, we can use a case match statement to look for simple commands and process messages
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

6. Finally, the most important step we need to do is run our bot
```
# Run our bot once it is configured
client.run(token)
```

See `main_simple.py` for the entire file

## Advanced Bot Instructions

Instead of running everything from a single file that we endlessly scroll through to find a line to work on, we break our program up into meaningful classes that have their dedicated jobs, or **cogs**.

A cog is a class that inheirits `from discord.ext import commands` using `(commands.Cog, name="CogName")` for the parameters, inside this class we have overridable methods that have a context variable that can be used to pull information from the message recieved, the message author, and more context information. Using cogs we can seperate logic into interchangeable pieces that can be loaded and unloaded as needed.

For example, we can have a bot connected to multiple Discord servers. Based on the name of the server, or some other determining factor, after the bot init's it is able to load specific cogs. One server could have general, games, mentor while another server could have general, music, agent.

### Setup Project

1. If not already completed, finish **Get Discord Token** steps, and **Setup Project** instructions steps from Simple Bot

2. We need to create the folder structure for our DiscordBot within
```
DiscordBot
    ├── *bots
    │   ├── *__init__.py
    │   └── *discordbot.py # Instantiate this class to start the bot
    ├── *cogs
    │   ├── *__init__.py
    │   ├── agent.py # Agent cog for AI activities
    │   ├── games.py # Fun games for users to interact with
    │   ├── *general.py # Regular commands that are needed across every bot
    │   ├── logging.py # Logs every interaction the bot registers
    │   └── mentor.py # Connects user to a mentor interface to ask specific questions
    ├─ utilities
    |   ├── __init__.py
    |   ├── database_utils.py # Functions specific to interacting with external database
    |   └── logging_utils.py # Implements the Logging class and methods that store logs in database
    ├── *main.py # Use this to start up our Advanced Bot
    └── main_simple.py # Previous Simple Bot example
```
> [!Note]
>
> For now, only files and folders with a `*` prefix need to be created

### Develop Project

The core of our project can be found within our `discordbot.py` file

1. Import the same libraries as before, adding one more import for a specific class to inherit from
```
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
```

2. Create our Discord bot class, inhereits from the Bot class in commands
```
class DiscordBot(commands.Bot):
```

3. Set up init method to store important variables. We pass cogs as an optional argument that can hold an indefinite amount of values. We then configure the intents and other default config info to pass to the \_\_init__ method of the parent class. Once the class object is instantiated, we use the built-in run method to start our bot.
```
  def __init__(self, *cogs):
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
```
