from typing import List, AsyncIterator

from databases import Database

from app.db.exceptions import UserNotExist
from app.db.models import users
from app.db.shemas import User


class UserRepository:
    def __init__(self, db: Database):
        self.db = db

    async def create(self, **values) -> int:
        return await self.db.execute(users.insert(), values=values)

    async def get_by_vk_id(self, vk_id: int) -> User:
        query = users.select().where(users.c.vk_id == vk_id)
        user = await self.db.fetch_one(query)
        if user is None:
            raise UserNotExist()
        return User.parse_obj({**user})

    async def get_by_subscribed_to_newsletter(self, subscribed_to_newsletter: bool) -> AsyncIterator[User]:
        query = (users
                 .select()
                 .where(users.c.subscribed_to_newsletter == subscribed_to_newsletter)
                 .order_by(users.c.subscribed_to_newsletter.desc())
                 )
        async for row in self.db.iterate(query=query):
            yield User.parse_obj({**row})

    async def exist(self, vk_id: int) -> bool:
        try:
            await self.get_by_vk_id(vk_id)
            return True
        except UserNotExist:
            return False

    async def update(self, vk_id: int, **data_to_update) -> None:
        query = users.update().values(**data_to_update).where(users.c.vk_id == vk_id)
        return await self.db.execute(query)
