from discord.ext import tasks
import aiohttp
import discord
import logging
import json

from .http import HTTPClient
from .helpers import *
from .errors import *


class DanBotClient:
    """Represents a client connection that connects to the DanBotHosting API.

    Parameters
    -----------
    bot : Union[discord.Client, discord.ext.commands.Bot])
        your discord.py client connection.
    key : str
        the DanBot Hosting API key.
    autopost : bool, default: False
        If you want to have autopost turned on/off.
    session : Optional[aiohttp.ClientSession]
        If you want to have a custom ClientSession instance for sending requests.
    """

    def __init__(
            self,
            bot: discord.Client,
            *,
            key: str,
            session: aiohttp.ClientSession = None,
            autopost: bool = False):

        self.bot = bot
        self.logger = logging.getLogger("danbot_api")
        self.http = HTTPClient(session=session, loop=bot.loop)

        if key.startswith('danbot-'):
            self.key = key
        else:
            raise NotAllowed(
                "\"key\" is not prefixed with \"danbot-\". Please follow the key format")

        self._is_closed = False
        self.baseurl = 'https://danbot.host/api'

        if autopost:
            self._autopost.loop = bot.loop
            self._autopost.start()

    async def post(self, server_count: int, user_count: int):
        """Main post method

        You don't need to use this method if you have the autopost
        paremeter in the class set to True.

        Parameters
        -----------
        server_count : int
            The server count you're posting to the API
        user_count : int
            The user count you're posting to the API

        Returns
        -------
        Optinal[dict]
            The data posted to the API
        """

        bot_inf = self.bot.user
        clientinfo = get_client_info(bot_inf)

        _data = {
            "id": str(bot_inf.id),
            "key": self.key,
            "servers": str(server_count),
            "users": str(user_count),
            "clientInfo": clientinfo
        }
        json_data = json.dumps(_data)

        await self.http.post_info(route=f"/bot/{bot_inf.id}/stats", data=json_data)

        return _data

    @tasks.loop(seconds=60000)
    async def _autopost(self):

        data = await self.post(len(self.bot.guilds),
                               len(set(self.bot.get_all_members())))
        self.bot.dispatch('dbh_post',  # basically triggers a on_dbh_post dpy event on every new post
                          data  # and may also return the dict that is used to post the bot info
                          )

    @_autopost.before_loop
    async def _ready_autopost(self):

        await self.bot.wait_until_ready()

        self.logger.info("Auto Post Started")

    async def get_bot_info(self, bot_id: int = None):
        """a coroutine that gets bots' infos from the API

        Parameters
        -----------
        bot_id: Optional[int]
            The id of the bot you're searching for. Defaults to the own bot's

        Returns
        -------
        Optional[dict]
            Data of the bot asked for, gotten from the API
        """

        if bot_id is None:
            bot_id = self.bot.user.id

        return await self.http.get_bot_info(route="/bot/{bot_id}/info")

    async def close(self):
        """Closes all of the connections.
        """

        self.logger.debug("Closing Connections...")
        
        if self._is_closed:
            return

        await self.http.close()
        self._autopost.cancel()

        self._is_closed = True
