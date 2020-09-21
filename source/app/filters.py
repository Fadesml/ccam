import json
from typing import Dict

from state_manager.filters.base import BaseFilter
from vkwave.bots import BaseEvent
from vkwave.bots.addons.easy.base_easy_bot import SimpleBotEvent
from vkwave.types.bot_events import BotEventType


def has_payload(event: BaseEvent):
    if event.object.object.dict().get("payload") is not None:
        return True
    if (
        event.object.object.dict().get("message") is not None
        and event.object.object.dict()["message"].get("payload") is not None
    ):
        return True
    return False


class PayloadFilter(BaseFilter):
    def __init__(self, payload: Dict[str, str]) -> None:
        self.payload = payload

    async def check(self, event: SimpleBotEvent) -> bool:
        if not has_payload(event):
            return False
        if event.object.type == BotEventType.MESSAGE_EVENT.value:
            current_payload = event.object.object.payload
        else:
            current_payload = json.loads(event.object.object.message.payload)
        if current_payload is None:
            return False
        if self.payload is None:
            return True
        return current_payload == self.payload
