from pydantic import BaseModel


class User(BaseModel):
    id: int
    vk_id: int
    subscribed_to_newsletter: bool
