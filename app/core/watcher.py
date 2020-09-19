from typing import List

from app.core.camera import Camera
from time import time

from app.utils.utils import save
from multiprocessing import Queue


class Watcher:
    def __init__(self, delay_for_send_to_vk: float, path_to_save_image: str) -> None:
        self._time = time()
        self.delay_for_send_to_vk = delay_for_send_to_vk
        self.path_to_save_image = path_to_save_image

    def run(self, queue: Queue, camera_id: int) -> None:
        camera = Camera(camera_id)
        for images in camera.get_recognized_images():
            if self.is_send_time():
                queue.put_nowait(images)
                self._time = time()
            self.save_images(images)

    def is_send_time(self) -> bool:
        # Проверка на периодичность отправки сообщений
        return (time() - self._time) > self.delay_for_send_to_vk

    def save_images(self, images: List[str]) -> None:
        # сохранение изображений на диск
        for index, image in enumerate(images):
            save(f"{self.path_to_save_image}/{int(time())}_{index}.jpg", image)
