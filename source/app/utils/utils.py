from typing import Any, List

import cv2


def save(file_name: str, content: Any, *, mode: str = 'wb') -> None:
    with open(file_name, mode=mode) as f:
        f.write(content)


def get_str_representation_image(image: List[List[List[int]]], file_extension: str = '.jpg') -> str:
    return cv2.imencode(file_extension, image)[1]


def get_face_from_image(image: List[List[List[int]]], x: int, y: int, height: int, width: int):
    return image[y:y + height, x:x + width]
