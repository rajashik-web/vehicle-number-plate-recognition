import cv2

from src.camera import Camera
from src.pipeline import ANPRPipeline

camera = Camera()
pipeline = ANPRPipeline()

while True:

    frame = camera.read()

    if frame is None:
        break

    result, plates = pipeline.process(frame)

    output = result.plot()

    for plate in plates:

        x1, y1, x2, y2 = plate["bbox"]

        text = plate["text"]

        if text != "":

            cv2.putText(
                output,
                text,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

    cv2.imshow(
        "Live ANPR",
        output
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()

cv2.destroyAllWindows()