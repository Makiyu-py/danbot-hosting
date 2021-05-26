from .helpers import check_resp_status
import aiohttp
import asyncio


class HTTPClient:

    def __init__(self, **kwargs) -> None:
        self.base_url = "https://danbot.host/api"
        self.loop = kwargs.get("loop", asyncio.get_event_loop())
        self.session = kwargs.get(
            "session", aiohttp.ClientSession(
                loop=self.loop))

    async def send_request(self, **kwargs):
        req_types = {
            "get": self.session.get,
            "post": self.session.post
        }

        async with req_types[kwargs["method"].lower()](
            url=self.base_url + kwargs["route"], data=kwargs["data"],
            headers={"Content-Type": "application/json",
                     **kwargs.get("extra_headers", {})}
        ) as resp:
            status = await check_resp_status(resp)

            if status:
                return resp

    async def post_info(self, **kwargs) -> None:
        await self.send_request(method="post", **kwargs)

    async def get_bot_info(self, **kwargs) -> dict:
        bot_data = await self.send_request(method="get", **kwargs)

        return await bot_data.json()

    async def close(self):
        await self.session.close()
