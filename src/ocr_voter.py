from collections import defaultdict

from src.utils import normalize_plate
from src.validator import PlateValidator


class OCRVoter:

    def __init__(self):
        self.validator = PlateValidator()

    def vote(self, candidates):
        """
        Select the best OCR candidate using:
        1. Normalized text
        2. Vote count
        3. Average confidence
        4. Plate validation
        """

        grouped = defaultdict(list)

        for candidate in candidates:

            text = normalize_plate(candidate["text"])

            if not text:
                continue

            grouped[text].append(candidate["confidence"])

        if not grouped:
            return {
                "text": "",
                "confidence": 0.0
            }

        best_text = ""
        best_conf = 0.0
        best_votes = -1
        best_valid = False

        for text, confidences in grouped.items():

            votes = len(confidences)
            avg_conf = sum(confidences) / votes
            valid = self.validator.is_valid(text)

            if (
                valid > best_valid
                or (
                    valid == best_valid
                    and (
                        votes > best_votes
                        or (
                            votes == best_votes
                            and avg_conf > best_conf
                        )
                    )
                )
            ):
                best_text = text
                best_conf = avg_conf
                best_votes = votes
                best_valid = valid

        return {
            "text": best_text,
            "confidence": best_conf,
            "votes": best_votes,
            "valid": best_valid
        }