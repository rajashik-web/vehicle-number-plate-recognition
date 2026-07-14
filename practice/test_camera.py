import cv2

from src.camera import Camera

camera = Camera()

while True:

    frame = camera.read()

    if frame is None:
        break

    cv2.imshow(
        "Live Camera",
        frame
    )

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

camera.release()

cv2.destroyAllWindows()