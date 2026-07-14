import easyocr
import cv2


class OCRReader:

    def __init__(self):

        # Create OCR model only once
        self.reader = easyocr.Reader(
            ['en'],
            gpu=False
        )

    def read_text(self, image):

        # Resize
        image = cv2.resize(
            image,
            None,
            fx=3,
            fy=3,
            interpolation=cv2.INTER_CUBIC
        )

        # Convert to grayscale only
        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        results = self.reader.readtext(
            gray,
            allowlist="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        )

        if len(results) == 0:
            return {
                "text": "",
                "confidence": 0.0
            }

        best = max(results, key=lambda x: x[2])

        return {
            "text": best[1],
            "confidence": float(best[2])
        }