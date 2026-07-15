class PlateCorrector:

    def correct(self, plate):

        if plate is None:
            return ""

        plate = plate.upper()

        chars = list(plate)

        length = len(chars)

        # Indian plates usually end with 3 or 4 digits.
        # Fix only the last four positions.

        start = max(length - 4, 0)

        for i in range(start, length):

            if chars[i] == "O":
                chars[i] = "0"

            elif chars[i] == "I":
                chars[i] = "1"

            elif chars[i] == "S":
                chars[i] = "5"

            elif chars[i] == "B":
                chars[i] = "8"

            elif chars[i] == "Z":
                chars[i] = "2"

        return "".join(chars)