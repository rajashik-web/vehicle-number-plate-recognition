import re

from src.validator import PlateValidator


class PlateCorrector:

    def __init__(self):
        self.validator = PlateValidator()

        self.letter_map = {
            "0": "O",
            "1": "I",
            "2": "Z",
            "5": "S",
            "6": "G",
            "8": "B",
            "4": "A",
        }

        self.digit_map = {
            "O": "0",
            "Q": "0",
            "D": "0",
            "I": "1",
            "L": "1",
            "T": "1",
            "Z": "2",
            "S": "5",
            "B": "8",
            "G": "6",
            "A": "4",
        }

        # State | District | Series | Number
        self.pattern = re.compile(
            r"^([A-Z]{2})([A-Z0-9]{1,2})([A-Z0-9]{1,3})([A-Z0-9]{4})$"
        )

    def _convert_letters(self, text):
        return "".join(
            self.letter_map.get(c, c)
            for c in text
        )

    def _convert_digits(self, text):
        return "".join(
            self.digit_map.get(c, c)
            for c in text
        )

    def correct(self, plate):

        if not plate:
            return ""

        plate = plate.upper().replace(" ", "").replace("-", "")

        # Already valid → don't modify
        if self.validator.is_valid(plate):
            return plate

        match = self.pattern.match(plate)

        # If we can't split it, return original.
        # (The validator will reject it later if needed.)
        if not match:
            return plate

        state, district, series, number = match.groups()

        corrected = (
            self._convert_letters(state)
            + self._convert_digits(district)
            + self._convert_letters(series)
            + self._convert_digits(number)
        )

        return corrected