import asyncio
import signal
from .api import make_api_server


async def _main():
    tasks = asyncio.gather(make_api_server())

    def _shutdown(*args):
        tasks.cancel()

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGTERM, _shutdown)
    loop.add_signal_handler(signal.SIGINT, _shutdown)
    await tasks


def main():
    try:
        asyncio.run(_main())
    except Exception as error:
        print("Unexpected error has ocurred.")
        print(repr(error))
