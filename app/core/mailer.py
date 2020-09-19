import io
from random import randint
from typing import List

from databases import Database
from pydantic import ValidationError
from vkwave.bots import SimpleLongPollBot, PhotoUploader

from app.db.repositories import UserRepository


class VkMailer:
    def __init__(self, database: Database, bot: SimpleLongPollBot):
        self.user_repository = UserRepository(database)
        self.bot = bot
        self.uploader = PhotoUploader(self.bot.api_context)

    async def notify_users(self, images: List[str], message_text: str) -> None:
        # оповещение юзеров подписаных на рыссылку
        async for vk_ids in self._get_users_id():
            if not vk_ids:
                return
            attachments = await self._create_attachments(images, vk_ids[0])
            try:
                await self.bot.api_context.messages.send(
                    user_ids=vk_ids,
                    message=message_text,
                    random_id=randint(1, 255),
                    attachment=attachments
                )
            except ValidationError:
                continue

    async def _create_attachments(self, images: List[str], vk_id: int) -> str:
        # создание attachments для отправки нескольких фоток
        attachments = ""
        for index, image in enumerate(images):
            image = io.BytesIO(bytes(image))
            attachment = await self.uploader.get_attachment_from_io(vk_id, image)
            if index == len(images):
                attachments += f"{attachment}"
            else:
                attachments += f"{attachment},"
        return attachments

    async def _get_users_id(self):
        # получение id юзеров которые подписаны на рассылку
        vk_ids = []
        async for user in self.user_repository.get_by_subscribed_to_newsletter(True):
            if len(vk_ids) == 100:
                yield vk_ids
                vk_ids = []
            vk_ids.append(user.vk_id)
        yield vk_ids
