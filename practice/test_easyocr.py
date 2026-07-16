import cv2

from src.ocr import OCRReader

ocr = OCRReader()

image = cv2.imread(
    "data/output/latest_crop.jpg"
)

result = ocr.read_text(image)

print(result)