from src.ocr import OCRReader
import cv2

ocr = OCRReader()

image = cv2.imread("data/output/plate_0.jpg")

result = ocr.read_text(image)

print(result)