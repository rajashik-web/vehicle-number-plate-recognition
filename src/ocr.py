import easyocr

from src.preprocessing import PlatePreprocessor


class OCRReader:

    def __init__(self):

        # Load EasyOCR once
        self.reader = easyocr.Reader(
            ['en'],
            gpu=False
        )

        # Image preprocessor
        self.preprocessor = PlatePreprocessor()

    def read_text(self, image):

        # Enhance plate image
        processed = self.preprocessor.process(
            image
        )

        # OCR
        results = self.reader.readtext(
            processed,
            allowlist="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        )

        if len(results) == 0:

            return {
                "text": "",
                "confidence": 0.0
            }

        best = max(
            results,
            key=lambda x: x[2]
        )

        return {
            "text": best[1],
            "confidence": float(best[2])
        }