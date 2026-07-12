import cv2
import os

from src.detector import PlateDetector

os.makedirs("data/output", exist_ok=True)

image = cv2.imread("data/images/car.jpg")

detector = PlateDetector()

plates = detector.crop_plate(image)

print(f"Detected {len(plates)} plate(s)")

for i, plate in enumerate(plates):

    print(plate["bbox"])

    print(plate["confidence"])

    cv2.imwrite(
        f"data/output/plate_{i}.jpg",
        plate["image"]
    )

print("Plate saved successfully!")