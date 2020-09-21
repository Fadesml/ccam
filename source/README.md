# face_recognition_bot

Для работы необходим python

## Установка
```bash
pip install -r requirements.txt
```

## Перед запуском
Вставить в .env или env vk_token, camera_id
```bash
alembic upgrade head
```

## Запуск
```bash
python app/main.py
```

## Заполнение .env
1) Получение VK_API_TOKEN:  
Переходим в пункт Работа с API:
![Работа с API](./readme_images/1_vk.png)  
Переходим в пункт Long Poll API и включаем все как на скрине:
![Long Poll API](./readme_images/2_vk.png)  
Выбираем все пункты как на скрине:
![Все пункты](./readme_images/3_vk.png)  
Во вкладке "Ключи доступа" нажимаем кнопку "создать ключ" и выбираем все пункты как на скрине:   
![Long Poll API](./readme_images/4_vk.png)  

## Camera id
Получение все доступных id камер:
```bash
python cameras_id.py
```
Использование первой работающей камеры:  
camera_id = -1