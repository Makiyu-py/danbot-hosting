from aiohttp import ClientResponse
from discord import ClientUser
from .errors import *


async def check_resp_status(resp: ClientResponse) -> bool:
    resp_code = resp.status
    actual_resp = await resp.json()

    if resp_code == 200:
        return True
    elif resp_code >= 500:
        raise ServerError(resp_code)
    elif actual_resp.get('error', False):
        raise APIError(actual_resp['message'])


def get_client_info(bot_info: ClientUser) -> dict:
    clientinfo = {}

    for slot_name in bot_info.__slots__:
        if not slot_name.startswith("_"):
            try:
                item = getattr(bot_info, slot_name)
                if not str(item).startswith("<") and not str(
                        item).endswith(">"):  # check if "average" data type
                    clientinfo[slot_name] = item
            except AttributeError:
                pass

    # dbh bot could read name rather than returning "undefined"
    clientinfo["username"] = clientinfo.pop("name")

    return clientinfo
