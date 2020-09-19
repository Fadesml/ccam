from vkwave.bots.addons.easy.base_easy_bot import SimpleBotEvent


def get_vk_id(event: SimpleBotEvent) -> int:
    return event.object.object.message.from_id
