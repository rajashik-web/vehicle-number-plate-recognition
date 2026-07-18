import logging

from src.detector import PlateDetector
from src.ocr import OCRReader
from src.ocr_voter import OCRVoter
from src.utils import normalize_plate
from src.validator import PlateValidator
from src.corrector import PlateCorrector
from src.services.decision_engine import DecisionEngine

logger = logging.getLogger(__name__)


class ANPRPipeline:

    def __init__(self):
        self.detector = PlateDetector()
        self.ocr = OCRReader()
        self.validator = PlateValidator()
        self.corrector = PlateCorrector()
        self.decision = DecisionEngine()
        self.voter = OCRVoter()

    def process(self, image):
        """
        Run the full ANPR pipeline on a single frame/image.

        Returns:
            (result, plates)
            result – raw YOLO result object (for drawing bounding boxes)
            plates – list of dicts:
                {
                    "bbox":           (x1, y1, x2, y2),
                    "confidence":     float,   # YOLO detection confidence
                    "image":          np.ndarray,
                    "text":           str,      # recognised plate or "" if unreadable
                    "ocr_confidence": float,
                }

        Fixes vs original:
          1. print() replaced with logger.debug().
          2. DecisionEngine is now wired in – plates below 0.80 OCR confidence
             are rejected as unreadable (text set to "").
          3. Unused import (is_valid_plate from utils) removed.
        """
        # ── Detect ───────────────────────────────────────────────────
        result = self.detector.detect(image)
        plates = self.detector.extract_plates(image, result)

        # ── OCR each cropped plate ────────────────────────────────────
        for plate in plates:
            # Generate OCR candidates from multiple image variants
            candidates = self.ocr.read_candidates(plate["image"])

            # Choose the best candidate
            winner = self.voter.vote(candidates)

            print("=" * 60)
            print("OCR CANDIDATES")
            for c in candidates:
                print(c)
            print("=" * 60)

            print("OCR WINNER:", winner)
            print("=" * 60)

            raw_text = winner["text"]
            ocr_conf = winner["confidence"]

            # Normalise → correct → validate
            text = normalize_plate(raw_text)
            text = self.corrector.correct(text)
            print("FINAL TEXT:", repr(text))
            print("VALID:", self.validator.is_valid(text))
            logger.debug(
                "OCR raw=%s  normalised=%s  valid=%s  conf=%.3f",
                raw_text,
                text,
                self.validator.is_valid(text),
                ocr_conf,
            )

            # Accept only if:
            #   • Plate format is valid (Indian registration regex)
            #   • DecisionEngine passes the OCR confidence threshold (≥ 0.80)
            if self.validator.is_valid(text) and self.decision.should_accept(text, ocr_conf):
                plate["text"] = text
            else:
                plate["text"] = ""

            plate["ocr_confidence"] = ocr_conf

        return result, plates
