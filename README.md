# DanBotHosting API Python Wrapper

A Python API Wrapper for the DanBot Hosting API

### **Still under development!!**

# Links

- [DanBot Hosting Discord Server](https://discord.gg/dbh)
- [DanBot Hosting Website](https://danbot.host)
- [Original Wrapper (for discord.js)](https://github.com/danbot-devs/danbot-hosting)

# Installation

### For Windows:

`pip install danbot-hosting-py`

### For Linux/MacOS

`pip3 install danbot-hosting-py`

# Examples

## Auto-posting

```python
from discord.ext import commands
from danbot_api import DanBotClient


bot = commands.Bot(command_prefix='>', description="This is a Helper Bot")


@bot.event
async def on_ready():
    DanBotClient(bot, key="your_dbh_key", autopost=True)
    print('Bot is Online')

@bot.event
async def on_dbh_post(data):
    print("Posted Bot Data to DBH. Data Posted:")
    print(data)

@bot.command()
async def ping(ctx):
    await ctx.send('pong!')

bot.run("your bot's token here")
```

# FAQ

> How do you get an API key?

#### Go to the [discord server](https://discord.gg/dbh) and use the `DBH!ApiKey` command in a respective text channel there!

> I'm having trouble with the module

#### You may post at the [issues section in Github](https://github.com/Makiyu-py/danbot-hosting/issues) or message me on Discord! (Makiyu^#4707)
