import asyncio
from multiprocessing import Queue
from queue import Empty


class AsyncQueue:
    def __init__(self, queue: Queue):
        self.queue = queue

    async def get(self):
        while True:
            try:
                return self.queue.get(block=False)
            except Empty:
                await asyncio.sleep(0.01)
