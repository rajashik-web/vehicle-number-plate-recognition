from paddleocr import PaddleOCR

ocr = PaddleOCR(
    lang="en",
    enable_hpi=False
)

result = ocr.predict("data/output/plate_0.jpg")

print(result)