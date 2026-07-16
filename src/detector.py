from ultralytics import YOLO
from src.config import MODEL_PATH
import cv2

DEBUG = False

MIN_CONFIDENCE = 0.50
MIN_WIDTH = 80
MIN_HEIGHT = 30


class PlateDetector:

    def __init__(self):

        self.model = YOLO(MODEL_PATH)

    def detect(self, image):

        results = self.model(
            image,
            conf=0.25,
            iou=0.30
        )

        return results[0]

    def extract_plates(self, image, result):

        plates = []

        for box in result.boxes:

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            confidence = float(box.conf[0])

            # Ignore weak detections
            if confidence < MIN_CONFIDENCE:
                continue

            # Dynamic padding
            padding = int(max(x2 - x1, y2 - y1) * 0.15)

            x1 = max(0, x1 - padding)
            y1 = max(0, y1 - padding)

            x2 = min(image.shape[1], x2 + padding)
            y2 = min(image.shape[0], y2 + padding)

            plate = image[y1:y2, x1:x2]

            # Invalid crop
            if plate.size == 0:
                continue

            h, w = plate.shape[:2]

            # Ignore tiny plates
            if w < MIN_WIDTH or h < MIN_HEIGHT:
                continue

            # Save crop only for debugging
            if DEBUG:

                debug = cv2.resize(
                    plate,
                    None,
                    fx=4,
                    fy=4,
                    interpolation=cv2.INTER_CUBIC
                )

                cv2.imwrite(
                    "data/output/latest_crop.jpg",
                    debug
                )

            plates.append(
                {
                    "bbox": (x1, y1, x2, y2),
                    "confidence": confidence,
                    "image": plate,
                }
            )

        # Sort plates from left to right
        plates.sort(
            key=lambda plate: plate["bbox"][0]
        )

        return plates