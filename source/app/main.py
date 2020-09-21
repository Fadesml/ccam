import logging
import os
import sys

from databases import Database

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.split(dir_path)[0])

from app.db.repositories import UserRepository
from app.events import startup_wrapper, shutdown_wrapper
from app.handlers import router
from app.config import VK_API_TOKEN, DB_URL, GROUP_ID
from app.state_manager.storages.memory import MemoryStorage
from app.state_manager.routes.vkwave import VkWaveMainRouter

logging.basicConfig(level=logging.INFO)
main_instance = VkWaveMainRouter(VK_API_TOKEN, GROUP_ID)
database = Database(DB_URL)

main_instance.container.bind_constant(Database, database)
main_instance.container.bind_constant(UserRepository, UserRepository)

main_instance.include_router(router)

if __name__ == '__main__':
    main_instance.run(
        storage=MemoryStorage(),
        on_startup=startup_wrapper(database, main_instance.bot),
        on_shutdown=shutdown_wrapper(database)
    )
