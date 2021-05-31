from discord.ext import commands
from danbot_api import DanBotClient
import logging


# logging stuff
dbh_logger = logging.getLogger('danbot_api')
dbh_logger.setLevel(level=logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(name)s: %(levelname)s - %(message)s')

ch.setFormatter(formatter)
dbh_logger.addHandler(ch)


bot = commands.Bot(command_prefix='!')
bot.dbh = DanBotClient(bot, key="dbh api key here", autopost=True)


@bot.event
async def on_ready():
    print('Bot is Online')


@bot.event
async def on_dbh_post(data):
    dbh_logger.info("Posted data to DBH")


@bot.command()
async def ping(ctx):
    await ctx.send('pong!')


bot.run("token here")
