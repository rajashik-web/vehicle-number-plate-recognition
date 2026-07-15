import cv2

from src.detector import PlateDetector

detector = PlateDetector()

image = cv2.imread(
    "data/images/car.jpg"
)

result = detector.detect(image)

plates = detector.extract_plates(
    image,
    result
)

print("=" * 50)
print("Detected:", len(plates))
print("=" * 50)

for i, plate in enumerate(plates):

    print()

    print("Plate", i + 1)

    print("BBox :", plate["bbox"])

    print("Confidence :", plate["confidence"])

    cv2.imshow(
        f"Plate {i+1}",
        plate["image"]
    )

cv2.waitKey(0)
cv2.destroyAllWindows()