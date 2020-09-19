import cv2


cameras = []
for i in range(100):
    try:
        camera = cv2.VideoCapture(i).getBackendName()
        cameras.append(i)
    except:
        continue

print(cameras)
