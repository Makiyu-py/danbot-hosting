import aiohttp
import asyncio
import discord
import logging
import json

from .http import HTTPClient
from .helpers import *
from .errors import *


class DanBotClient:
    """
    Represents a client connection that connects to the DanBotHosting API.

    :param bot: your discord.py client connection.
    :type bot: Union[discord.Client, discord.ext.commands.Bot]
    :param key: the DanBot Hosting API key.
    :type key: str
    :param autopost: If you want to have autopost turned on/off Default `False`.
    :type autopost: bool
    :param session: If you want to have a custom aiohttp.ClientSession instance for sending requests.
    :type session: aiohttp.ClientSession
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
            self.autopost_task = bot.loop.create_task(self._autopost())

    async def post(self, server_count: int, user_count: int):
        """main post method

        :param server_count: The server count you're posting to the API
        :type server_count: int
        :param user_count: The user count you're posting to the API
        :type user_count: int
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

    async def _autopost(self):

        self.logger.info("Auto Post Started")

        while not self.bot.is_closed():
            data = await self.post(len(self.bot.guilds),
                                   len(set(self.bot.get_all_members())))
            self.bot.dispatch('dbh_post',  # basically triggers a on_dbh_post dpy event on every new post
                              data  # and may also return the dict that is used to post the bot info
                              )
            await asyncio.sleep(60000)

    async def get_bot_info(self, bot_id: int = None):
        """a coroutine that gets bots' infos from the API

        :param bot_id: The id of the bot you're searching for. Defaults to the own bot's id
        :type bot_id: int
        """

        if bot_id is None:
            bot_id = self.bot.user.id

        return await self.http.get_bot_info(route="/bot/{bot_id}/info")

    async def close(self):
        """ closes all of the connections.
        """

        if self._is_closed:
            return

        await self.http.close()

        if hasattr(self, "autopost_task"):
            self.autopost_task.cancel()

        self._is_closed = True
