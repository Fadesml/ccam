from typing import List, Optional, Iterator

import cv2

from app.utils.utils import get_str_representation_image, get_face_from_image
from app.config import SCALE_FACTOR, MIN_NEIGHBORS

Image = List[List[List[int]]]


class Camera:
    def __init__(
        self,
        camera_id: int,
        *,
        xml_file: str = "haarcascade_frontalface_default.xml",
        scale_factor: float = SCALE_FACTOR,
        min_neighbors: int = MIN_NEIGHBORS
    ) -> None:
        self.camera = cv2.VideoCapture(camera_id)
        self.face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + xml_file)
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors

    def get_recognized_images(self):
        # получение изображений на которых найдено человеческое лицо
        for image in self.get_images():
            face_coordinates = self.get_face_coordinates(image)
            if face_coordinates is None:
                continue

            images = [get_str_representation_image(image)]
            for x, y, w, h in face_coordinates:
                images.append(get_str_representation_image(get_face_from_image(image, x, y, h, w)))

            yield images

    def get_face_coordinates(self, image: Image) -> Optional[List[List[int]]]:
        # получение координат лица
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        face_coordinates = self.face_detector.detectMultiScale(img_gray, self.scale_factor, self.min_neighbors)
        if isinstance(face_coordinates, tuple):
            return None
        return face_coordinates

    def get_images(self) -> Iterator[Image]:
        # получение всех изображений с камеры
        while True:
            _, img = self.camera.read()
            yield img
