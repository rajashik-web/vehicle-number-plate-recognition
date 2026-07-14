from ultralytics import YOLO
from src.config import MODEL_PATH


class PlateDetector:
    def __init__(self):
        self.model = YOLO(MODEL_PATH)

    def detect(self, image):
        results = self.model(
    image,
    conf=0.25,
    iou=0.3
)
        return results[0]

    def extract_plates(self, image, result):

        plates = []

        for box in result.boxes:

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            confidence = float(box.conf[0])

            # Add padding around the plate
            padding = 10

            x1 = max(0, x1 - padding)
            y1 = max(0, y1 - padding)

            x2 = min(image.shape[1], x2 + padding)
            y2 = min(image.shape[0], y2 + padding)

            plate = image[y1:y2, x1:x2]

            plates.append(
                {
                    "bbox": (x1, y1, x2, y2),
                    "confidence": confidence,
                    "image": plate,
                }
            )

        return plates