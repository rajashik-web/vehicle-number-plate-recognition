from paddleocr import PaddleOCR


class OCRReader:
    def __init__(self):
        self.reader = PaddleOCR(
            use_angle_cls=True,
            lang="en"
        )

    def read_text(self, image):
        result = self.reader.ocr(image)

        return result
    