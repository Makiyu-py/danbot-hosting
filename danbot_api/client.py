import requests as rq
import asyncio
import discord
import json

from .errors import *


async def check_resp_status(resp: rq.Response):  # for the requests stuff
    resp_code = resp.status_code

    if resp_code == 200:
        return True
    elif resp_code >= 500:
        raise ServerError(resp_code)
    elif resp.json()['error']:
        raise APIError(resp.json()['message'])


class DanBotClient:

    def __init__(self, bot: discord.Client, key: str, autopost: bool = False):
        """

        :param bot: your discord.py client
        :param key: the DanBot Hosting API key
        :param autopost: If you want to have autopost turned on/off (bool)
        """

        self.bot = bot

        if key.startswith('danbot_api-'):
            self.key = key
        else:
            raise NotAllowed("\"key\" is not prefixed with \"danbot_api-\". Please follow the key format")

        self.baseurl = 'https://danbot.host/api'

        if autopost:
            self.autopost_task = bot.loop.create_task(self._autopost())

    async def post(self, server_count: int, user_count: int):

        with rq.post(url=self.baseurl + f"/bot/{self.bot.user.id}/stats",
                     data={
                         "id": self.bot.user.id,
                         "key": self.key,
                         "servers": str(server_count),
                         "users": str(user_count),
                         "clientInfo": self.bot.user
                     },
                     headers={"Content-Type": "application/json"}) as resp:
            status = await check_resp_status(resp)

            if status:
                return True

    async def _autopost(self):

        print("DanBotHosting - Auto Post Started")  # how do u do logging??
        await self.post(len(self.bot.guilds),
                        len(set(self.bot.get_all_members())))  # Creates first post

        data = {
            "id": self.bot.user.id,
            "key": self.key,
            "servers": len(self.bot.guilds),
            "users": len(set(self.bot.get_all_members()))
        }

        self.bot.dispatch('dbh_post', data)

        while not self.bot.is_closed():
            await asyncio.sleep(60000)
            await self.post(len(self.bot.guilds),
                            len(set(self.bot.get_all_members())))
            self.bot.dispatch('dbh_post',  # basically triggers a on_dbh_post d.py event on every new post
                              data  # and may also return the dict that is used to post the bot info
                              )

    async def get_bot_info(self, bot_id: int = None):

        if bot_id is None:
            bot_id = self.bot.user.id

        with rq.get(self.baseurl + f"/bot/{bot_id}/stats") as data:
            if await check_resp_status(data):
                js_data = data.json()
            else:
                return False

        return json.loads(js_data)
