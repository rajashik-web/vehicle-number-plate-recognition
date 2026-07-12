from ultralytics import YOLO


class PlateDetector:
    def __init__(self):
        self.model = YOLO("models/license_plate/best.pt")

    def detect(self, image):
        results = self.model(image)
        return results[0]

    def crop_plate(self, image):

        result = self.detect(image)

        plates = []

        for box in result.boxes:

            x1, y1, x2, y2 = box.xyxy[0]

            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)

            confidence = float(box.conf)

            plate = image[y1:y2, x1:x2]

            plates.append({
                "bbox": (x1, y1, x2, y2),
                "confidence": confidence,
                "image": plate
            })

        return plates