import aiohttp
import asyncio
from logic import App
import time

start = time.time()
loop = asyncio.get_event_loop()
app = App(loop)
asyncio.run(app.act())
print(time.time() - start)
