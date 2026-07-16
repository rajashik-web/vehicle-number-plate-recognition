import easyocr
import cv2

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
        cv2.imwrite(
    "data/output/ocr_input.jpg",
    processed
)
        

        # OCR
        results = self.reader.readtext(
    processed,
    allowlist="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    paragraph=False,
    decoder="beamsearch",
    width_ths=0.7,
    height_ths=0.7
)
        if len(results) == 0:

            return {
                "text": "",
                "confidence": 0.0
            }

        print("\n" + "=" * 60)
        print("EasyOCR Results")
        print("=" * 60)

        for i, item in enumerate(results):

            bbox = item[0]
            text = item[1]
            confidence = item[2]

            print(f"{i+1}.")
            print("Text       :", text)
            print("Confidence :", confidence)
            print("Box        :", bbox)
            print("-" * 40)

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