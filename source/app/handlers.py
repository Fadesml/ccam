from state_manager.models.state_managers.base import Depends
from state_manager.routes.vkwave import VkWaveRouter
from state_manager.filters.vkwave import text_filter
from vkwave.bots.addons.easy.base_easy_bot import SimpleBotEvent

from app.db.repositories import UserRepository
from app.filters import PayloadFilter
from app.keyboards import unsubscribe_kb, subscribe_kb
from app.depends import get_vk_id

router = VkWaveRouter()


@router.on.message_handler(text_filter(["старт", "start", "run", "начать"]))
async def start(event: SimpleBotEvent, user_repository: UserRepository, vk_id: int = Depends(get_vk_id)):
    if not await user_repository.exist(vk_id):
        await user_repository.create(vk_id=vk_id, subscribed_to_newsletter=False)
    await event.answer("Привет", keyboard=subscribe_kb())


@router.on.message_handler(PayloadFilter(payload={"state": "subscribe"}))
async def subscribe(event: SimpleBotEvent, user_repository: UserRepository, vk_id: int = Depends(get_vk_id)):
    await user_repository.update(vk_id, subscribed_to_newsletter=True)
    await event.answer("Рассылка включена", keyboard=unsubscribe_kb())


@router.on.message_handler(PayloadFilter(payload={"state": "unsubscribe"}))
async def unsubscribe(event: SimpleBotEvent, user_repository: UserRepository, vk_id: int = Depends(get_vk_id)):
    await user_repository.update(vk_id, subscribed_to_newsletter=False)
    await event.answer("Рассылка выключена", keyboard=subscribe_kb())
