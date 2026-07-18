import logging
import os
import cv2
import easyocr

from src.preprocessing import PlatePreprocessor
from src.config import OUTPUT_FOLDER

logger = logging.getLogger(__name__)

DEBUG = os.getenv("DEBUG", "false").lower() == "true"


class OCRReader:

    def __init__(self):
        # Load EasyOCR once at startup
        self.reader = easyocr.Reader(["en"], gpu=False)
        self.preprocessor = PlatePreprocessor()

    def read_candidates(self, image):
        """
        Run OCR on multiple image variants.

        Returns:
            [
                {
                    "variant": 1,
                    "text": "...",
                    "confidence": 0.95,
                    "boxes": 4
                }
            ]
        """

        variants = self.preprocessor.generate_variants(image)

        candidates = []

        for index, variant in enumerate(variants):

            results = self.reader.readtext(
                variant,
                allowlist="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
                paragraph=False,
                decoder="beamsearch",
                width_ths=0.7,
                height_ths=0.7,
            )

            if not results:
                continue

            # Sort text boxes from left to right
            results = sorted(
                results,
                key=lambda r: r[0][0][0]
            )

            words = []
            confidences = []

            for box, text, conf in results:

                text = text.strip().upper()

                if not text:
                    continue

                words.append(text)
                confidences.append(conf)

            if not words:
                continue

            final_text = "".join(words)

            avg_conf = sum(confidences) / len(confidences)

            candidates.append(
                {
                    "variant": index + 1,
                    "text": final_text,
                    "confidence": float(avg_conf),
                    "boxes": len(words),
                }
            )

        print("\n" + "=" * 70)
        print("OCR Candidates")
        print("=" * 70)

        for c in candidates:
            print(
                f"Variant {c['variant']} | "
                f"Text: {c['text']} | "
                f"Confidence: {c['confidence']:.3f} | "
                f"Boxes: {c['boxes']}"
            )

        print("=" * 70)

        return candidates