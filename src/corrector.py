class PlateCorrector:

    def correct(self, plate):

        if not plate:
            return ""

        plate = plate.upper().replace(" ", "")

        chars = list(plate)

        # -------------------------
        # Letter positions
        # -------------------------

        letter_map = {
            "0": "O",
            "1": "I",
            "2": "Z",
            "5": "S",
            "8": "B"
        }

        # -------------------------
        # Digit positions
        # -------------------------

        digit_map = {
            "O": "0",
            "Q": "0",
            "D": "0",
            "I": "1",
            "L": "1",
            "Z": "2",
            "S": "5",
            "B": "8"
        }

        # First two characters → letters

        for i in [0, 1]:

            if i < len(chars):

                chars[i] = letter_map.get(
                    chars[i],
                    chars[i]
                )

        # State code digits

        for i in [2, 3]:

            if i < len(chars):

                chars[i] = digit_map.get(
                    chars[i],
                    chars[i]
                )

        # Series letters

        for i in [4, 5]:

            if i < len(chars):

                chars[i] = letter_map.get(
                    chars[i],
                    chars[i]
                )

        # Last four → digits

        for i in range(max(len(chars) - 4, 0), len(chars)):

            chars[i] = digit_map.get(
                chars[i],
                chars[i]
            )

        return "".join(chars)