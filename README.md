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

1. Create a project directory ../Projects/DiscordBot/

2. Open a terminal and move to directory `cd ../Projects/DiscordBot/`

3. Create a virtual environment to hold our libraries `python -m venv bot-env`

4. Enter virtual environment `source bot-env/bin/activate`

5. Install libraries `pip install -U discord.py, python-dotenv`
> [!Note]
> discord.py is used to operate bot, python-dotenv is used to interact with .env files

### Develop Project

1. Import necessary libraries, after importing the function load_dotenv() we need to call it, os is used to access our .env variables
```
import discord
import os
from dotenv import load_dotenv
load_dotenv()
```

2. Create an intents objects configuration file and set the permissions for channels you need, then you can instantiate your bot
```
intents = discord.Intents.default()
intents.presences = True # Allows the bot to view user presence (e.g., online/offline status)
intents.members = True # Lets the bot access member-related data (e.g., when users join or leave the server)
intents.message_content = True # Gives the bot access to read message content, such as the text within a message

# Create client bot instance
client = discord.Client(intents=intents)
```

3. Create an override function with the decorator `@client.event`, this triggers anytime a message is posted on the server or sent directly to the bot
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

4. Finally, the most important step we need to do is run our bot
```
# Run our bot once it is configured
client.run(token)
```
