import cv2

from src.pipeline import ANPRPipeline

pipeline = ANPRPipeline()

image = cv2.imread("data/images/car.jpg")

result, plates = pipeline.process(image)

print("=" * 60)

for index, plate in enumerate(plates):

    print(f"Plate {index + 1}")
    print(f"YOLO Confidence : {plate['confidence']:.2f}")
    print(f"OCR Text        : {plate['text']}")
    print(f"OCR Confidence  : {plate['ocr_confidence']:.2f}")
    print(f"Bounding Box    : {plate['bbox']}")
    print("-" * 60)

    cv2.imshow(
        f"Plate {index+1}",
        plate["image"]
    )

cv2.waitKey(0)
cv2.destroyAllWindows()