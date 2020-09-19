from vkwave.bots import Keyboard

from app.config import SUBSCRIBE_TEXT, UNSUBSCRIBE_TEXT


def base_keyboard_instance() -> Keyboard:
    return Keyboard(one_time=True)


def subscribe_kb() -> str:
    kb = base_keyboard_instance()
    kb.add_text_button(text=SUBSCRIBE_TEXT, payload={"state": "subscribe"})
    return kb.get_keyboard()


def unsubscribe_kb() -> str:
    kb = base_keyboard_instance()
    kb.add_text_button(text=UNSUBSCRIBE_TEXT, payload={"state": "unsubscribe"})
    return kb.get_keyboard()
