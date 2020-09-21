import asyncio
from threading import Thread
from queue import Queue as ThreadQueue
from typing import Callable, Awaitable

from databases import Database
from vkwave.bots import SimpleLongPollBot

from app.config import PATH_TO_IMAGES, DELAY_FOR_SEND_TO_VK, CAMERA_ID, ALERT_TEXT
from app.core.mailer import VkMailer
from app.core.watcher import Watcher
from app.utils.queue import AsyncQueue


async def start_face_recognition_service(database: Database, bot: SimpleLongPollBot) -> None:
    # создание очереди для обмена изображениями между процессами
    queue = ThreadQueue()
    async_queue = AsyncQueue(queue)  # создание асинхронной обертки над синхронной очередью, чтобы не блокировать event loop

    watcher = Watcher(DELAY_FOR_SEND_TO_VK, PATH_TO_IMAGES)
    Thread(target=watcher.run, args=(queue, CAMERA_ID)).start()  # запуск синхронную проверку камеры в другом процессе, чтобы не блокировать event loop

    mailer = VkMailer(database, bot)
    while True:
        images = await async_queue.get()  # получение изображений из очереди(другого процесса)
        await mailer.notify_users(images, ALERT_TEXT)


def startup_wrapper(database: Database, bot: SimpleLongPollBot) -> Callable[..., Awaitable[None]]:
    """connect to database"""
    async def startup() -> None:
        await database.connect()
        asyncio.ensure_future(start_face_recognition_service(database, bot))

    return startup


def shutdown_wrapper(database: Database) -> Callable[..., Awaitable[None]]:
    """disconnect to database"""
    async def shutdown() -> None:
        await database.disconnect()

    return shutdown
