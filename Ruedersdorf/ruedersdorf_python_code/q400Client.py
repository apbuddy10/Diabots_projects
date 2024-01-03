import asyncio
from vq400connector import Vq400Connector



async def test():
    client=Vq400Connector()
    await client.initVQ400()
    await client.q400_execute_cam2(13)


asyncio.run (test())