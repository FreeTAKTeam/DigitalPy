import aiohttp

async def send_get_request(address: str, cookies: dict = {}):
    """This method is used to send a request to the network.
    Args:
        request (Request): the request message
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(address, cookies=cookies) as response:
            response_body = await response.text()
            response_session = response.cookies.get("session", None)
            return response_body, response_session