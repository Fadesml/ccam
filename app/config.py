from app.utils.config import Config

config = Config(".env")

DB_URL = config("DB_URL", cast=str)
VK_API_TOKEN = config("VK_API_TOKEN", cast=str)

# Настройка точности нейронки
SCALE_FACTOR = config("SCALE_FACTOR", cast=float)
MIN_NEIGHBORS = config("MIN_NEIGHBORS", cast=int)

PATH_TO_IMAGES = config("PATH_TO_IMAGES", cast=str)
DELAY_FOR_SEND_TO_VK = config("DELAY_FOR_SEND_TO_VK", cast=float)
CAMERA_ID = config("CAMERA_ID", cast=int)

# Текст сообщений
ALERT_TEXT = "Обнаружен человек"

# Текст кнопок
SUBSCRIBE_TEXT = "Подписаться на рассылку"
UNSUBSCRIBE_TEXT = "Отписаться от рассылку"
