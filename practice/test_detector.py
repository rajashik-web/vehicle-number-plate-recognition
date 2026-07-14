import cv2
import os

from src.detector import PlateDetector

image = cv2.imread("data/images/car.jpg")

detector = PlateDetector()

# Detect license plates
result = detector.detect(image)

# Extract cropped plates
plates = detector.extract_plates(image, result)

os.makedirs("data/output", exist_ok=True)

for i, plate in enumerate(plates):

    cv2.imwrite(
        f"data/output/plate_{i}.jpg",
        plate["image"]
    )

print(f"Detected {len(plates)} plate(s)")